#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid


#### NETWORK SLICE MANAGER/NFVO URL
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
def get_nsm_url():
    nsm_ip = os.environ.get("SDN_CONTROLLER_IP")
    nsm_port = os.environ.get("SDN_CONTROLLER_PORT")
    nfvo_url = "http://"+ str(nsm_ip) +":"+ str(nsm_port)  #TODO: check the API
    return nfvo_url


#### REQUESTS
# returns all the contexts
def get_all_contexts():
    url = get_nsm_url() #TODO: check the API
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns a specific context
def get_context(context_ID):
    url = get_nsm_url() #TODO: check the API
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

#TODO: returns all connectivity_services
def get_all_connectivity_services():
    
    return 200

#TODO: returns specific connectivity services
def get_connectivity_service(cs_ID):
    
    return 200

#TODO: sends request to deploy a connectivity service
def instantiate_connectivity_service():
    return 200

#TODO: sends request to terminate a connectivity service
def terminate_connectivity_service():
    return 200