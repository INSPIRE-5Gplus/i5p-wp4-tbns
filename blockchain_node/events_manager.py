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
        settings.logger.info("TRANSPORT_EVENT_MNGR: NO NEED TO PROCESS THIS EVENT.")

def transport_event_loop(transport_event_filter, poll_interval):
    while True:
        for event in transport_event_filter.get_new_entries():
            handle_transport_event(event)
        
        time.sleep(poll_interval)

def handle_transport_event(event):
    event_json = {}
    if (event['args']['status'] == "NEW" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: EVENT TO CREATE A NEW CS")
        cs_json = json.loads(event['args']['cs_dumps'])
        settings.executor.submit(orch.instantiate_local_connectivity_service, cs_json)
    elif (event['args']['status'] == "READY" and event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
        settings.logger.info("TRANSPORT_EVENT_MNGR: EVENT TO UPDATE A CS")        
        event_json['id'] = event['args']['id']
        event_json['blockchain_owner'] = event['args']['owner']
        event_json['vl_ref'] = event['args']['vl_ref']
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


#TODO: pensar si és realment necessari
def e2e_event_loop(e2e_event_filter, poll_interval):
    while True:
        for event in e2e_event_filter.get_new_entries():
            handle_e2e_event(event)
        
        time.sleep(poll_interval)

def handle_e2e_event(event):
    event_json = {}
    if (event['args']['status'] == "NEW_DOMAIN" and event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
        if (event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
            settings.logger.info("TRANSPORT_EVENT_MNGR: NEW TOPOLOGY EVENT")
            event_json = json.loads(event['args']['context'])
            settings.executor.submit(orch.add_node_e2e_topology, event_json)
    elif (event['args']['status'] == "UPDATE_DOMAIN" and event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
        pass
    elif (event['args']['status'] == "REMOVE_DOMAIN" and event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
        pass
    else:
        # print ("An ERROR has ocurred, a log should be sent to the requester/user.")
        # TODO: exception/error management
        settings.logger.info("E2E_EVENT_MNGR: NO NEED TO PROCESS THIS EVENT.")