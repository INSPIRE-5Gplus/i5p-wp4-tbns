#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import networkx as nx

from config_files import settings

# NOTE: e2e_topology is the sum of all SDN topologies to create the E2E topology of the network
e2e_topology = nx.Graph()

'''
    {
        "domain_id": "Core",
        "topology":{
            "node_name": "Core",
            "ports":[
                {
                    "port_id":"Core:1",
                    "destination": "Packet:2"
                },
                {
                    "port_id":"Core:2",
                    "destination": "Optical:2"
                }
            ]
        },
        "cs_list":[]
    }
'''
# adds the local context in the graph
def add_node(domain_json):
    node_item = domain_json['topology']['node_name']
    e2e_topology.add_node(node_item)

    ports_list = domain_json['topology']['ports']
    for port_item in ports_list:
        parts = port_item['destination'].split(":")
        e2e_topology.add_node(parts[0])
        e2e_topology.add_edge(node_item,parts[0])

# TODO: updates the e2e topology
def update_graph(new_domain_json):
    pass

# TODO: computes the path between two compute domains
def find_path(source, destination):
    src = source.split(":")
    dst = destination.split(":")

    path_nodes_list = nx.shortest_path(e2e_topology, src[0], dst[0])
    return path_nodes_list

