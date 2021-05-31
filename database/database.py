#!/usr/local/bin/python3.4
import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import settings

# database for Network Slice Instances
nsi_db = []
# database for local Network Slice-subnets requested through the Blockchain system
blockchain_subnets_db = []
# database for the local context (topology + domain CSs), there is only one dict element
context_db = {}
# database for the E2E CS requested, each domain manages its requests locally
e2e_cs_db = [] 

def add_element(db_element, selected_db):
    settings.logger.info("Adding Element into DB %s", selected_db)
    if selected_db == "slices":
        nsi_db.append(db_element)
        settings.logger.info("%s", str(nsi_db))
        return {'msg':'Element added and saved.'}, 200
    elif selected_db == "blockchain_subnets":
        blockchain_subnets_db.append(db_element)
        settings.logger.info("%s", str(blockchain_subnets_db))
        return {'msg':'Element added and saved.'}, 200
    elif selected_db == "context":
        #context_db.append(db_element)
        context_db = db_element
        settings.logger.info("%s", str(context_db))
        return {'msg':'Element added and saved.'}, 200
    elif selected_db == "e2e_cs":
        e2e_cs_db.append(db_element)
        settings.logger.info("%s", str(e2e_cs_db))
        return {'msg':'Element added and saved.'}, 200
    else:
        # TODO:error management
        settings.logger.error("NO DB IS SELECTED")
        return {'msg':'DB not found.'}, 400

def update_db(element_id, db_element, selected_db):
    settings.logger.info("Updating Element in DB %s", selected_db)
    if selected_db == "slices":
        for nsi_element in nsi_db:
            if nsi_element['id'] == element_id:
                nsi_element = db_element
                settings.logger.info("%s", str(nsi_db))
                return {'msg':'Element updated and saved.'}, 200
    elif selected_db == "blockchain_subnets":
        for subnet_element in blockchain_subnets_db:
            if subnet_element['id'] == element_id:
                subnet_element = db_element
                settings.logger.info("%s", str(blockchain_subnets_db))
                return {'msg':'Element updated and saved.'}, 200
    elif selected_db == "context":
        #for context_element in context_db:
            #if context_element['id'] == element_id:
                #context_element = db_element
        context_db = db_element
        settings.logger.info("%s", str(context_db))
        return {'msg':'Element updated and saved.'}, 200
    elif selected_db == "e2e_cs":
        for e2e_cs_element in e2e_cs_db:
            if e2e_cs_element['id'] == element_id:
                e2e_cs_element = db_element
                settings.logger.info("%s", str(e2e_cs_db))
                return {'msg':'Element updated and saved.'}, 200
    else:
        # TODO:error management
        settings.logger.error("NO DB IS SELECTED")
        pass

def remove_element(element_id, selected_db):
    if selected_db == "slices":
        for nsi_element in nsi_db:
            if nsi_element['id'] == element_id:
                nsi_db.remove(nsi_element)
                return {'msg':'Element removed from DB.'}, 200
    elif selected_db == "blockchain_subnets":
        for subnet_element in blockchain_subnets_db:
            if subnet_element['id'] == element_id:
                blockchain_subnets_db.remove(subnet_element)
                return {'msg':'Element removed from DB.'}, 200
    elif selected_db == "context":
        #for context_element in context_db:
            #if context_element['id'] == element_id:
                #context_db.remove(context_element)
        #TODO: check there are not CSs before removing it.
        context_db = {}
        return {'msg':'Element removed from DB.'}, 200
    elif selected_db == "e2e_cs":
        for e2e_cs_element in e2e_cs_db:
            if e2e_cs_element['id'] == element_id:
                e2e_cs_db.remove(e2e_cs_element)
                return {'msg':'Element removed from DB.'}, 200
    else:
        # TODO:error management
        pass

def get_elements(selected_db):
    if selected_db == "slices":
        return nsi_db
    elif selected_db == "blockchain_subnets":
        return blockchain_subnets_db
    elif selected_db == "context":
        return context_db
    elif selected_db == "e2e_cs":
        return e2e_cs_db
    else:
        # TODO:error management
        pass

def get_element(element_id, selected_db):
    if selected_db == "slices":
        for nsi_element in nsi_db:
            if nsi_element['id'] == element_id:
                return nsi_element
    elif selected_db == "blockchain_subnets":
        for subnet_element in blockchain_subnets_db:
            if subnet_element['id'] == element_id:
                return subnet_element
    elif selected_db == "context":
        return context_db       # there is just one context, no need for element_id
    elif selected_db == "e2e_cs":
        for e2e_cs_element in e2e_cs_db:
            if e2e_cs_element['id'] == element_id:
                return e2e_cs_element
    else:
        # TODO:error management
        pass

# add domain_CS info into the context_db
def add_cs(cs_response):
    cs_list = context_db["tapi-common:context"]["tapi-connectivity:connectivity-context"]["connectivity-service"]
    cs_list.append(cs_response)
    context_db["tapi-common:context"]["tapi-connectivity:connectivity-context"]["connectivity-service"] = cs_list
    pass