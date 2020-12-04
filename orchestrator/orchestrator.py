#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from database import database as db

def share_slice(slice_json):
    db.nsi_db.append(slice_json)
    return 200

def get_all_shared_slice():
    return db.nsi_db

def instantiate_e2e_slice(e2e_slice_json):

    return 200

def terminate_e2e_slice(e2e_slice_json):

    return 200