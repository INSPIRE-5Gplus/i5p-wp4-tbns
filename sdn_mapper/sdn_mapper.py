#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from config_files import settings


#### SDN TRANSPORT CONTROLLER URL
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
def get_nsm_url():
    controller_ip = os.environ.get("SDN_CONTROLLER_IP")
    controller_port = os.environ.get("SDN_CONTROLLER_PORT")
    controller_url = "http://"+ str(controller_ip) +":"+ str(controller_port)  #TODO: check the API
    return controller_url


#### REQUESTS
# returns the local context  #NOTE: currently the data is emulated
def get_local_context():
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code

    # NOTE: while SDN controller is not available, its data is simulated
    controller_domain = os.environ.get("SDN_DOMAIN")
    file_name = 'database/topology_'+ str(controller_domain) +'.json'
    with open(file_name) as json_file:
        data = json.load(json_file)
    if data:
        return data, 200
    else:
        data = {'msg':'ERROR loading data'}
        return data, 400

#TODO: returns all connectivity_services
def get_all_connectivity_services():
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass

#TODO: returns specific connectivity services
def get_connectivity_service(cs_ID):
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass

#TODO: sends request to deploy a connectivity service
def instantiate_connectivity_service(cs_json):
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass

#TODO: sends request to terminate a connectivity service
def terminate_connectivity_service():
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass