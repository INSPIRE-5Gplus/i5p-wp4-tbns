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
# returns the local context
def get_local_context(sdn_ctrl_ip, sdn_ctrl_port):
    url = "http://"+ str(sdn_ctrl_ip) + ":" + str(sdn_ctrl_port) +"/restconf/data/tapi-common:context"
    response = requests.get(url, headers=JSON_CONTENT_HEADER)
    return response.text, response.status_code

    # NOTE: while SDN controller is not available, its data is simulated
    #controller_domain = os.environ.get("SDN_DOMAIN")
    #file_name = 'database/topology_'+ str(controller_domain) +'.json'
    #with open(file_name) as json_file:
    #    data = json.load(json_file)
    #if data:
    #    return data, 200
    #else:
    #    data = {'msg':'ERROR loading data'}
    #    return data, 400

#TODO: returns all connectivity_services
def get_all_connectivity_services():
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass

# returns specific connectivity services
def get_connectivity_service(cs_ID):
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    sample_json = {}
    sample_json['status'] = "READY"
    #time.sleep(10)
    return sample_json, 200

#sends request to deploy a connectivity service
"""
Incoming CS information
{
    "uuid": "uuid_CS",
    "address_owner": "address_owner",
    "sips": [
        "uuid_sip",
        "uuid_sip"
    ],
    "capacity": {
        "value": 150,
        "unit": "GHz"
    },
    "spectrum_slot": {
        "low-freq": 191700000,
        "high-freq": 196100000
    }
}
Generated CS request
{
  "tapi-connectivity:input": {
    "connectivity-constraint": {
      "connectivity-direction": "UNIDIRECTIONAL",
      "requested-capacity": {
        "total-size": {
          "unit": "GHz",
          "value": 50
        }
      }
    },
    "end-point": [
      {
        "layer-protocol-name": "PHOTONIC_MEDIA",
        "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC",
        "local-id": "291796d9-a492-5837-9ccb-24389339d18a",
        "protection-role": "WORK",
        "role": "UNKNOWN",
        "service-interface-point": {
          "service-interface-point-uuid": "291796d9-a492-5837-9ccb-24389339d18a"
        },
        "tapi-photonic-media:media-channel-connectivity-service-end-point-spec": {
          "mc-config": {
            "spectrum": {
              "frequency-constraint": {
                "adjustment-granularity": "G_6_25GHZ",
                "grid-type": "FLEX"
              },
              "lower-frequency": 193275000,
              "upper-frequency": 193325000
            }
          }
        }
      },
      {
        "layer-protocol-name": "PHOTONIC_MEDIA",
        "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC",
        "local-id": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac",
        "protection-role": "WORK",
        "role": "UNKNOWN",
        "service-interface-point": {
          "service-interface-point-uuid": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac"
        }
      }
    ]
  }
}
"""
def instantiate_connectivity_service(cs_info_json):
    #var with the json to add into the request
    cs_req_json = {}
    tapi_connectivity_cs = []
    cs_item = {}
    cs_item["uuid"] = cs_info_json["uuid"]

    # generating the key_json "connectivity-constraint"
    req_capacity = {}
    connec_constrain = {}
    req_capacity["total-size"] = cs_info_json["capacity"]
    connec_constrain["requested-capacity"] = req_capacity
    connec_constrain["connectivity-direction"] = "UNIDIRECTIONAL"
    cs_item["connectivity-constraint"] = connec_constrain

    # generating the key_json "end-point"
    endpoint_list = []
    for sip_item in cs_info_json["sips"]:
        endpoint_item = {}
        sip = {}
        freq_constraint = {}
        spectrum = {}
        mc_config = {}
        
        endpoint_item["layer-protocol-name"] = "PHOTONIC_MEDIA"
        endpoint_item["layer-protocol-qualifier"] = "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC"
        endpoint_item["local-id"] = sip_item
        endpoint_item["protection-role"] = "WORK"      #NOTE: ask if is is still used
        endpoint_item["role"] = "UNKNOWN"              #NOTE: ask if is is still used

        sip["service-interface-point-uuid"] = sip_item
        endpoint_item["service-interface-point"] = sip

        freq_constraint["adjustment-granularity"] = "G_75GHZ"        #NOTE: inform OLS owner about this granularity
        freq_constraint["grid-type"] = "FLEX"
        spectrum["frequency-constraint"] = freq_constraint
        spectrum["lower-frequency"] = cs_info_json["spectrum_slot"]["low-freq"]
        spectrum["upper-frequency"] = cs_info_json["spectrum_slot"]["high-freq"]
        mc_config["spectrum"] = spectrum
        endpoint_item["tapi-photonic-media:media-channel-connectivity-service-end-point-spec"] = mc_config

        endpoint_list.append(endpoint_item)
    
    cs_item["end-point"] = endpoint_list
    tapi_connectivity_cs.append(cs_item)
    cs_req_json["tapi-connectivity:connectivity-service"] = tapi_connectivity_cs

    # sending request
    #url = "http://10.1.7.80:8182/restconf/config/context/connectivity-service/6e0abcf9-037c-4b0a-b444-fe37a09f46ea/"
    #data_dumps = '{"uuid":"6e0abcf9-037c-4b0a-b444-fe37a09f46ea","end-point":[{"service-interface-point":{"service-interface-point-uuid":"fdd57f63-cc36-5a75-97f8-6968c1a39cac"},"layer-protocol-name":"DSR","layer-protocol-qualifier":"tapi-dsr:DIGITAL_SIGNAL_TYPE_10_GigE_WAN"},{"service-interface-point":{"service-interface-point-uuid":"ff6fefd6-25c3-556a-8337-edda612bfbd6"},"layer-protocol-name":"DSR","layer-protocol-qualifier":"tapi-dsr:DIGITAL_SIGNAL_TYPE_10_GigE_WAN"}],"connectivity-constraint":{"connectivity-direction":"UNIDIRECTIONAL","requested-capacity":{"total-size":{"value":5,"unit":"GBPS"}}}}'
    url = get_nsm_url() + "/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context"
    data_dumps = json.dumps(cs_req_json)
    response = requests.post(url, headers=JSON_CONTENT_HEADER, data=data_dumps)
    """
    if response.status_code == 200:
        #return_json = {}
        #return_json['instance_id'] = "6e0abcf9-037c-4b0a-b444-fe37a09f46ea"
        return_json['status'] = "READY"
    else:
        return response.text, response.status_code
    """
    return response.text, response.status_code

#TODO: sends request to terminate a connectivity service
def terminate_connectivity_service():
    #url = get_nsm_url() #TODO: check the API
    #response = requests.get(url, headers=JSON_CONTENT_HEADER)
    #return response.text, response.status_code
    pass
