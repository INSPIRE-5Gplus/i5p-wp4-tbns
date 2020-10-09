#!/usr/local/bin/python3.4
"""
## Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO, 2020 INSPIRE5G-plus [, ANY ADDITIONAL AFFILIATION]
## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO, 2020 INSPIRE5G-plus [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).
##
## This work has been performed in the framework of the INSPIRE5G-plus
##  project, funded by the European Commission under Grant number 871808
## through the Horizon 2020 and 5G-PPP programmes. The authors would like
## to acknowledge the contributions of their colleagues of the INSPIRE5G-plus
## partner consortium (https://www.inspire-5gplus.eu/).
"""

import os, sys, logging, uuid, json, time, datetime
from slice_mgmt import nst_management as nst_mgmt
from slice_subnet_mgmt import slice_mapper as slice_mapper
from database import database as db

def slice_instantiation(nst_json, nfvo_ip, header):
    #for service_item in nst_json:
        #service_id = service_item[id]
        #slice_mapper.deploy_service(nfvo_ip, header, service_id)
    return return_text, return_code

################################ NSI CREATION & INSTANTIATION SECTION ##################################
# 2 steps: create_nsi (with its internal functions) and update_instantiating_nsi
# Network Slice Instance Object Creation
def create_nsi(nsi_json, nfvo_ip, header):
  host_ip = nfvo_ip
  request_header = header
  print ("Creating a new Network Slice record before instantiating it:")
  nstId = nsi_json['nstId']
  resp = nst_mgmt.get_nst(nstId)
  if resp[1] == 200:
    nst_json = json.loads(resp[0])
  else:
    return {"msg": "There is no NST with the given reference"}, 404
  """
  catalogue_response = nst_catalogue.get_saved_nst(nstId)
  if catalogue_response.get('nstd'):
    nst_json = catalogue_response['nstd']
  else:
    return catalogue_response, catalogue_response['http_code']
  # validate if there is any NSTD
  if not catalogue_response:
    return_msg = {}
    return_msg['error'] = "There is NO NSTd with this uuid in the DDBB."
    return return_msg, 400
  
  # check if exists another nsir with the same name, based on the same NSTd and not instantiated
  nsirepo_jsonresponse = nsi_repo.get_all_saved_nsi()
  if nsirepo_jsonresponse:
    for nsir_item in nsirepo_jsonresponse:
      if (nsir_item["name"] == nsi_json['name'] and \
          nsir_item["nst-ref"] == nstId and \
          nsir_item["nst-version"] == nst_json['version'] and \
          nsir_item["vendor"] == nst_json['vendor'] and \
          nsir_item["nsi-status"] not in ["TERMINATED", "TERMINATING", "ERROR"] ):
        return_msg = {}
        return_msg['error'] = "There is already an INSTANTIATED slice with this name and based on the selected NSTd (id/name/vendor/version)."
        return (return_msg, 400)
  """

  # creates NSI with the received information
  print ("Creating NSI record basic structure.")
  new_nsir = add_basic_nsi_info(nst_json, nsi_json)
  
  # adds the NetServices (subnets) information within the NSI record
  print ("Adding subnets into the NSI structure.")
  new_nsir = add_subnets(new_nsir, nst_json, nsi_json)

  #TODO: validate if all NSD composing the slice axist in the database.
  
  # adds the VLD information within the NSI record
  if nst_json.get('slice-vld'):
    print ("Adding vlds into the NSI structure.")
    new_nsir = add_vlds(new_nsir, nst_json, host_ip, request_header)
  
  # Network Slice Placement
  print ("Placement of the Network Service Instantiations.")
  new_nsir = nsi_placement(new_nsir, nsi_json)

  if new_nsir[1] != 200:
    LOG.info("Error returning saved nsir.")
    return (new_nsir[0], new_nsir[1])
  
  # saving the NSI into the repositories
  #nsirepo_jsonresponse = nsi_repo.safe_nsi(new_nsir[0])
  db.nsi_db.append(new_nsir[0]) #TODO: temporal

  """
  if nsirepo_jsonresponse[1] == 200:
    # starts the thread to instantiate while sending back the response
    LOG.info("Network Slice Instance Record created. Starting the instantiation procedure.")
    thread_ns_instantiation = thread_ns_instantiate(new_nsir[0])
    thread_ns_instantiation.start()
  else:
    error_msg = nsirepo_jsonresponse[0]
    new_nsir['errorLog'] = error_msg['message']
    return (new_nsir, 400)
  
  return nsirepo_jsonresponse
  """
  return new_nsir[0], 200
  
# Basic NSI structure
def add_basic_nsi_info(nst_json, nsi_json):
  nsir_dict = {}
  nsir_dict['id'] = str(uuid.uuid4())
  nsir_dict['name'] = nsi_json['name']
  if nsi_json.get('description'):
    nsir_dict['description'] = nsi_json['description']
  else:
    nsir_dict['description'] = 'This NSr is based on ' + str(nsi_json['name'])
  nsir_dict['vendor'] = nst_json['vendor']
  nsir_dict['nst-ref'] = nsi_json['nstId']
  nsir_dict['nst-name'] = nst_json['name']
  nsir_dict['nst-version'] = nst_json['version']
  nsir_dict['nsi-status'] = 'INSTANTIATING'
  nsir_dict['errorLog'] = ''
  nsir_dict['datacenter'] = []
  nsir_dict['instantiateTime'] = str(datetime.datetime.now().isoformat())
  nsir_dict['terminateTime'] = ''
  nsir_dict['scaleTime'] = ''
  nsir_dict['updateTime'] = ''
  #nsir_dict['sliceCallback'] = nsi_json['callback']  #URL used to call back the GK when the slice instance is READY/ERROR
  nsir_dict['nsr-list'] = []
  nsir_dict['vldr-list'] = []
  nsir_dict['_wim-connections']=[]
  if nsi_json.get('instantiation-params'):
    nsir_dict['_instantiation-params']=nsi_json['instantiation-params']
  else:
    nsir_dict['_instantiation-params']=[]

  return nsir_dict

# Adds the basic subnets information to the NSI record
def add_subnets(new_nsir, nst_json, request_nsi_json):
  nsr_list = []                         # empty list to add all the created slice-subnets
  serv_seq = 1                          # to put in order the services within a slice in the portal
  #nsirs_ref_list = nsi_repo.get_all_saved_nsi()
  nsirs_ref_list = db.nsi_db #TODO: temporal
  for subnet_item in nst_json["slice-ns-subnets"]:
    # Checks if there is already a shared nsr and copies its information
    found_shared_nsr = False
    if subnet_item['is-shared']:
      if nsirs_ref_list:
        for nsir_ref_item in nsirs_ref_list:
          if nsir_ref_item['nsi-status'] in ['NEW', 'INSTANTIATING', 'INSTANTIATED', 'READY']:
            for nsir_subnet_ref_item in nsir_ref_item['nsr-list']:
              if nsir_subnet_ref_item['subnet-nsdId-ref'] == subnet_item['nsd-ref'] and nsir_subnet_ref_item['isshared']:
                subnet_record = nsir_subnet_ref_item
                found_shared_nsr = True
                break
          if found_shared_nsr:
            break
        #TODO: what about the ingress and egress of a new slice having the shared NSR???
    
    # IF NSr is not shared or it is shared but not created
    if (subnet_item['is-shared'] == False or subnet_item['is-shared'] == True and found_shared_nsr == False):
      # Copying the basic subnet info from the NST to the NSI
      subnet_record = {}
      subnet_record['nsrName'] = new_nsir['name'] + "-" + subnet_item['id'] + "-" + str(serv_seq)
      subnet_record['nsrId'] = '00000000-0000-0000-0000-000000000000'
      subnet_record['nsr-placement'] = []
      subnet_record['working-status'] = 'NEW'    
      subnet_record['subnet-ref'] = subnet_item['id']
      subnet_record['subnet-nsdId-ref'] = subnet_item['nsd-name']
      subnet_record['requestId'] = '00000000-0000-0000-0000-000000000000'
      subnet_record['isshared'] = subnet_item['is-shared']
      
      # Checks if the subnet item in the NST has SLA, ingresses or egresses information
      if 'sla_name' and 'sla_id' in subnet_item:
        subnet_record['sla-name'] = subnet_item['sla-name']
        subnet_record['sla-ref'] = subnet_item['sla-ref']
      else:
        subnet_record['sla-name'] = "None"
        subnet_record['sla-ref'] = "None"
      if 'ingresses' in subnet_item:
        subnet_record['ingresses'] = subnet_item['ingresses']
      else:
        subnet_record['ingresses'] = []      
      if 'egresses' in subnet_item:
        subnet_record['egresses'] = subnet_item['egresses']
      else:
        subnet_record['egresses'] = []

      # INSTANTIATION PARAMETERS MANAGEMENT (VIM selection done in nsi_placement function)
      # Adding the instantiation parameters into the NSI subnet
      if 'instantiation-params' in request_nsi_json:
        instant_params = request_nsi_json['instantiation-params']
        for ip_item in instant_params:
          if ip_item['subnet_id'] == subnet_item['id']:
            # adding the SLA uuid to apply to the slice subnet (NS)
            if 'sla_name' and 'sla_id' in ip_item:
              subnet_record['sla-name'] = ip_item['sla_name']
              subnet_record['sla-ref'] = ip_item['sla_id']
            # checking about ingresses
            if 'ingresses' in ip_item:
              subnet_record['ingresses'] = ip_item['ingresses']
            # checking about egresses
            if 'egresses' in ip_item:
              subnet_record['egresses'] = ip_item['egresses']
      
      # adding the vld id where each subnet is connected to
      subnet_vld_list = []
      if nst_json["slice-vld"]:
        for vld_item in nst_json["slice-vld"]:
          for nsd_cp_item in vld_item['nsd-connection-point-ref']:
            if subnet_item['id'] == nsd_cp_item['subnet-ref']:
              subnet_vld_item = {}
              subnet_vld_item['vld-ref'] = vld_item['id']
              subnet_vld_list.append(subnet_vld_item)
              break
      subnet_record['vld'] = subnet_vld_list

    nsr_list.append(subnet_record)
    serv_seq = serv_seq + 1
  
  new_nsir['nsr-list'] = nsr_list
  return new_nsir

