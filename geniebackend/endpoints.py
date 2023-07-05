# from .middlewares import login_required
import os
import pdb
import requests

import jwt
import arrow
from flask import Flask, redirect, url_for, session, request, jsonify, g, json
from flask_cors import CORS
from werkzeug import exceptions

from .api import json_response, get_user, query_sparql, query_actuation, query_data, query_entity_tagset, \
    iterate_extract, get_zone_temperature_sensor, get_occupancy_command, get_temperature_setpoint, \
    get_thermal_power_sensor, API_URL, get_token, cid, csec, parse_api_token, get_headers
from .configs import config

INDEX_URL = config['genie_index']
AUTH_URL = config['brickapi']['AUTH_URL'].format(API_URL=API_URL)
ebu3b_prefix = 'http://ucsd.edu/building/ontology/ebu3b#'
mock_prefix = 'ebu3b:EBU3B_Rm_'

production = False

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
CORS(app)


@app.route('/')
def hello_main():
    return 'hello Genie backend'


# @app.route('/api/log')
# def login():
#     return redirect(AUTH_URL)
#
# @app.route('/api/logout')
# def logout():
#     resp = requests.post('https://accounts.google.com/o/oauth2/revoke',
#     params={'token': session['app_token']},
#     headers = {'content-type': 'application/x-www-form-urlencoded'})
#     if resp.ok:
#         session.pop('app_token', None)
#     return redirect(INDEX_URL)

# @app.route('/api/redirected')
# def redirected():
#     access_token = request.args['user_access_token']
#     # body = {
#     #     'user_access_token': access_token,
#     #     'client_id': cid,
#     #     'client_secret': csec,
#     # }
#     # url = API_URL + '/auth/get_token'
#     # resp = requests.post(url, json=body, verify=False)
#     # session['app_token'] = resp.json()['token']
#
#     url = API_URL + '/user'
#     authorization = 'Bearer {0}'.format(access_token)
#     res = requests.get(url, headers={'Authorization': authorization}, verify=False)
#     print("redirected", res.json())
#     user_email = res.json()['email']
#     return user_email

# @app.route("/api/userid")
# def get_userid():
#     # print(config)
#     # jwt_token = config["api_token"]
#     # data = jwt.decode(jwt_token.encode("ascii"), options={"verify_signature": False})
#     # return data
#
#     jwt_token = config["api_token"]
#     # jwt_token = request.args['user_token']
#     url = API_URL + '/user'
#     authorization = 'Bearer {0}'.format(jwt_token)
#     res = requests.get(url, headers={'Authorization': authorization})
#     user_email = res.json()
#     return user_email


# @app.route("/api/room", methods=["GET"])
# def get_all_rooms():
#     jwt_token = request.headers['Authorization'].split(' ')[1]
#     authorization = 'Bearer {0}'.format(jwt_token)
#     q = f"""
#     select ?s where {{
#         ?s rdf:type brick:HVAC_Zone .
#     }}
#     """
#     resp = query_sparql(q, authorization)
#     if resp == None:
#         return json_response({'message': 'error'}, resp.status_code)
#     # print(resp)
#     res = resp['results']['bindings']
#     rooms = iterate_extract(res, ebu3b_prefix) if res else []
#     return json_response({'rooms': rooms})


@app.route("/api/point/setpoint/<room>", methods=["GET"])
def get_temp_setpoint(room):
    api_token = config["api_token"]
    uuid = get_temperature_setpoint(room, api_token)
    # app_token = session['app_token']
    # uuid = bldg:BLDG_RM101_ZNT_SP
    if not uuid:
        return json_response({'value': None})
    try:
        value = query_data(uuid, api_token)
        print('get_temp_setpoint value:', value)
        resp = json_response({'value': value})
    except exceptions.Unauthorized as e:
        resp = json_response({'value': None,
                              'status_code': 401})
    return resp


@app.route("/api/point/setpoint/<room>", methods=["POST"])
def set_temp_setpoint(room):
    api_token = config["api_token"]
    uuid = get_temperature_setpoint(room, api_token)
    if not uuid:
        return json_response({'value': None})
    req_data = request.get_json()
    query_actuation(uuid, req_data['value'], api_token)
    return json_response({'value': req_data['value']})


@app.route("/api/point/temp/<room>", methods=["GET"])
def get_room_temperature(room):
    api_token = config["api_token"]
    uuid = get_zone_temperature_sensor(room, api_token)
    # uuid = bldg:BLDG_RM101_ZN_T
    if not uuid:
        return json_response({'value': None})
    # app_token = session['app_token']
    value = query_data(uuid, api_token)
    print('get_room_temperature:', value)
    return json_response({'value': value})


@app.route("/api/point/energy/<room>", methods=["GET"])
def get_energy_usage(room):
    api_token = config["api_token"]
    uuid = get_thermal_power_sensor(room, api_token)
    # uuid = bldg:BLDG_RM101_MTR
    if not uuid:
        return json_response({'value': None})
    # app_token = session['app_token']
    value = query_data(uuid, api_token)
    print('get_energy_usage:', value)
    return json_response({'value': value})


@app.route("/api/point/status/<room>", methods=["GET"])
def get_status(room):
    api_token = config["api_token"]
    uuid = get_occupancy_command(room, api_token)
    if not uuid:
        return json_response({'value': None})
    # app_token = session['app_token']
    try:
        value = query_data(uuid, api_token)
        resp = json_response({'value': value})
    except exceptions.Unauthorized as e:
        resp = json_response({'value': None,
                              'status_code': 401})
    return resp


@app.route("/api/point/status/<room>", methods=["POST"])
def set_status(room):
    api_token = config["api_token"]
    uuid = get_occupancy_command(room, api_token)
    # uuid = bldg:BLDG_RM101_ONOFF
    if not uuid:
        return json_response({'value': None})
    req_data = request.get_json()
    # 3 means on, 1 means off
    resp = query_actuation(uuid, req_data['value'], api_token)
    return json_response({'value': req_data['value']})


@app.route("/api/user", methods=["GET"])
def get_current_user():
    api_token = config["api_token"]
    url = API_URL + '/user'
    res = requests.get(url, headers=get_headers(api_token))
    return res.json()


if __name__ == '__main__':
    # ssl_context = (config['ssl']['cert'], config['ssl']['key'])
    app.run(host=config['host'],
            port=config['port'],
            # ssl_context=ssl_context,
            )
