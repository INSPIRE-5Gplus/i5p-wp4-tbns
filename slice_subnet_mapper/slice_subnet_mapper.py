#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import settings


#### NETWORK SLICE MANAGER/NFVO URL
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
def get_nsm_url():
    nsm_ip = os.environ.get("NSM_IP")
    nsm_port = os.environ.get("NSM_PORT")
    nfvo_url = "http://"+ str(nsm_ip) +":"+ str(nsm_port) +"/api/v3"
    return nfvo_url

#### REQUESTS
# returns all the slice-subnets templates in the NSM
def get_all_slice_subnet_templates():
    settings.logger.info('SUBNET_MAPPER: Requests all local slice-subnet templates information.')
    url = get_nsm_url() + "/slices"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns a specific slice-subnet template in the NSM
def get_slice_subnet_template(slice_ID):
    settings.logger.info('SUBNET_MAPPER: Requests local slice-subnet template information. ID: ' + str(slice_ID))
    url = get_nsm_url() + "/slices/" + str(slice_ID)
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns all slice-subnet instances in the NSM
def get_all_slice_subnet_instances():
    settings.logger.info('SUBNET_MAPPER: Requests all local slice-subnet instances information.')
    url = get_nsm_url() + "/slice-instances"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# returns specific slice-subnet instance in the NSM
def get_slice_subnet_instance(instance_ID):
    settings.logger.info('SUBNET_MAPPER: Requests local slice-subnet instance information. ID: ' + str(instance_ID))
    url = get_nsm_url() + "/slice-instances/" + str(instance_ID)
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

# sends request to deploy a slice-subnet template (NST) to the NSM
def instantiate_slice_subnet(data_json):
    settings.logger.info("SUBNET_MAPPER: Requests local slice-subnet deployment.")
    data_dumps = json.dumps(data_json)  
    #url = get_nsm_url() + "/requests"
    #response = requests.post(url, headers=JSON_CONTENT_HEADER, data=data_dumps)
    #return response.text, response.status_code
    id_sample = str(uuid.uuid4())
    response = {}
    response['id'] = id_sample
    return response, 200

# returns specific slice-subnet instance request from the NSM/NFVO
def get_slice_subnet_instance_request(request_ID):
    #url = get_nsm_url() + "/requests/" + str(request_ID)
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    settings.logger.info('SUBNET_MAPPER: Requests local slice-subnet instance REQUEST information. ID: ' + str(request_ID))
    sample_json = {}
    sample_json['instance_uuid'] = str(uuid.uuid4())
    sample_json['status'] = "INSTANTIATED"
    time.sleep(10)
    settings.logger.info('SUBNET_MAPPER: THE ANSWER!!!! ' + str(sample_json))
    return sample_json, 200

# sends request to terminate a slice-subnet template (NST) to the NSM
def terminate_slice_subnet(data_json):
    settings.logger.info("SUBNET_MAPPER: Requests local slice-subnet termination.")
    data_dumps = json.dumps(data_json)  
    #url = get_nsm_url() + "/requests"
    #response = requests.post(url, headers=JSON_CONTENT_HEADER, data=data_dumps)
    #return response.text, response.status_code
    id_sample = str(uuid.uuid4())
    response = {}
    response['id'] = id_sample
    return response, 200