# Sends requests to create vim networks and adds their information into the NSIr
def add_vlds(new_nsir, nst_json, host_ip, request_header):
  vldr_list = []
  
  for vld_item in nst_json["slice-vld"]:
    vld_record = {}
    vld_record['id'] = vld_item['id']
    vld_record['name'] = vld_item['name']
    vld_record['vim-net-id']  = str(uuid.uuid4())
    vld_record['vim-net-stack'] = []

    if 'mgmt-network' in vld_item.keys():
      vld_record['mgmt-network'] = True
    vld_record['type'] = vld_item['type']
    #TODO: FUTUR WORK: use this parameters to define characterisitics (currently not necessary)
    #vld_record['root-bandwidth']
    #vld_record['leaf-bandwidth']
    #vld_record['physical-network']
    #vld_record['segmentation_id']
    vld_record['vld-status'] = 'INACTIVE'
    
    # Defines the parameters 'ns-conn-point-ref' & 'access_net' of each slice_vld
    cp_refs_list = []
    for cp_ref_item in vld_item['nsd-connection-point-ref']:
      cp_dict = {}
      cp_dict[cp_ref_item['subnet-ref']] = cp_ref_item['nsd-cp-ref']
      cp_refs_list.append(cp_dict)
      
      # if the slice defines the accessability (floating IPs) take it, else take it from the NSs.
      if vld_item.get('access-net'):
        vld_record['access-net'] = vld_item['access-net']
      else:
        for subn_item in nst_json["slice-ns-subnets"]:
          if subn_item['id'] == cp_ref_item['subnet-ref']:
            #repo_item = mapper.get_nsd(subn_item['nsd-ref']) nsd-ref is changed to nsd-name
            nfvo_ip = host_ip
            header = request_header
            resp = slice_mapper.get_service(nfvo_ip, header, subn_item['nsd-ref'])
            repo_item = json.loads(resp[0])
            print(repo_item)
            nsd_item = repo_item['nsd']
            for service_vl in nsd_item['virtual_links']:
              for service_cp_ref_item in service_vl['connection_points_reference']:
                if service_cp_ref_item == cp_ref_item['nsd-cp-ref']:
                  if service_vl.get('access'):
                    vld_record['access-net'] = service_vl['access']
                  else:
                    # If NSD has no 'access_net' parameter, apply True
                    vld_record['access-net'] = True
    
    vld_record['ns-conn-point-ref'] = cp_refs_list
    vld_record['shared-nsrs-list'] = []
    vldr_list.append(vld_record)

  # SHARED functionality: looking for the already shared vld
  # modify the vldr only for those where an instantiated shared ns is conencted
  #nsirs_ref_list = nsi_repo.get_all_saved_nsi()
  nsirs_ref_list = db.nsi_db #TODO: temporal

  if nsirs_ref_list:
    for nsr_item in new_nsir['nsr-list']:
      if nsr_item['isshared']:
        # looks for the nsir with the current shared nsr
        for nsir_ref_item in nsirs_ref_list:
          if nsir_ref_item['vldr-list'] and nsir_ref_item['nsi-status'] in ['NEW', 'INSTANTIATING', 'INSTANTIATED', 'READY']:
            nsir_found = False
            for nsr_ref_item in nsir_ref_item['nsr-list']:
              if (nsr_item['subnet-nsdId-ref'] == nsr_ref_item.get('subnet-nsdId-ref') and nsr_ref_item.get('isshared')):
                nsir_found = True
                break
          
            if nsir_found:
              for vld_nsr_item in nsr_item['vld']:
                for vldr_ref in nsir_ref_item['vldr-list']:
                  if vld_nsr_item['vld-ref'] == vldr_ref['id']:
                    for current_vldr_item in vldr_list:
                      if current_vldr_item['id'] == vldr_ref['id']:
                        current_vldr_item['vim-net-id'] = vldr_ref['vim-net-id']
                        current_vldr_item['vim-net-stack'] = vldr_ref['vim-net-stack']
                        current_vldr_item['vld-status'] = 'ACTIVE'
                        current_vldr_item['type'] = vldr_ref['type']
                        current_vldr_item['shared-nsrs-list'] = vldr_ref['shared-nsrs-list']
                        break
              break
  new_nsir['vldr-list'] = vldr_list
  
  return new_nsir

