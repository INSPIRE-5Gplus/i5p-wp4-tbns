#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from orchestrator import orchestrator as orch
from database import database as db
from config_files import settings

def event_loop(event_filter, poll_interval):
    while True:
        settings.logger.info("EVENT_MNGR: WAITING FOR EVENTS")
        for event in event_filter.get_new_entries():
            if (event['args']['owner'] == str(settings.web3.eth.defaultAccount)):
                handle_sliceInstance_event(event)
        time.sleep(poll_interval)

def handle_sliceInstance_event(event):
    event_json = {}
    settings.logger.info("EVENT_MNGR: A NEW EVENT ARRIVED: " +str(event))
    if (event['args']['status'] == "INSTANTIATING"):
        settings.logger.info("EVENT_MNGR: INSTANTIATING EVENT")
        event_json['nst_ref'] = event['args']['templateId']
        event_json["id"] = event['args']['instanceId']
        event_json["status"] = event['args']['status']
        settings.executor.submit(orch.instantiate_local_slicesubnet, event_json)
    elif (event['args']['status'] == "INSTANTIATED"):
        settings.logger.info("EVENT_MNGR: INSTANTIATED EVENT")
        event_json['instanceId'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.update_slicesubnet_from_blockchain, event_json)
    elif (event['args']['status'] == "TERMINATING"):
        settings.logger.info("EVENT_MNGR: TERMINATING EVENT")
        event_json['id'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.terminate_local_slicesubnet, event_json)
    elif (event['args']['status'] == "TERMINATED"):
        settings.logger.info("EVENT_MNGR: TERMINATED EVENT")
        event_json['instanceId'] = event['args']['instanceId']
        event_json['status'] = event['args']['status']
        settings.executor.submit(orch.update_slicesubnet_from_blockchain, event_json)
    else:
        # print ("An ERROR has ocurred, a log should be sent to the requester/user.")
        # TODO: exception/error management
        pass