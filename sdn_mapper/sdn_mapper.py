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
cs_info_json = {
  "uuid": "uuid_CS",
  "context-uuid" : "uuid,
  "address-owner": "blockchain-peer_address",
  "status": "INSTANTIATING/DEPLOYED/TERMINATED",
  "sip-source": "sip_uuid",
  "sip-destination": "sip_uuid",
  "internal-links":[
    "link_uuid",
    "link_uuid"
  ]
},
spectrum = {
  "lower-frequency": 191700000,
  "upper-frequency": 106100000
},
capacity = {
  "value": 75,
  "unit": "GHz"
},
Generated CS request
{
  "tapi-connectivity:connectivity-service": [
    {
      "uuid": "650a02db-4bf2-4ff0-a477-a589fca170a2",
      "connectivity-constraint": {
        "requested-capacity": {
          "total-size": {
            "value": 50,
            "unit": "GHz"
          }
        },
        "connectivity-direction": "UNIDIRECTIONAL"
      },
      "end-point": [
        {
          "service-interface-point": {
            "service-interface-point-uuid": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb"
          },
          "layer-protocol-name": "PHOTONIC_MEDIA",
          "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC",
          "local-id": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb",
          "tapi-photonic-media:media-channel-connectivity-service-end-point-spec": {
            "mc-config": {
              "spectrum": {
                "frequency-constraint": {
                  "adjustment-granularity": "G_6_25GHZ",
                  "grid-type": "FLEX"
                },
                "lower-frequency": 191775000,
                "upper-frequency": 191825000
              }
            }
          }
        },
        {
          "service-interface-point": {
            "service-interface-point-uuid": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"
          },
          "layer-protocol-name": "PHOTONIC_MEDIA",
          "layer-protocol-qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC",
          "local-id": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"
        }
      ],
      "include-link": [
          "40de8a74-ab17-5880-aefe-2482b48c4ece",
          "bec726c9-9d6f-5047-a3f6-47d53a52fcf9",
          "8ddcc1a9-2286-5486-876e-0c6e2317557a"
      ]
    }
  ]
}
"""
# assegurar que el json a enviar és el que comença amb "tapi-connectivity:input"
def instantiate_connectivity_service(cs_info_json, spectrum, capacity):
  settings.logger.info("SDN_MAPPER: Arrived a requests to deploy a local CS.")
  settings.logger.info("SDN_MAPPER: CS information: " + str(cs_info_json) + " / Capacity: " + str(capacity) + "/ Spectrum: " + str(spectrum))
  # JSON creation for the request.
  request_json = {}
  tapi_cs_list = []
  cs_json = {}
  con_constraint = {}
  req_capacity = {}
  endpoint = []

  cs_json["uuid"] = cs_info_json["uuid"]

  total_size = capacity
  req_capacity["total-size"] = total_size
  con_constraint["requested-capacity"] = req_capacity
  con_constraint["connectivity-direction"] = "UNIDIRECTIONAL"
  cs_json["connectivity-constraint"] = con_constraint

  endpoint_item = {}
  sip_uuid = {}
  sip_uuid["service-interface-point-uuid"] = cs_info_json["sip-source"]
  endpoint_item["service-interface-point"] = sip_uuid
  endpoint_item["layer-protocol-name"]  = "PHOTONIC_MEDIA"
  endpoint_item["layer-protocol-qualifier"] = "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC"
  endpoint_item["local-id"] = cs_info_json["sip-source"]
  freq_const = {}
  freq_const["adjustment-granularity"] = "G_6_25GHZ"
  freq_const["grid-type"] = "FLEX"
  spec = {}
  spec["frequency-constraint"] = freq_const
  spec["lower-frequency"] = spectrum["lower-frequency"]
  spec["upper-frequency"] = spectrum["upper-frequency"]
  mc_config = {}
  mc_config["spectrum"] = spec
  tpmmccsps = {}
  tpmmccsps["mc-config"] = mc_config
  endpoint_item["tapi-photonic-media:media-channel-connectivity-service-end-point-spec"] = tpmmccsps
  endpoint.append(endpoint_item)

  endpoint_item = {}
  sip_uuid = {}
  sip_uuid["service-interface-point-uuid"] = cs_info_json["sip-destination"]
  endpoint_item["service-interface-point"] = sip_uuid
  endpoint_item["layer-protocol-name"]  ="PHOTONIC_MEDIA"
  endpoint_item["layer-protocol-qualifier"] = "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC"
  endpoint_item["local-id"] = cs_info_json["sip-destination"]
  endpoint.append(endpoint_item)
  cs_json["end-point"] = endpoint

  if os.environ.get("ABSTRACION_MODEL") == "transparent":
    cs_json["include-link"] = cs_info_json["internal-links"]
  else:
    cs_json["include-link"] = []

  tapi_cs_list.append(cs_json)
  request_json["tapi-connectivity:connectivity-service"] = tapi_cs_list
  print(str(request_json))
   
  """
  # sending request
  url = get_nsm_url() + "/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context"
  data_dumps = json.dumps(request_json)
  response = requests.post(url, headers=JSON_CONTENT_HEADER, data=data_dumps)
  settings.logger.info("SDN_MAPPER: CS deployment request: " + str(data_dumps))
  
  if response.status_code == 201:
    cs_info_json["status"] = "DEPLOYED"
    return cs_info_json, 200
  else:
    return {"msg": "ERROR requesting CS to the SDN Controller."}, response.status_code
  """
  time.sleep(0.25)
  cs_info_json["status"] = "DEPLOYED"
  return cs_info_json, 200

# sends request to terminate a connectivity service
def terminate_connectivity_service(cs_uuid):
  settings.logger.info("SDN_MAPPER: Arrived a requests to terminate a local CS: " + str(cs_uuid))
  """
  # sending request
  url = get_nsm_url() + "/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service="+str(cs_uuid)
  response = requests.delete(url)
  settings.logger.info("SDN_MAPPER: CS deployment request:")

  if response.status_code == 204:
    cs_info_json = {}
    cs_info_json["status"] = "TERMINATED"
    return cs_info_json, 200
  else:
    return {"msg": "ERROR requesting CS to the SDN Controller."}, response.status_code
  """
  time.sleep(0.25)
  cs_info_json = {}
  cs_info_json["status"] = "TERMINATED"
  return cs_info_json, 200
