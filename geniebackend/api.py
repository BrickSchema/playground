# from .middlewares import login_required
import pdb
import requests
import json, copy
import arrow
from datetime import datetime, timedelta
import jwt

from werkzeug import exceptions
from flask import request

from .configs import config

API_URL = config['brickapi']['API_URL']
bs_url = config['brickapi']['API_URL']
rawqueries_url = bs_url + '/rawqueries'
entity_url = bs_url + '/entities'
user_url = bs_url + '/user'  # TODO: This should be updated.
ts_url = bs_url + '/data/timeseries'
actuation_url = bs_url + '/actuation'

brick_prefix = config['brick']['brick_prefix']
ebu3b_prefix = config['brick']['building_prefix']

cid = config['google_oauth']['client_id']
csec = config['google_oauth']['client_secret']

production = False


def parse_header_token():
    return request.headers['Authorization'][7:]


def get_token():
    user_token = parse_header_token()
    body = {
        'user_access_token': user_token,
        'client_id': cid,
        'client_secret': csec,
    }
    url = API_URL + '/auth/get_token'
    resp = requests.post(url, json=body, verify=False)
    token = resp.json()['token']
    return token


def parse_api_token(api_token):
    return jwt.decode(
        api_token, options={"verify_signature": False}
    )


def get_headers(api_token):
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_token,
    }


def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})


def query_sparql(qstr, api_token):
    payload = parse_api_token(api_token)
    headers = get_headers(api_token)
    headers['Content-Type'] = 'sparql-query'
    resp = requests.post(
        f"{rawqueries_url}/domains/{payload['domain']}/sparql",
        headers=headers,
        data=qstr,
        verify=False
    )
    if resp.status_code != 200:
        return None
    else:
        return resp.json()


def query_data(uuid, api_token):
    payload = parse_api_token(api_token)
    if production:
        start_time = arrow.get().shift(minutes=-30).timestamp
        end_time = arrow.get().timestamp
    else:
        # start_time = arrow.get(2019,3,1).timestamp
        start_time = 1581161300
        # end_time = arrow.get(2019,3,30).timestamp
        end_time = 2581161311

    params = {
        'start_time': start_time,
        'end_time': end_time,
        'entity_id': uuid,
    }
    print('query params:', params)
    query_url = f"{ts_url}/domains/{payload['domain']}"
    print('query dst:', query_url)
    resp = requests.get(
        query_url,
        params=params,
        headers=get_headers(api_token),
        verify=False,
    )
    if resp.status_code == 401:
        raise exceptions.Unauthorized()
    print(resp.json())
    if resp.status_code != 200:
        return None
    data = resp.json()["data"]
    if data:
        data.sort(key=lambda d: d[1], reverse=True)
        return data[0][2]
    else:
        return None


def query_actuation(uuid, value, api_token):
    payload = parse_api_token(api_token)
    body = {uuid: [value]}
    resp = requests.post(
        f"{actuation_url}/domains/{payload['domain']}",
        json=body,
        headers=get_headers(api_token),
        verify=False,
    )
    if resp.status_code == 401:
        raise exceptions.Unauthorized()


def query_entity_tagset(uuid, api_token):
    payload = parse_api_token(api_token)
    params = {
        "domain": payload["domain"],
        "entity_id": uuid,
    }
    resp = requests.get(
        entity_url,
        params=params,
        headers=get_headers(api_token),
        verify=False,
    )
    if resp.status_code == 401:
        raise exceptions.Unauthorized()
    if resp.status_code != 200:
        return None
    return resp.json()["type"]


def extract(s, prefix_tagset):
    return s.replace(prefix_tagset, '')


def json_model(key):
    if key == "ebu3b":
        return {
            'college': 'UCSD',
            'campus': 'Main',
            'building': 'EBU3B'
        }
    return {}


def iterate_extract(list, prefix_tagset):
    res = []
    # for s in list:
    #    fields = extract(s[0], prefix_tagset).lower().split("_rm_")
    #    temp = copy.deepcopy(json_model("ebu3b"))
    #    temp['room'] = fields[1]
    #    res.append(temp)
    for s in list:
        res.append({
            'room': s['s']['value'],
            'college': 'UCSD',
            'campus': 'Warren',
            'building': 'BLDG',
        })
    return res


def get_user(jwt_token):
    res = requests.get(user_url,
                       headers=get_headers(jwt_token),
                       verify=False,
                       )
    if res.status_code == 401:
        raise exceptions.Unauthorized()
    if res.status_code == 200:
        return res.json()['name']
    else:
        return None


def _get_hvac_zone_point(tagset, room, api_token):
    q = f"""
    select ?s where {{
        <{room}> rdf:type brick:HVAC_Zone .
        #?zone rdf:type brick:HVAC_Zone .
        <{room}> brick:hasPoint ?s.
        ?s rdf:type brick:{tagset} .
    }}
    """
    resp = query_sparql(q, api_token)
    if resp == None:
        return None
    # res = resp['tuples']
    # return extract(res[0][0], ebu3b_prefix)
    res = resp['results']['bindings'][0]
    return res['s']['value']


def _get_vav_point(tagset, room, api_token):
    q = f"""
    select ?s where {{
        <{room}> rdf:type brick:HVAC_Zone .
        ?vav brick:feeds <{room}> .
        ?vav rdf:type brick:VAV .
        ?vav brick:hasPoint ?s .
        ?s rdf:type brick:{tagset} .
    }}
    """
    resp = query_sparql(q, api_token)
    if resp == None:
        return None
    # res = resp['tuples']
    print(resp)
    res = resp['results']['bindings'][0]
    return res['s']['value']


def get_temperature_setpoint(room, api_token):
    tagset = 'Zone_Air_Temperature_Setpoint'
    return _get_vav_point(tagset, room, api_token)


def get_zone_temperature_sensor(room, api_token):
    tagset = 'Zone_Air_Temperature_Sensor'
    return _get_hvac_zone_point(tagset, room, api_token)


def get_thermal_power_sensor(room, api_token):
    #    q = """
    #    select ?s where {{
    #        <{0}> user:hasOffice {1} .
    #        {1} rdf:type brick:HVAC_Zone .
    #        ?vav brick:feeds {1}.
    #        ?vav brick:hasPoint ?s.
    #        ?s a/rdfs:subClassOf* brick:Thermal_Power_Sensor .
    #    }}
    #    """.format(user_email, room)
    q = f"""
    select ?s where {{
    ?vav brick:feeds <{room}>.
    ?vav brick:hasPoint ?s.
    ?s a brick:Thermal_Power_Sensor.
    }}
    """
    resp = query_sparql(q, api_token)
    if resp == None:
        return None
    # res = resp['tuples']
    # return res[0][0]
    res = resp['results']['bindings'][0]
    return res['s']['value']


def get_occupancy_command(room, api_token):
    tagset = 'On_Off_Command'
    return _get_vav_point(tagset, room, api_token)
