import math, sys, threading, time, requests, random, uuid, json
from time import sleep
from dataclasses import dataclass
from threading import Lock

mutex_endpoints = Lock()

@dataclass
class ConnectivityServiceData:
    start_TS: int = -1
    inter_arrival_time: float = -0.1
    end_TS: int = -1
    type: str = ''
    result: str = ''
    uuid: str = ''
    ber: bool = True

def millis():
    return int(round(time.time() * 1000))

def poisson_wait_time(lmb):
    p = random.random()

    inter_arrival_time = -math.log(1.0 - p) / lmb
    # print('inter_arrival_time: {}'.format(inter_arrival_time))
    return inter_arrival_time

class Connectivity:
    def __init__(self, lmb, connections):
        self.log = []
        self.start_time = -1
        self.end_time = -1
        self.total_holding_time = 0 # no l'entenc. borrar
        
        #list of available NEP/SIPs in the other domains
        self.endpoints = {
            'available_output':[
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "79516f5e-55a0-5671-977a-1f5cc934e700"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "0d29c715-fa35-5eaf-8be8-20cc73d8a4e6"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "fbdd154e-659e-54df-8d75-23575711978b"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "68ac012e-54d4-5846-b5dc-6ec356404f90"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "a6e6da0a-c2ea-5a2e-b901-fcac4abed95a"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "79516f5e-55a0-5671-977a-1f5cc934e700"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "0d29c715-fa35-5eaf-8be8-20cc73d8a4e6"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "fbdd154e-659e-54df-8d75-23575711978b"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "42d64587-8763-5917-bbd6-8f6a8b8d2700"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "9f65970c-24ae-5e17-b86e-d5cf25df589e"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "7e9dc6c7-63d5-5709-aaec-e1dcf243b22b"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "5e34d63c-b23f-5fbb-909e-5c6ed6b13f4f"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "b2c55979-0f9b-52e3-a767-deedebe12547"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "9ce4373d-acca-5edd-b5b0-533057776a2f"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "df71fece-6979-5f50-88cb-a88e94dc684e"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "d7ee402b-7f9e-5468-86ec-113c5ec22707"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "223421ea-579e-5020-9924-0027c91e12a2"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "71941e6f-0f69-53d4-820e-f4efc5d3364b"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "f15278a8-8d93-5594-af08-18e9c4104af8"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "68ac012e-54d4-5846-b5dc-6ec356404f90"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "a6e6da0a-c2ea-5a2e-b901-fcac4abed95a"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "367b19b1-3172-54d8-bdd4-12d3ac5604f6"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "84e9eef3-11c2-5710-89f1-bf355cacb7c3"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "f1737854-81ef-5a98-9a27-0ae89619ba1e"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "a53e9d1e-8045-591a-8ed8-8b8164ae9d6b"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "79516f5e-55a0-5671-977a-1f5cc934e700"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "0d29c715-fa35-5eaf-8be8-20cc73d8a4e6"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "68ac012e-54d4-5846-b5dc-6ec356404f90"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "a6e6da0a-c2ea-5a2e-b901-fcac4abed95a"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "79516f5e-55a0-5671-977a-1f5cc934e700"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "0d29c715-fa35-5eaf-8be8-20cc73d8a4e6"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "30d9323e-b916-51ce-a9a8-cf88f62eb77f"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "b10c4b7d-1c2f-5f25-a239-de4daaa622ac"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "68ac012e-54d4-5846-b5dc-6ec356404f90"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "a6e6da0a-c2ea-5a2e-b901-fcac4abed95a"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "bd512c4b-834e-5551-bbc5-0f6de0f262db"}
            ],
            'available_input':[
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "aade6001-f00b-5e2f-a357-6a0a9d3de870"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "291796d9-a492-5837-9ccb-24389339d18a"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "eb287d83-f05e-53ec-ab5a-adf6bd2b5418"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "9180bfbf-9ad7-5145-8bb8-9fd8d6b2db9a"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "0ef74f99-1acc-57bd-ab9d-4b958b06c513"},
                {"context_uuid": "0bd7908e-c22b-574d-8bba-396d060e2611", "node_uuid":"0bd7908e-c22b-574d-8bba-396d060e2611", "sip_uuid": "92bc2016-ae6d-530d-ba08-b2637c3eabce"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "aade6001-f00b-5e2f-a357-6a0a9d3de870"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "291796d9-a492-5837-9ccb-24389339d18a"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "b1655446-a3e1-5077-8006-0277028b9179"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "5b139e0a-a967-5acf-be83-617c8586840f"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "00672024-10f1-5dbe-95a6-265d60889a86"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "f9dc5177-f923-5873-a8eb-c40a8b90312a"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "e258f1cf-b870-5edf-bd6f-cbe86989bdcd"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "e21b5b3e-5bd4-567c-b819-f5e6ac689c68"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "9853c355-5d3a-5f46-b4bd-e94de00e902f"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "eb287d83-f05e-53ec-ab5a-adf6bd2b5418"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "9180bfbf-9ad7-5145-8bb8-9fd8d6b2db9a"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "1b7dbfae-2ef5-5d7c-b4ff-be8fba395f6d"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "e9f2cd83-622f-5693-a3ea-edda0238f675"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "fc7d3da3-31c2-5f7a-868c-fe824919a2e4"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "edb7c0b6-0a87-5ecd-84a2-0fb5ed015550"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "0ef74f99-1acc-57bd-ab9d-4b958b06c513"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "92bc2016-ae6d-530d-ba08-b2637c3eabce"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "50296d99-58cc-5ce7-82f5-fc8ee4eec2ec"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "0e047118-5aee-5721-979e-2fece9b45fb2"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "589c2048-0b7f-59c7-b893-514949faea32"},
                {"context_uuid": "226b9166-974e-57ff-821d-2f24e5a71b00", "node_uuid":"226b9166-974e-57ff-821d-2f24e5a71b00", "sip_uuid": "075a2ea8-c642-5b8b-9d32-8f97218af55c"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "aade6001-f00b-5e2f-a357-6a0a9d3de870"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "eb287d83-f05e-53ec-ab5a-adf6bd2b5418"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "9180bfbf-9ad7-5145-8bb8-9fd8d6b2db9a"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "0ef74f99-1acc-57bd-ab9d-4b958b06c513"},
                {"context_uuid": "3d89bd76-e54d-5fab-9787-eb609f291ee0", "node_uuid":"3d89bd76-e54d-5fab-9787-eb609f291ee0", "sip_uuid": "92bc2016-ae6d-530d-ba08-b2637c3eabce"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "aade6001-f00b-5e2f-a357-6a0a9d3de870"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "a9b6a9a3-99c5-5b37-bc83-d087abf94ceb"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "eb287d83-f05e-53ec-ab5a-adf6bd2b5418"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "9180bfbf-9ad7-5145-8bb8-9fd8d6b2db9a"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "0ef74f99-1acc-57bd-ab9d-4b958b06c513"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "92bc2016-ae6d-530d-ba08-b2637c3eabce"},
                {"context_uuid": "627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "node_uuid":"627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3", "sip_uuid": "ce525139-c58a-5ee7-a527-94e344d8fa5e"}
            ],
            'occupied_output': [], #[{"cs_uuid": "uuid", "endpoint_info": {}}]
            'occupied_input': [] #[{"cs_uuid": "uuid", "endpoint_info": {}}]
            
        }
        print("Available source SIPs: " + str(len(self.endpoints["available_output"])))
        print("Available destination SIPs: " + str(len(self.endpoints["available_input"])))
        print("Occupied source SIPs: " + str(len(self.endpoints["occupied_output"])))
        print("Occupied destination SIPs: " + str(len(self.endpoints["occupied_input"])))

        # context and port relationship (domain)
        self.ports = [
            {
                'context_uuid':'0bd7908e-c22b-574d-8bba-396d060e2611',
                'port_domain': '4441'
            },
            {
                'context_uuid':'226b9166-974e-57ff-821d-2f24e5a71b00',
                'port_domain': '4442'
            },
            {
                'context_uuid':'3d89bd76-e54d-5fab-9787-eb609f291ee0',
                'port_domain': '4443'
            },
            {
                'context_uuid':'627ea8a3-f3cf-578b-b0dd-9e65a5a0e0a3',
                'port_domain': '4444'
            }
        ]

        self.max_connections = connections
        self.watcher_thread = threading.Thread(target=self.watcher_function, args=(lmb,))
        self.first_conn = None
        self.n_threads = 0
        self.connection_no_ber = 0
    
    def start(self):
        print('Starting watcher')
        self.watcher_thread.start()
    
    def watcher_function(self, lmb):
        n_connections = 0
        self.start_time = millis()
        while n_connections < self.max_connections:
            s_next = poisson_wait_time(lmb)
            print("Wait " + str(s_next) + "seconds for the next E2E CS request.")
            time.sleep(s_next)
            print("Connection Nº: " +str(n_connections))
            connection = ConnectivityServiceData(inter_arrival_time=s_next)
            next_thread = threading.Thread(target=self.connectivity, args=(connection, ))
            next_thread.start()
            n_connections = n_connections + 1
        self.exit_function()
    
    def connectivity(self, connection):
        connection.type = 'CREATE'
        connection.start_TS = millis()
        self.n_threads = self.n_threads + 1
        
        try:
            cs_uuid = str(uuid.uuid4())
            print("NEW E2E CS with ID: " + str(cs_uuid))
            #print(str(self.endpoints['occupied_output']))
            #print(str(self.endpoints['occupied_input']))
            
            mutex_endpoints.acquire()
            src = random.choice(self.endpoints['available_output'])
            dst = random.choice(self.endpoints['available_input'])

            while dst["context_uuid"] == src["context_uuid"]:
                dst = random.choice(self.endpoints['available_input'])
            print(str(src))
            print(str(dst))
            
            for idx, endpoint_item in enumerate(self.endpoints['available_output']):
                if endpoint_item['sip_uuid'] == src['sip_uuid']:
                    src_idx = idx
                    break
            del self.endpoints['available_output'][src_idx]
            
            for idx, endpoint_item in enumerate(self.endpoints['available_input']):
                if endpoint_item['sip_uuid'] == dst['sip_uuid']:
                    dst_idx = idx
                    break
            del self.endpoints['available_input'][dst_idx]

            src_json = {}
            src_json["cs_uuid"] = cs_uuid
            src_json["endpoint_info"] = src
            #print("SRC: " + str(cs_json))
            self.endpoints['occupied_output'].append(src_json)
            dst_json = {}
            dst_json["cs_uuid"] = cs_uuid
            dst_json["endpoint_info"] = dst
            #print("DST: "+ str(cs_json))
            self.endpoints['occupied_input'].append(dst_json)
            mutex_endpoints.release()

            # select port based on the src context.
            for port_item in self.ports:
                if port_item["context_uuid"] == src["context_uuid"]:
                    selected_port = port_item["port_domain"]
        
        except IndexError:
            #cs_uuid, endpoint = 'cs_error', ['a', 'b']
            cs_uuid = 'cs_error'
            endpoint_src = {'context_uuid': 'a', 'nep_uuid': 'b', 'sip_uuid': 'c'}
            endpoint_dst = {'context_uuid': 'c', 'nep_uuid': 'd', 'sip_uuid': 'e'}
            print('No SIPs available: {}'.format(cs_uuid))

        #print(str(self.endpoints['occupied_output']))
        #print(str(self.endpoints['occupied_input']))
        #print(str(src))
        #print(str(dst))
        print("Available source SIPs: " + str(len(self.endpoints["available_output"])))
        print("Available destination SIPs: " + str(len(self.endpoints["available_input"])))
        print("Occupied source SIPs: " + str(len(self.endpoints["occupied_output"])))
        print("Occupied destination SIPs: " + str(len(self.endpoints["occupied_input"])))
        connection.uuid = cs_uuid
        capacity = random.choice([75, 150, 225, 300, 375, 450, 525, 600])

        #url = "http://" + ip + "/restconf/config/context/connectivity-service/" + cs_uuid
        url = "http://" + ip + selected_port +  "/pdl-transport/connectivity_service"
        print("Selected port domain (last number = domain): " + str(selected_port))
        
        # print(url)
        print('SEND cs: {}'.format(cs_uuid))
        #response = requests.post(url, json={"uuid": cs_uuid, "src": src, "dst": dst, "capacity": capacity})
        cs_json = {"cs_uuid": cs_uuid,"source": src, "destination": dst, "capacity": {"value": capacity,"unit": "GHz"}}
        print('CS JSON Request: ' + str(cs_json))
        #print("URL: " + str(url))
        response = requests.post(url, json=cs_json)
        print("POST response: "+str(response.text) + "with status: " + str(response.status_code))
        if response.status_code != 200:
            response_json = json.loads(response.text)
            print('Error cs: {} -> {}'.format(cs_uuid, response_json['msg']))
            connection.result = response_json['msg']
            self.log.append(connection)
            mutex_endpoints.acquire()
            for idx, occupied_item in enumerate(self.endpoints['occupied_output']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    del self.endpoints['occupied_output'][idx]
                    temp_list = self.endpoints['available_output']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_output'] = temp_list
                    break
            for idx, occupied_item in enumerate(self.endpoints['occupied_input']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    del self.endpoints['occupied_input'][idx]
                    temp_list = self.endpoints['available_input']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_input'] = temp_list
                    break
            mutex_endpoints.release()
            self.n_threads = self.n_threads - 1
            return 0
        connection.end_TS = millis()

        #response["description"] = [OK, No Spectrum, No route]
        # waiting E2E CS deployment finishes
        time.sleep(40)  # awaits 20 seconds before it starts tocheck
        print("Waiting the E2E CS deployment with id: " + str(cs_uuid))
        while True:
            url = "http://" + ip + selected_port +  "/pdl-transport/connectivity_service/"+str(cs_uuid)
            response = requests.get(url)
            response_json = json.loads(response.text)
            #response_json = {"status":"DEPLOYED", "description":"OK"}
            if response_json["status"] == []:
                pass
            elif response_json["status"] == "DEPLOYED" or response_json["status"] == "ERROR":
                break
            else:
                pass
            time.sleep(10)  # awaits 10 seconds before it checks again

        # print(response.status_code)
        if response_json["status"] == "ERROR":
            print('Error cs: {} -> {}'.format(cs_uuid, response_json['description']))
            connection.result = response_json['description']
            self.log.append(connection)
            mutex_endpoints.acquire()
            for idx, occupied_item in enumerate(self.endpoints['occupied_output']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    del self.endpoints['occupied_output'][idx]
                    temp_list = self.endpoints['available_output']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_output'] = temp_list
                    break
            for idx, occupied_item in enumerate(self.endpoints['occupied_input']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    del self.endpoints['occupied_input'][idx]
                    temp_list = self.endpoints['available_input']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_input'] = temp_list
                    break
            mutex_endpoints.release()
            self.n_threads = self.n_threads - 1
            return 0
        else:                                  # SUCCESSFUL CASE
            print('Successful cs: {}'.format(cs_uuid))
            connection.result = response_json['description']

        self.log.append(connection)
        s_next = poisson_wait_time(mu)
        
        connection = ConnectivityServiceData()
        connection.inter_arrival_time = s_next
        connection.uuid = cs_uuid
        connection.type = 'DELETE'

        self.delete_cs(connection, selected_port)
        

    def delete_cs(self, connection, selected_port):
        start_ht = millis()
        print("Wait " + str(connection.inter_arrival_time) + "seconds for the next E2E CS request terminate.")
        time.sleep(connection.inter_arrival_time)
        self.total_holding_time = self.total_holding_time + connection.inter_arrival_time
        check_ht = millis() - start_ht
        if check_ht/1000 < 1:
            connection.ber = False
        
        #print("Request to terminate E2E CS with ID: "+ str(connection.uuid))
        connection.start_TS = millis()
        """
        try:
            for idx, occupied_item in enumerate(self.endpoints['occupied_output']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    endpoint_output = occupied_item["endpoint_info"]
                    break
            for idx, occupied_item in enumerate(self.endpoints['occupied_input']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    endpoint_input = occupied_item["endpoint_info"]
                    break
            
            #print("Source CS: " + str(endpoint_output))
            #print("Destination CS: " + str(endpoint_input))
        except Exception as e:
            print(str(e))
            #print(self.endpoints['occupied'])
            print(self.endpoints['occupied_output'])
            print(self.endpoints['occupied_input'])
        """

        url = "http://" + ip + selected_port + "/pdl-transport/connectivity_service/terminate/" + connection.uuid
        print('SEND delete cs: {}'.format(connection.uuid))
        response = requests.post(url, data='')
        connection.end_TS = millis()

        # waiting E2E CS termination finishes
        print("Waiting the E2E CS termination with id: " + str(connection.uuid))
        while True:
            url = "http://" + ip + selected_port +   "/pdl-transport/connectivity_service/"+str(connection.uuid)
            response = requests.get(url)
            response_json = json.loads(response.text)
            #response_json = {"status":"TERMINATED", "description":"OK"}
            if response_json["status"] == "TERMINATED" or response_json["status"] == "ERROR":
                break
            time.sleep(10)  # awaits 10 seconds before it checks again

        if response_json["status"] == "ERROR":
            print('Error delete cs: {} -> {}'.format(connection.uuid, response_json['description']))
            connection.result = response_json['description']
            print(response.content)
        else:
            print('Successful delete cs: {}'.format(connection.uuid))
            connection.result = response_json['description']
            #del self.endpoints['occupied'][connection.uuid]
            #self.endpoints['available'][connection.uuid] = endpoints 
            mutex_endpoints.acquire()           
            for idx, occupied_item in enumerate(self.endpoints['occupied_input']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    temp_list = self.endpoints['available_input']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_input'] = temp_list
                    del self.endpoints['occupied_input'][idx]
                    break
            for idx, occupied_item in enumerate(self.endpoints['occupied_output']):
                if occupied_item["cs_uuid"] == connection.uuid:
                    temp_list = self.endpoints['available_output']
                    temp_list.append(occupied_item["endpoint_info"])
                    self.endpoints['available_output'] = temp_list
                    del self.endpoints['occupied_output'][idx]
                    break
            mutex_endpoints.release()

        self.log.append(connection)
        self.n_threads = self.n_threads - 1

    def exit_function(self):
        print('exit_function')
        self.end_time = millis()
        while self.n_threads != 0:
            sleep(0.5)
        print('Ending test')
        spect_error = 0
        path_error = 0
        sip_error = 0
        created = 0
        deleted = 0
        delete_error = 0
        no_ber = 0
        self.log.sort(key=lambda x: x.start_TS, reverse=False)
        with open('log_{}_a{}_h{}_c{}.csv'.format(millis(), lmb_inv, mu_inv, connections), 'w') as filehandle:
            print('WRITING log')
            filehandle.write("Parameters:\n  -N connections: %s\n  -Inter arrival rate: %s(s)\n  -Holding time: %s(s)\n" % (self.max_connections, lmb_inv, mu_inv))
            for connection in self.log:
                if connection.result == 'No spectrum':
                    spect_error = spect_error+1
                elif connection.result == 'Deployment Error':
                    path_error = path_error + 1
                elif connection.result == 'OK' and connection.type == 'CREATE':
                    created = created + 1
                elif connection.result == 'OK' and connection.type == 'DELETE':
                    deleted = deleted + 1
                elif connection.result != 'OK' and connection.type == 'DELETE':
                    delete_error = delete_error + 1
                elif connection.result == 'SOURCE SIP is already used.' or connection.result == 'DESTINATION SIP is already used.':
                    sip_error = sip_error + 1
                else:
                    print('Should not enter here')
                    print(connection)

                if not connection.ber and connection.type == 'DELETE':
                    no_ber = no_ber + 1

                filehandle.write("%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\n" % (connection.start_TS, connection.inter_arrival_time, connection.end_TS, connection.type, connection.result, connection.ber, connection.uuid))

            filehandle.write("Successfully created: %s\n" % created)
            filehandle.write("Successfully deleted: %s\n" % deleted)

            filehandle.write("Spectrum error: %s\n" % spect_error)
            filehandle.write("Path errors: %s\n" % path_error)
            filehandle.write("Error deleting: %s\n" % delete_error)
            filehandle.write("Error no BER: %s\n" % no_ber)
            assert created+spect_error+path_error+sip_error == self.max_connections
            filehandle.write("Blocking probability: %s\n" % float((spect_error+path_error)/(created+spect_error+path_error)))
            running_time = float(self.end_time-self.start_time)/1000
            filehandle.write("%s connections in %s seconds\n" % (self.max_connections, running_time))
            cps = self.max_connections/running_time
            filehandle.write("%s connections created per second\n" % (created/running_time))
            filehandle.write("Average interarrival time: %s\n" % cps)
            filehandle.write("Average holding time: %s\n" % (self.total_holding_time/deleted))
            filehandle.write("Erlangs: %s\n" % erlang)


        print('WRITTEN')

# sys.argv[1] = IP@ to send the requests
# sys.argv[2] = Inter arrival time in seconds  (1/lambda)
# sys.argv[3] = Holding time in seconds (1/mu)  --> always must be bigger than 1/lambda otherwise, it will lose requests for sure.
# sys.argv[4] = total number of requests
if __name__ == "__main__":
    #ip = 'localhost:4441'
    ip = 'localhost:'
    lmb_inv = float(sys.argv[1])
    mu_inv = float(sys.argv[2])
    connections = float(sys.argv[3])

    total_holding_time = 0
    lmb = 1/lmb_inv
    mu = 1/mu_inv
    erlang = lmb*mu_inv
    print('Starting')
    print('\tIp: {}'.format(ip))
    print('\tInter arrival time: {} seconds --> Lambda: {}'.format(lmb_inv, lmb))
    print('\tHolding time: {} seconds --> Mu: {}'.format(mu_inv, mu))
    print('\tErlangs: {}'.format(erlang))
    print('\tTotal connections: {}'.format(connections))
    connectivity = Connectivity(lmb, connections)
    input('Start?')

    connectivity.start()

