#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from orchestrator import orchestrator as orch
from database import database as db
from config_files import settings

def slice_event_loop(slice_event_filter, poll_interval):
    while True:
        settings.logger.info("SLICE_EVENT_MNGR: WAITING FOR SLICING EVENTS")
        for event in slice_event_filter.get_new_entries():
            if (event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
                handle_sliceInstance_event(event)
        time.sleep(poll_interval)

def handle_sliceInstance_event(event):
    event_json = {}
    settings.logger.info("SLICE_EVENT_MNGR: A NEW EVENT ARRIVED: " +str(event))
    if (event['args']['status'] == "INSTANTIATING"):
        settings.logger.info("SLICE_EVENT_MNGR: INSTANTIATING EVENT")
        event_json['nst_ref'] = event['args']['templateId']
        event_json["id"] = event['args']['instanceId']
        event_json["status"] = event['args']['status']
        settings.executor.submit(orch.instantiate_local_slicesubnet, event_json)
    elif (event['args']['status'] == "INSTANTIATED"):
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
        pass

def transport_event_loop(transport_event_filter, poll_interval):
    while True:
        settings.logger.info("TRASPORT_EVENT_MNGR: WAITING FOR TRANSPORT EVENTS")
        for event in transport_event_filter.get_new_entries():
            handle_transport_event(event)
        
        time.sleep(poll_interval)

def handle_transport_event(event):
    event_json = {}
    settings.logger.info("TRANSPORT_EVENT_MNGR: A NEW EVENT ARRIVED: " +str(event))
    if (event['args']['status'] == "NEW_DOMAIN"):
        if (event['args']['owner'] != str(settings.web3.eth.defaultAccount)):
            settings.logger.info("TRANSPORT_EVENT_MNGR: NEW TOPOLOGY EVENT")
            event_json['domain_id'] = event['args']['domain_id']
            event_json["topology"] = json.loads(event['args']['topology'])
            settings.executor.submit(orch.add_node_collaborative_topology, event_json)
    elif (event['args']['status'] == "UPDATED_DOMAIN"):
        settings.logger.info("TRANSPORT_EVENT_MNGR: UPDATE TOPOLOGY EVENT")
        pass
    else:
        pass
