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
from .app import app

API_URL = config['brickapi']['API_URL']
bs_url = config['brickapi']['API_URL']
rawqueries_url = bs_url + ''
entity_url = bs_url + '/entities'
user_url = bs_url + '/user'  # TODO: This should be updated.
ts_url = bs_url + '/data/timeseries'
actuation_url = bs_url + '/actuation'
domain_url = bs_url + '/domains'
app_url = bs_url + '/apps'

# brick_prefix = config['brick']['brick_prefix']
# ebu3b_prefix = config['brick']['building_prefix']

# cid = config['google_oauth']['client_id']
# csec = config['google_oauth']['client_secret']

production = False


def parse_header_token():
    return request.headers['Authorization'][7:]


# def get_token():
#     user_token = parse_header_token()
#     body = {
#         'user_access_token': user_token,
#         'client_id': cid,
#         'client_secret': csec,
#     }
#     url = API_URL + '/auth/get_token'
#     resp = requests.post(url, json=body, verify=False)
#     token = resp.json()['token']
#     return token


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
        app.logger.info("query_sparql result: %s", resp.json())
        return resp.json()


def query_user_profiles_arguments(api_token):
    payload = parse_api_token(api_token)
    resp = requests.get(
        f"{app_url}/me",
        headers=get_headers(api_token),
        verify=False
    )
    if resp.status_code == 401:
        raise exceptions.Unauthorized()
    app.logger.info("user_profiles_arguments result: %s", resp.json())
    if resp.status_code != 200:
        return None
    return resp.json()


def query_data(uuid, api_token, value_type="number"):
    payload = parse_api_token(api_token)
    query_url = f"{actuation_url}/domains/{payload['domain']}/read"
    body = {f'{uuid}': [""]}
    resp = requests.post(
        query_url,
        json=body,
        headers=get_headers(api_token),
        verify=False,
    )
    if resp.status_code == 401:
        raise exceptions.Unauthorized()
    app.logger.info("query data result: %s", resp.json())
    if resp.status_code != 200:
        return None
    if "results" not in resp.json()["data"]:
        return None
    data = resp.json()["data"]["results"]
    print(data)
    return float(data[0]["detail"])


def query_actuation(uuid, value, api_token):
    payload = parse_api_token(api_token)
    body = {f'{uuid}': [str(value)]}
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
            'campus': 'Central',
            'building': 'Center Hall',
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


# def _get_hvac_zone_point(tagset, room, api_token):
#     q = f"""
#     select ?s where {{
#         # <{room}> rdf:type brick:HVAC_Zone .
#         ?e brick:feeds {room} . 
#         ?p brick:isPointOf ?e . 
#         ?p a {tagset} .
#     }}
#     """
#     resp = query_sparql(q, api_token)
#     if resp == None:
#         return None
#     res = resp["data"]
#     print(res)
#     return res['s']


def _get_vav_point(tagset, room, api_token):
    q = f"""
    select ?s where {{
        ?vav brick:feeds {room} .
        ?vav a brick:Equipment .
        ?vav brick:hasPoint ?s .
        ?s a brick:{tagset} .
    }}
    """
    # print(q)
    resp = query_sparql(q, api_token)
    if resp == None:
        return None
    # res = resp['tuples']
    res = resp["data"]
    print(res)
    if len(res.get('s', [])) > 0:
        return res['s'][0]


def get_temperature_setpoint(room, api_token):
    tagset = 'Warm_Cool_Adjust_Sensor'
    return _get_vav_point(tagset, room, api_token)


def get_zone_temperature_sensor(room, api_token):
    tagset = 'Zone_Air_Temperature_Sensor'
    return _get_vav_point(tagset, room, api_token)

def get_zone_carbon_sensor(room, api_token):
    tagset = 'CO2_Sensor'
    return _get_vav_point(tagset, room, api_token)

# def get_thermal_power_sensor(room, api_token):
#     #    q = """
#     #    select ?s where {{
#     #        <{0}> user:hasOffice {1} .
#     #        {1} rdf:type brick:HVAC_Zone .
#     #        ?vav brick:feeds {1}.
#     #        ?vav brick:hasPoint ?s.
#     #        ?s a/rdfs:subClassOf* brick:Thermal_Power_Sensor .
#     #    }}
#     #    """.format(user_email, room)
#     q = f"""  
#     select ?s where {{
#     ?vav brick:feeds {room}.
#     ?vav brick:hasPoint ?s.
#     ?s a brick:Thermal_Power_Sensor.
#     }}
#     """
#     resp = query_sparql(q, api_token)
#     if resp is None:
#         return None
#     # res = resp['tuples']
#     # return res[0][0]
#     res = resp['results']['bindings'][0]
#     return res['s']['value']


def get_occupancy_command(room, api_token):
    tagset = 'Occupancy_Sensor'
    return _get_vav_point(tagset, room, api_token)
