# from .middlewares import login_required
import os
import pdb
import requests

import jwt
import arrow
from flask import Flask, redirect, url_for, session, request, jsonify, g, json
from flask_cors import CORS
from werkzeug import exceptions

from .app import app
from .api import *
from .configs import config

# INDEX_URL = config['genie_index']
# AUTH_URL = config['brickapi']['AUTH_URL'].format(API_URL=API_URL)
# ebu3b_prefix = 'http://ucsd.edu/building/ontology/ebu3b#'
# mock_prefix = 'ebu3b:EBU3B_Rm_'

production = False


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

@app.route('/api/redirected')
def redirected():
    # access_token = request.args['user_access_token']
    # # body = {
    # #     'user_access_token': access_token,
    # #     'client_id': cid,
    # #     'client_secret': csec,
    # # }
    # # url = API_URL + '/auth/get_token'
    # # resp = requests.post(url, json=body, verify=False)
    # # session['app_token'] = resp.json()['token']
    #
    # url = API_URL + '/user'
    # authorization = 'Bearer {0}'.format(access_token)
    # res = requests.get(url, headers={'Authorization': authorization}, verify=False)
    # print("redirected", res.json())
    # user_email = res.json()['email']
    api_token = config["api_token"]
    payload = parse_api_token(api_token)
    return payload["user_id"]


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


@app.route("/api/room", methods=["GET"])
def get_all_rooms():
    api_token = config["api_token"]
    resp = query_user_profiles_arguments(api_token)
    if resp is None:
        return json_response({'message': 'error'}, 200)
    print(resp)
    rooms = []
    rooms.append({
        'room': resp["data"]["arguments"]["room"],
        'college': 'UCSD',
        'campus': 'Central',
        'building': resp["data"]["domain"]["name"],
    })
    # for arguments_dict in resp:
    #     print(arguments_dict)
    #     for value in arguments_dict.values():
            
    # res = resp['results']['bindings']
    # rooms = iterate_extract(res, ebu3b_prefix) if res else []
    # print(rooms)
    return json_response({'rooms': rooms})


# @app.route("/api/room", methods=["GET"])
# def get_all_rooms():
#     user_email = request.args['user_email']
#     jwt_token = request.headers['Authorization'].split(' ')[1]
#     authorization = 'Bearer {0}'.format(jwt_token)
#     q = """
#     select ?s where {{
#         <{0}> brick:hasOffice ?s.
#         ?s rdf:type brick:HVAC_Zone .
#     }}
#     """.format(user_email)
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
        app.logger.info('get_temp_setpoint value: %s', value)
        resp = json_response({'value': value})
    except exceptions.Unauthorized as e:
        resp = json_response({'value': None,
                              'status_code': 401})
    return resp


@app.route("/api/point/setpoint/<room>", methods=["POST"])
def set_temp_setpoint(room):
    api_token = config["api_token"]
    uuid = get_temperature_setpoint(room, api_token)
    print(uuid)
    if not uuid:
        return json_response({'value': None})
    req_data = request.get_json()
    # req_data = {"value": 1}
    query_actuation(uuid, req_data['value'], api_token)
    return json_response({'value': req_data['value']})


@app.route("/api/point/temp/<room>", methods=["GET"])
def get_room_temperature(room):
    api_token = config["api_token"]
    uuid = get_zone_temperature_sensor(room, api_token)
    # uuid = bldg:BLDG_RM101_ZN_T
    print(uuid)
    if not uuid:
        return json_response({'value': None})
    # app_token = session['app_token']
    value = query_data(uuid, api_token)
    app.logger.info('get_room_temperature: %s', value)
    return json_response({'value': value})


@app.route("/api/point/energy/<room>", methods=["GET"])
def get_energy_usage(room): # too lazy change the function name
    api_token = config["api_token"]
    uuid = get_zone_carbon_sensor(room, api_token)
    # app.logger.info(f"get_energy_usage of {uuid}")
    # uuid = bldg:BLDG_RM101_MTR
    if not uuid:
        return json_response({'value': None})
    # app_token = session['app_token']
    value = query_data(uuid, api_token)
    app.logger.info('get_co2: %s', value)
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
        app.logger.info('get_status: %s', value)
    except exceptions.Unauthorized as e:
        resp = json_response({'value': None,
                              'status_code': 401})
    return resp


# @app.route("/api/point/status/<room>", methods=["POST"])
# def set_status(room):
#     api_token = config["api_token"]
#     uuid = get_occupancy_command(room, api_token)
#     # uuid = bldg:BLDG_RM101_ONOFF
#     if not uuid:
#         return json_response({'value': None})
#     req_data = request.get_json()
#     # 3 means on, 1 means off
#     resp = query_actuation(uuid, req_data['value'], api_token)
#     return json_response({'value': req_data['value']})


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
