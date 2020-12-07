#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid


#### NETWORK SLICE MANAGER/NFVO URL
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
def get_nsm_url():
    nsm_ip = os.environ.get("NSM_IP")
    nsm_port = os.environ.get("NSM_PORT")
    print(nsm_ip)
    print(nsm_port)
    nfvo_url = "http://"+ str(nsm_ip) +":"+ str(nsm_port) +"/api/v3"
    print(nfvo_url)
    
    return nfvo_url


#### REQUESTS
def get_all_slice():
    url = get_nsm_url() + "/slices"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    print(str(response.text))
    return response.text, response.status_code

def get_slice(slice_ID):
    url = get_nsm_url() + "/slices/" + str(slice_ID)
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    print(str(response.text))
    return response.text, response.status_code