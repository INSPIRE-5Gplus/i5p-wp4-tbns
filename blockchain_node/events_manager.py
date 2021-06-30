#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from orchestrator import orchestrator as orch
from database import database as db
from config_files import settings

def slice_event_loop(slice_event_filter, poll_interval):
    while True:
        for event in slice_event_filter.get_new_entries():
            if (event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
                handle_sliceInstance_event(event)
        time.sleep(poll_interval)

def handle_sliceInstance_event(event):
    event_json = {}
    if (event['args']['status'] == "INSTANTIATING"):
        settings.logger.info('SLICE_EVENT_MNGR: Received Blockchain event (TIME 3): ' + str(time.time_ns()))
        settings.logger.info("SLICE_EVENT_MNGR: INSTANTIATING EVENT")
        event_json['nst_ref'] = event['args']['templateId']
        event_json["id"] = event['args']['instanceId']
        event_json["status"] = event['args']['status']
        settings.executor.submit(orch.instantiate_local_slicesubnet, event_json)
    elif (event['args']['status'] == "INSTANTIATED"):
        settings.logger.info('SLICE_EVENT_MNGR: Received Blockchain event (TIME 3): ' + str(time.time_ns()))
        settings.logger.info("SLICE_EVENT_MNGR: INSTANTIATED EVENT")
        event_json['instanceId'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.update_slicesubnet_from_blockchain, event_json)
    elif (event['args']['status'] == "TERMINATING"):
        settings.logger.info("SLICE_EVENT_MNGR: TERMINATING EVENT")
        event_json['id'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.terminate_local_slicesubnet, event_json)
    elif (event['args']['status'] == "TERMINATED"):
        settings.logger.info("SLICE_EVENT_MNGR: TERMINATED EVENT")
        event_json['instanceId'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.update_slicesubnet_from_blockchain, event_json)
    else:
        # print ("An ERROR has ocurred, a log should be sent to the requester/user.")
        # TODO: exception/error management
        settings.logger.info("SLICE_EVENT_MNGR: NO NEED TO PROCESS THIS EVENT.")

def transport_event_loop(transport_event_filter, poll_interval):
    while True:
        for event in transport_event_filter.get_new_entries():
            handle_transport_event(event)
        time.sleep(poll_interval)

def handle_transport_event(event):
    event_json = {}
    if (event['args']['status'] == "NEW_IDL" and event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: NEW SET OF IDL")
        event_json = json.loads(event['args']['sdn_info'])
        settings.executor.submit(orch.add_idl_info, event_json)
    elif (event['args']['status'] == "NEW_DOMAIN" and event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: NEW TOPOLOGY EVENT")
        context_json = {}
        context_json["uuid"] =  event['args']['id']
        context_json["name_context"] =  event['args']['name_context']
        context_json["sip"] =  event['args']['sip']
        context_json["nw_topo_serv"] =  event['args']['nw_topo_serv']
        context_json["topo_metadata"] =  event['args']['topo_metadata']
        context_json["node_topo"] =  event['args']['inode_topod']
        context_json["link_topo"] =  event['args']['link_topo']
        
        settings.executor.submit(orch.add_context_info, context_json)
    elif (event['args']['status'] == "NEW" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: EVENT TO CREATE A NEW CS")
        cs_json = json.loads(event['args']['cs_dumps'])
        settings.executor.submit(orch.instantiate_local_connectivity_service, cs_json)
    elif (event['args']['status'] == "READY" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: EVENT TO UPDATE A CS")        
        event_json['id'] = event['args']['id']
        event_json['blockchain_owner'] = event['args']['owner']
        event_json['cs_info'] = event['args']['sdn_info']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.update_connectivity_service_from_blockchain, event_json)
    elif (event['args']['status'] == "REMOVE" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        pass
    elif (event['args']['status'] == "REMOVED" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        pass
    else:
        # print ("An ERROR has ocurred, a log should be sent to the requester/user.")
        # TODO: exception/error management
        settings.logger.info("TRANSPORT_EVENT_MNGR: NO NEED TO PROCESS THIS EVENT.")