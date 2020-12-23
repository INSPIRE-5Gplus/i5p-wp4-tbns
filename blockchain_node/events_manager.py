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
        '''
        #NOTE: Move one space back
        elif (event['args']['status'] == "TERMINATING"):
            print("Calling the termination procedure.")
            mutex_slice2blockchaindb_access.acquire()
            for bl_slice_subnet_item in bl_slice_subnets_db:
                if bl_slice_subnet_item['id'] ==  event['args']['instanceId']:

                    #LOCAL TERMINATION PROCESS IS CALLED
                    print("#################### LOCAL REQUEST SENT: ", time.time())
                    data_json = {}
                    data_json['instance_uuid'] = bl_slice_subnet_item['instance_uuid']
                    data_json['request_type'] = 'TERMINATE_SLICE'
                    data_dumps = json.dumps(data_json)
                    url = url_nfvo + "/requests"
                    response = requests.post(url, data=data_dumps, headers=JSON_CONTENT_HEADER)
                    jsonresponse = json.loads(response.text)
                    print("#################### LOCAL REQUEST ACCEPTED: ", time.time())

                    bl_slice_subnet_item["request_id"] = jsonresponse['id']
                    bl_slice_subnet_item["status"] = "TERMINATING"
                    bl_slice_subnet_item["log"] = "Terminating Blockchain Slice Subnet Instance"
                    break
            mutex_slice2blockchaindb_access.release()
        elif (event['args']['status'] == "TERMINATED"):
            # look in the local nsi db which nsi has the updated slice subnet
            mutex_slice2db_access.acquire()
            found_nsi = False
            for nsi_item in nsi_db2:
                for slice_subnet_item in nsi_item["slice_subnets"]:
                    if slice_subnet_item["id"] == event['args']['instanceId']:
                        slice_subnet_item["status"] =  event['args']['status']
                        slice_subnet_item["log"] = "Slice Subnet Instance from another domain TERMINATED."
                        found_nsi_id = nsi_item["id"]
                        found_nsi = True
                        break
                if found_nsi:
                    break
            mutex_slice2db_access.release()
        '''
    else:
        # print ("An ERROR has ocurred, a log should be sent to the requester/user.")
        # TODO: exception/error management
        pass