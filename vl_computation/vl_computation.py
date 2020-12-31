#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import networkx as nx

from config_files import settings

collaborative_topology_graph = nx.Graph()

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
    collaborative_topology_graph.add_node(node_item)

    ports_list = domain_json['topology']['ports']
    for port_item in ports_list:
        parts = port_item['destination'].split(":")
        collaborative_topology_graph.add_node(parts[0])
        collaborative_topology_graph.add_edge(node_item,parts[0])
    
    settings.logger.info("VL_COMP: Nodes: " +str(list(collaborative_topology_graph.nodes)))
    settings.logger.info("VL_COMP: Edges: " +str(list(collaborative_topology_graph.edges)))

# TODO: updates the graph with an external blockchain domain
def update_graph(new_domain_json):
    pass

# TODO: computes the path between two compute domains
def find_path():
    pass