#TODO: improve the placement, now must use only the instantiation params
# does the NSs placement based on the available VIMs resources & the required of each NS.
def nsi_placement(new_nsir, request_nsi_json):

  def check_vim (check_vim, check_list):
    for check_list_item in check_list:
      for check_vimaccountid_item in check_list_item['vimAccountId']:
        if check_vimaccountid_item['vim-id'] == check_vim:
          return True
    
    return False
  """
  #TODO: solve how to get the resources in VIMs for a placement algorithm
  # get the VIMs information registered to the SP
  vims_list = mapper.get_vims_info()
  vims_list_len = len(vims_list['vim_list'])

  # validates if the incoming vim_list is empty (return 500) or not (follow)
  if not vims_list['vim_list']:
    return_msg = {}
    return_msg['error'] = "Not found any VIM information, register one to the SP."
    return return_msg, 500
  """
  # NSR PLACEMENT: based on the required nsr resources vs available vim resources
  # 2 POSSIBILITIES: placement based on the available resources (Opt 1) or based 
  # on the instantiation parameters (Opt 2). Opt 2 overwrites Opt 1.
  for nsr_item in new_nsir['nsr-list']:
    # if NSR IS NOT SHARED, placement is always done. Otherwise, only the first time (nsr-placement is empty)
    if (not nsr_item['isshared'] or nsr_item['isshared'] and not nsr_item['nsr-placement']):
      vim_found = False
      do_autoplacement = True
      nsr_placement_list = []
      """
      req_core = req_mem = req_sto = 0
      nsd_obj = mapper.get_nsd(nsr_item['subnet-nsdId-ref'])
      LOG.info("NSD record to check: "+str(nsd_obj))
      if nsd_obj:
        # prepares the nsr-placement object and gathers the VIMS resources values
        for vnfd_item in nsd_obj['nsd']['network_functions']:
          nsd_comp_dict = {}
          nsd_comp_dict['nsd-comp-ref'] = vnfd_item['vnf_id']
          
          # adds the vnf_id/vim_uuid dict into the slice.nsr-list information
          nsr_placement_list.append(nsd_comp_dict)
          
          # it must return a list of one element as the trio (name/vendor/version) makes it unique
          vnfd_obj = mapper.get_vnfd(vnfd_item['vnf_name'], vnfd_item['vnf_vendor'], vnfd_item['vnf_version'])
          if vnfd_obj:
            vnfd_info = vnfd_obj[0]['vnfd']
            if vnfd_info.get('virtual_deployment_units'):
              for vdu_item in vnfd_info['virtual_deployment_units']:
                # sums up al the individual VNF resources requirements into a total NS resources required
                req_core = req_core + vdu_item['resource_requirements']['cpu']['vcpus']
                if vdu_item['resource_requirements']['memory']['size_unit'] == "MB":
                  req_mem = req_mem + vdu_item['resource_requirements']['memory']['size']/1024
                else:
                  req_mem = req_mem + vdu_item['resource_requirements']['memory']['size']
                if vdu_item['resource_requirements']['storage']['size_unit'] == "MB":
                  req_sto = req_sto + vdu_item['resource_requirements']['storage']['size']/1024
                else:
                  req_sto = req_sto + vdu_item['resource_requirements']['storage']['size']
            elif vnfd_info.get('cloudnative_deployment_units'):
              # CNF does not need to look for resources to select VIM.
              pass
            else:
              new_nsir['errorLog'] = "VNF type not accepted for placement, only VNF and CNF."
              new_nsir['nsi-status'] = 'ERROR'
              # 409 = The request could not be completed due to a conflict with the current state of the resource.
              return new_nsir, 409

          else:
            new_nsir['errorLog'] = "No VNFD/CNFD available, please use a NSD with available VNFDs."
            new_nsir['nsi-status'] = 'ERROR'
            # 409 = The request could not be completed due to a conflict with the current state of the resource.
            return new_nsir, 409
      else:
        new_nsir['errorLog'] = "No " + str(nsr_item['subnet-nsdId-ref']) + " NSD FOUND."
        new_nsir['nsi-status'] = 'ERROR'
        # 409 = The request could not be completed due to a conflict with the current state of the resource.
        return new_nsir, 409
      """
      # OPTION 1: VIM selection to deploy the NSR based on instantiation parameters given by the user
      if request_nsi_json['instantiation-params']:
        for subnet_ip_index, subnet_ip_item in enumerate(request_nsi_json['instantiation-params']):
          if subnet_ip_item['subnet_id'] == nsr_item['subnet-ref']: # subnet found in the instantiation_parameters
            if 'vim_id' in subnet_ip_item:
              # assigns the VIM to the NSR and adds it into the list for the NSIr
              selected_vim = subnet_ip_item['vim_id']
              vim_found = True
              do_autoplacement = False
            else:
              # instantiation_params does not have any assigned vim for the current nsr, so it's automaticaly done
              do_autoplacement = True
            
            break
          """
          # nsr_item NOT found in the instantiation_parameters, apply autoplacement
          if subnet_ip_index == (vims_list_len-1): 
            do_autoplacement = True
            break
          """
      """
      # OPTION 2: VIM selection to deploy the NSR done through placement strategy  based on VIMs resources
      else:
        do_autoplacement = True
      if do_autoplacement:
        for vim_index, vim_item in enumerate(vims_list['vim_list']):
          # VNFs placement looks for th evisrt VIM where it can deploy all the VNF within the same NS
          #TODO: missing to use storage but this data is not comming in the VIMs information
          #if (req_core != 0 and req_mem != 0 and req_sto != 0 and vim_item['type'] == "vm"): #current nsr only has VNFs
          if (req_core != 0 and req_mem != 0 and vim_item['type'] == "vm"):
            
            available_core = vim_item['core_total'] - vim_item['core_used']
            available_memory = vim_item['memory_total'] - vim_item['memory_used']
            #available_storage = vim_item['storage_total'] - vim_item['storage_used']
            
            #if req_core > available_core or req_mem > available_memory or req_sto > available_storage:
            if req_core > available_core or req_mem > available_memory:
              # if there are no more VIMs in the list, returns error
              if vim_index == (vims_list_len-1):
                new_nsir['errorLog'] = str(nsr_item['nsrName']) + " nsr placement failed, no VIM resources available."
                new_nsir['nsi-status'] = 'ERROR'
                return new_nsir, 409
              else:
                continue
            else:
              # assigns the VIM to the NSR and adds it into the list for the NSIr
              selected_vim = vim_item['vim_uuid']
              vim_found = True
              
              # updates resources info in the temp_vims_list json to have the latest info for the next assignment
              vim_item['core_used'] = vim_item['core_used'] + req_core    
              vim_item['memory_used'] = vim_item['memory_used'] + req_mem
              #vim_item['storage_used'] = vim_item['storage_used'] + req_sto   
          # CNFs placement compares & finds the most resource free VIM available and deploys all CNFs in the VNF
          elif (req_core == 0 and req_mem == 0 and vim_item['type'] == "container"):
            selected_vim = {}
            # if no vim is still selected, take the first one
            if not selected_vim:
              selected_vim = vim_item['vim_uuid']
            # compare the selected vim with the next one in order to find which one has more available resources
            else:
              sel_vim_core = selected_vim['core_total'] - selected_vim['core_used']
              sel_vim_memory = selected_vim['memory_total'] - selected_vim['memory_used']
              challenger_vim_core = vim_item['core_total'] - vim_item['core_used']
              challenger_vim_memory = vim_item['memory_total'] - vim_item['memory_used']
              if (sel_vim_core < challenger_vim_core and sel_vim_memory < challenger_vim_memory):
                # the current VIM has more available resources than the already selected
                selected_vim = vim_item['vim_uuid']
                vim_found = True
          # NO placement done
          else:
            # if there are no more VIMs in the list, returns error
            if vim_index == (vims_list_len-1) and not selected_vim:
              new_nsir['errorLog'] = str(nsr_item['nsrName'])+ " nsr placement failed, no available VIM was found."
              new_nsir['nsi-status'] = 'ERROR'
              return new_nsir, 409

          #the following two vars must be true because CNFs look for the VIM with better conditions while VNFs look for
          #... the first VIM where the NS fits.
          if vim_found and selected_vim:
            break
      """

      for nsr_placement_item in nsr_placement_list:
        # assigns the VIM to the NSr and adds it into the list for the NSIr
        nsr_placement_item['vim-id'] = selected_vim
      
      # assigns the generated placement list to the NSir key
      nsr_item['nsr-placement'] = nsr_placement_list

  # VLDR PLACEMENT: if two nsr linked to the same vld are placed in different VIMs, the vld must have boths VIMs
  for vldr_item in new_nsir['vldr-list']:
    if not vldr_item['vim-net-stack']:
      vim_net_stack_list = []
    else:
      vim_net_stack_list = vldr_item['vim-net-stack']

    vimaccountid_list = []
    for nsr_item in new_nsir['nsr-list']:
      for vld_ref_item in nsr_item['vld']:
        if vld_ref_item['vld-ref'] == vldr_item['id']:
          for nsr_placement_item in nsr_item['nsr-placement']:
            
            # before adding, checks if this vld is already in the vim: True = adds it / False = doesn't add it
            vld_vim = check_vim(nsr_placement_item['vim-id'], vim_net_stack_list)

            # if the vld does not have the curret vim, add it with a new stack
            if not vld_vim:
              # prepares the object in case it has to be added.
              add_vl = {}
              add_vl['vim-id'] = nsr_placement_item['vim-id']
              add_vl['net-created'] = False
              
              # if empty, adds the first element
              if not vimaccountid_list:
                vimaccountid_list.append(add_vl)
              else:
                exist_vl_vimaccountid = False
                for vimAccountId_item in vimaccountid_list:
                  if vimAccountId_item['vim-id'] == nsr_placement_item['vim-id']:
                    exist_vl_vimaccountid = True
                    break
                
                if exist_vl_vimaccountid == False:
                  vimaccountid_list.append(add_vl)

    if vimaccountid_list:
      vim_net_stack_item = {}
      vim_net_stack_item['id']  = str(uuid.uuid4())
      vim_net_stack_item['vimAccountId'] = vimaccountid_list
      vim_net_stack_list.append(vim_net_stack_item)
      vldr_item['vim-net-stack'] = vim_net_stack_list

  # SLICE PLACEMENT: adds all the VIMs IDs into the slice record 'datacenter' key.
  nsi_datacenter_list = []
  if new_nsir['vldr-list']:
    for vldr_item in new_nsir['vldr-list']:
      for vim_net_stack_item in vldr_item['vim-net-stack']:
        for vimAccountId_item in vim_net_stack_item['vimAccountId']:
          #if empty, add the first VIM
          if not nsi_datacenter_list:
            nsi_datacenter_list.append(vimAccountId_item['vim-id'])
          else:
            existing_vim = False
            for nsi_datacenter_item in nsi_datacenter_list:
              if nsi_datacenter_item == vimAccountId_item['vim-id']:
                existing_vim = True
                break
            
            if existing_vim == False:
              nsi_datacenter_list.append(vimAccountId_item['vim-id'])
  else:
    for nsr_item in new_nsir['nsr-list']:
      for nsr_placement_item in nsr_item['nsr-placement']:
        if nsr_placement_item['vim-id'] not in nsi_datacenter_list:
          nsi_datacenter_list.append(nsr_placement_item['vim-id'])
  
  new_nsir['datacenter'] = nsi_datacenter_list
  return new_nsir, 200

