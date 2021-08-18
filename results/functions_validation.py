import math, sys, threading, time, requests, random
from time import sleep
from dataclasses import dataclass



endpointsD2 = {'available':[
            {'context_uuid': 'Hola', 'nep_uuid': '', 'sip_uuid': ''},
            {'context_uuid': 'adeu', 'nep_uuid': '', 'sip_uuid': ''},
            {'context_uuid': 'ciao', 'nep_uuid': '', 'sip_uuid': ''}],
            'occupied': []}


endpoint = random.choice(endpointsD2['available'])
print(endpoint)
print(endpoint['context_uuid'])