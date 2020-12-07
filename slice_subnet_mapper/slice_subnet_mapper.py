#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid


#### NETWORK SLICE MANAGER/NFVO URL
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
def get_nsm_url():
    nsm_ip = os.environ.get("NSM_IP")
    nsm_port = os.environ.get("NSM_PORT")
    nfvo_url = "http://"+ str(nsm_ip) +":"+ str(nsm_port) +"/api/v3"
    return nfvo_url


#### REQUESTS
# returns all the slice templates in the NSM
def get_all_slice_templates():
    url = get_nsm_url() + "/slices"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns a specific slice template in the NSM
def get_slice_template(slice_ID):
    url = get_nsm_url() + "/slices/" + str(slice_ID)
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns all instances information in the NSM
def get_all_slice_instances():
    url = get_nsm_url() + "/slice-instances"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns specific instance information in the NSM
def get_slice_instance(instance_ID):
    url = get_nsm_url() + "/slice-instances/" + str(instance_ID)
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# sends request to deploy a NST to the NSM
def instantiate_slice(slice_data):
    # slice_data = {"instance_uuid": slice_template_uuid, "request_type": "CREATE_SLICE"}
    url = get_nsm_url() + "/requests"
    response = requests.post(url, headers=JSON_CONTENT_HEADER, data=slice_data)
    return response.text, response.status_code

# sends request to terminate a NST to the NSM
def terminate_slice(slice_data):
    # slice_data = {"instance_uuid": instance_uuid, "request_type": "TERMINATE_SLICE"}
    url = get_nsm_url() + "/requests"
    response = requests.post(url, headers=JSON_CONTENT_HEADER, data=slice_data)
    return response.text, response.status_code
    return 200