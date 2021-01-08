#!/usr/local/bin/python3.4
import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import settings

#temporary database for Network Slice Instances
nsi_db = []
# temporary database for local Network Slice-subnets requested through the Blockchain system
blockchain_subnets_db = []
#temporary database for connectivity services
cs_db = []

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
    elif selected_db == "conn_services":
        cs_db.append(db_element)
        settings.logger.info("%s", str(cs_db))
        return {'msg':'Element added and saved.'}, 200
    else:
        # TODO:error management
        settings.logger.error("NO DB IS SELECTED")
        pass

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
    elif selected_db == "conn_services":
        for cs_element in cs_db:
            if cs_element['id'] == element_id:
                cs_element = db_element
                settings.logger.info("%s", str(cs_db))
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
    elif selected_db == "conn_services":
        for cs_element in cs_db:
            if cs_element['id'] == element_id:
                cs_db.remove(cs_element)
                return {'msg':'Element removed from DB.'}, 200
    else:
        # TODO:error management
        pass

def get_elements(selected_db):
    if selected_db == "slices":
        return nsi_db
    elif selected_db == "blockchain_subnets":
        return blockchain_subnets_db
    elif selected_db == "conn_services":
        return cs_db
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
    elif selected_db == "conn_services":
        for cs_element in cs_db:
            if cs_element['id'] == element_id:
                return cs_element
    else:
        # TODO:error management
        pass