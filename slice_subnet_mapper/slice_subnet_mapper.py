#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

nsm_ip = str(os.environ.get("NSM_IP"))
nsm_port = str(os.environ.get("NSM_PORT"))
nfvo_url = "http://"+ nsm_ip +":"+ nsm_port +"/api/v3"
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}

def get_all_slice():
    url = nfvo_url + "slices"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, 200

def get_slice(slice_ID):
    return 200