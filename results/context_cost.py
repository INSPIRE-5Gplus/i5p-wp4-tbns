#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, uuid, requests
from tabulate import tabulate
import datetime

# Calculates the cost to prepare the SDN Domains and IDLs.
def cost_setDomains():
    totalcost_data = []
   
    #total counters
    total_phyopt = 0
    total_linkopt = 0
    total_idl = 0
    total_sip = 0
    total_nep = 0
    total_node = 0
    total_link = 0
    total_context = 0
    total_gas_phyopt = 0
    total_gas_linkopt = 0
    total_gas_idl = 0
    total_gas_sip = 0
    total_gas_nep = 0
    total_gas_node = 0
    total_gas_link = 0
    total_gas_context = 0
    total_bytes_phyopt = 0
    total_bytes_linkopt = 0
    total_bytes_idl = 0
    total_bytes_sip = 0
    total_bytes_nep = 0
    total_bytes_node = 0
    total_bytes_link = 0
    total_bytes_context = 0

    for x in range(1, 5):
        # Open file using readlines()
        path = 'results/transparent_600_400_50/domain'+str(x)+'/log_file_2021-09-25.log'
        file1 = open(path, 'r')
        Lines = file1.readlines()
        data = []
        update_data = []
        
        # list of counters per element type
        count_phyopt = 0
        count_linkopt = 0
        count_idl = 0
        count_sip = 0
        count_nep = 0
        count_node = 0
        count_link = 0
        count_context = 0

        # list of gas counters per element type
        gascount_phyopt = 0
        gascount_linkopt = 0
        gascount_idl = 0
        gascount_sip = 0
        gascount_nep = 0
        gascount_node = 0
        gascount_link = 0
        gascount_context = 0

        # list of bytes counters per element type
        bytecount_phyopt = 0
        bytecount_linkopt = 0
        bytecount_idl = 0
        bytecount_sip = 0
        bytecount_nep = 0
        bytecount_node = 0
        bytecount_link = 0
        bytecount_context = 0

        #process the file
        for line in Lines:
            x = line.split("-")
            if 'COST PhysicalOption' in line:
                #print(" Gas Used: " + str(x[7]) + " and bytes sent: " + str(x[8]))
                gascount_phyopt = gascount_phyopt + int(x[7])
                bytecount_phyopt = bytecount_phyopt + int(x[8])
                count_phyopt +=1
            elif 'COST LinkOption' in line:
                gascount_linkopt = gascount_linkopt + int(x[7])
                bytecount_linkopt = bytecount_linkopt + int(x[8])
                count_linkopt +=1
            elif 'COST E2E_TOPOLOGY' in line:
                gascount_idl = gascount_idl + int(x[7])
                bytecount_idl = bytecount_idl + int(x[8])
                count_idl +=1
            elif 'COST SIP' in line:
                gascount_sip = gascount_sip + int(x[7])
                bytecount_sip = bytecount_sip + int(x[8])
                count_sip +=1
            elif 'COST NEP' in line:
                gascount_nep = gascount_nep + int(x[7])
                bytecount_nep = bytecount_nep + int(x[8])
                count_nep +=1
            elif 'COST NODE' in line:
                gascount_node = gascount_node + int(x[7])
                bytecount_node = bytecount_node + int(x[8])
                count_node +=1
            elif 'COST LINK' in line:
                gascount_link = gascount_link + int(x[7])
                bytecount_link = bytecount_link + int(x[8])
                count_link +=1
            elif 'COST CONTEXT' in line:
                gascount_context = gascount_context + int(x[7])
                bytecount_context = bytecount_context + int(x[8])
                count_context =+1
            else:
                pass
        
        # mean values calculus and Prepares Tables with results.
        if gascount_phyopt != 0:
            mean_gas_bytes_phyopt = gascount_phyopt/bytecount_phyopt
            mean_gas_element_phyopt = gascount_phyopt/count_phyopt
        else:
            mean_gas_bytes_phyopt = 0
            mean_gas_element_phyopt = 0
        data_element = []
        data_element.append("PhyOpt")
        data_element.append(str(count_phyopt))
        data_element.append(str(gascount_phyopt))
        data_element.append(str(mean_gas_element_phyopt))
        data_element.append(str(bytecount_phyopt))
        data_element.append(str(mean_gas_bytes_phyopt))
        data.append(data_element)
        total_phyopt = total_phyopt + count_phyopt
        total_gas_phyopt = total_gas_phyopt + gascount_phyopt
        total_bytes_phyopt = total_bytes_phyopt + bytecount_phyopt

        if gascount_linkopt != 0:
            mean_gas_bytes_linkopt = gascount_linkopt/bytecount_linkopt
            mean_gas_element_linkopt = gascount_linkopt/count_linkopt
        else:
            mean_gas_bytes_linkopt = 0
            mean_gas_element_linkopt = 0
        data_element = []
        data_element.append("LinkOpt")
        data_element.append(str(count_linkopt))
        data_element.append(str(gascount_linkopt))
        data_element.append(str(mean_gas_element_linkopt))
        data_element.append(str(bytecount_linkopt))
        data_element.append(str(mean_gas_bytes_linkopt))
        data.append(data_element)
        total_linkopt = total_linkopt + count_linkopt
        total_gas_linkopt = total_gas_linkopt + gascount_linkopt
        total_bytes_linkopt = total_bytes_linkopt + bytecount_linkopt

        if gascount_idl != 0:
            mean_gas_bytes_idl = gascount_idl/bytecount_idl
            mean_gas_element_idl = gascount_idl/count_idl
        else:
            mean_gas_bytes_idl = 0
            mean_gas_element_idl = 0
        data_element = []
        data_element.append("IDL")
        data_element.append(str(count_idl))
        data_element.append(str(gascount_idl))
        data_element.append(str(mean_gas_element_idl))
        data_element.append(str(bytecount_idl))
        data_element.append(str(mean_gas_bytes_idl))
        data.append(data_element)
        total_idl = total_idl + count_idl
        total_gas_idl = total_gas_idl + gascount_idl
        total_bytes_idl = total_bytes_idl + bytecount_idl

        if gascount_sip != 0:
            mean_gas_bytes_sip = gascount_sip/bytecount_sip
            mean_gas_element_sip = gascount_sip/count_sip
        else:
            mean_gas_bytes_sip = 0
            mean_gas_element_sip = 0
        data_element = []
        data_element.append("SIP")
        data_element.append(str(count_sip))
        data_element.append(str(gascount_sip))
        data_element.append(str(mean_gas_element_sip))
        data_element.append(str(bytecount_sip))
        data_element.append(str(mean_gas_bytes_sip))
        data.append(data_element)
        total_sip = total_sip + count_sip
        total_gas_sip = total_gas_sip + gascount_sip
        total_bytes_sip = total_bytes_sip + bytecount_sip

        if gascount_nep != 0:
            mean_gas_bytes_nep = gascount_nep/bytecount_nep
            mean_gas_element_nep = gascount_nep/count_nep
        else:
            mean_gas_bytes_nep = 0
            mean_gas_element_nep = 0
        data_element = []
        data_element.append("NEP")
        data_element.append(str(count_nep))
        data_element.append(str(gascount_nep))
        data_element.append(str(mean_gas_element_nep))
        data_element.append(str(bytecount_nep))
        data_element.append(str(mean_gas_bytes_nep))
        data.append(data_element)
        total_nep = total_nep + count_nep
        total_gas_nep = total_gas_nep + gascount_nep
        total_bytes_nep = total_bytes_nep + bytecount_nep

        if gascount_node != 0:
            mean_gas_bytes_node = gascount_node/bytecount_node
            mean_gas_element_node = gascount_node/count_node
        else:
            mean_gas_bytes_node = 0
            mean_gas_element_node = 0
        data_element = []
        data_element.append("Node")
        data_element.append(str(count_node))
        data_element.append(str(gascount_node))
        data_element.append(str(mean_gas_element_node))
        data_element.append(str(bytecount_node))
        data_element.append(str(mean_gas_bytes_node))
        data.append(data_element)
        total_node = total_node + count_node
        total_gas_node = total_gas_node + gascount_node
        total_bytes_node = total_bytes_node + bytecount_node

        if gascount_link != 0:
            mean_gas_bytes_link = gascount_link/bytecount_link
            mean_gas_element_link = gascount_link/count_link
        else:
            mean_gas_bytes_link = 0
            mean_gas_element_link = 0
        data_element = []
        data_element.append("Link")
        data_element.append(str(count_link))
        data_element.append(str(gascount_link))
        data_element.append(str(mean_gas_element_link))
        data_element.append(str(bytecount_link))
        data_element.append(str(mean_gas_bytes_link))
        data.append(data_element)
        total_link = total_link + count_link
        total_gas_link = total_gas_link + gascount_link
        total_bytes_link = total_bytes_link + bytecount_link

        if gascount_context != 0:
            mean_gas_bytes_context = gascount_context/bytecount_context
            mean_gas_element_context = gascount_context/count_context
        else:
            mean_gas_bytes_context = 0
            mean_gas_element_context = 0
        data_element = []
        data_element.append("Context")
        data_element.append(str(count_context))
        data_element.append(str(gascount_context))
        data_element.append(str(mean_gas_element_context))
        data_element.append(str(bytecount_context))
        data_element.append(str(mean_gas_bytes_context))
        data.append(data_element)
        total_context = total_context + count_context
        total_gas_context = total_gas_context + gascount_context
        total_bytes_context = total_bytes_context + bytecount_context

        #Results presentation
        print (tabulate(data, headers=["Element", "Nº Elements Added", "Total Gas Used", "Gas/Element", "Total Bytes TX", "Gas/Byte"]))
        print('-------------------------------------------------------------------------------------------------')
        print('\n')

    totalcost_data_element = []
    total_mean = total_phyopt/4
    total_meangas = total_gas_phyopt/4
    total_meanbytes = total_bytes_phyopt/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('PhyOpt')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_linkopt/4
    total_meangas = total_gas_linkopt/4
    total_meanbytes = total_bytes_linkopt/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('LinkOpt')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_idl/4
    total_meangas = total_gas_idl/4
    total_meanbytes = total_bytes_idl/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('IDL')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)
    
    totalcost_data_element = []
    total_mean = total_sip/4
    total_meangas = total_gas_sip/4
    total_meanbytes = total_bytes_sip/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('SIP')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_nep/4
    total_meangas = total_gas_nep/4
    total_meanbytes = total_bytes_nep/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('NEP')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_node/4
    total_meangas = total_gas_node/4
    total_meanbytes = total_bytes_node/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('Node')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_link/4
    total_meangas = total_gas_link/4
    total_meanbytes = total_bytes_link/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('Link')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    totalcost_data_element = []
    total_mean = total_context/4
    total_meangas = total_gas_context/4
    total_meanbytes = total_bytes_context/4
    if total_meangas != 0:
        total_meangaselement = total_meangas/total_mean
        total_meangasbyte = total_meangas/total_meanbytes
    else:
        total_meangaselement = 0
        total_meangasbyte = 0
    totalcost_data_element.append('Context')
    totalcost_data_element.append(total_mean)
    totalcost_data_element.append(total_meangas)
    totalcost_data_element.append(total_meangaselement)
    totalcost_data_element.append(total_meanbytes)
    totalcost_data_element.append(total_meangasbyte)
    totalcost_data.append(totalcost_data_element)

    #Results presentation
    print (tabulate(totalcost_data, headers=["Element", "TOTAL Nº Elements Added", "Total Gas Used", "Gas/Element", "Total Bytes TX", "Gas/Byte"]))
    print('------------------------------------------------------------------------------------------------------------')
    print('\n')

#Calculates the time to deploy the resources in the blockchain
def time_resources():
    #datetime.datetime.strptime(e2e_cs_item["deployment"]["start"], '%Y-%m-%d %H:%M:%S.%f')
    time_data = []
    
    for domain_id in range(1, 5):
        # Open file using readlines()
        path = 'results/vlink_600_400_50/domain'+str(domain_id)+'/log_file_2021-09-27.log'
        file1 = open(path, 'r')
        Lines = file1.readlines()
        updatedata_element = []
        counter_link_opt = 0
        total_link_opt_time = datetime.timedelta(days=0)
        counter_sip = 0
        total_sip_dep_time = datetime.timedelta(days=0)
        counter_nep = 0
        total_nep_dep_time = datetime.timedelta(days=0)
        counter_node = 0
        total_node_dep_time = datetime.timedelta(days=0)
        counter_link = 0
        total_link_dep_time = datetime.timedelta(days=0)
        idl_init_ref_time = datetime.timedelta(days=0)
        idl_final_ref_time = datetime.timedelta(days=0)
        sdn_final_ref_time = datetime.timedelta(days=0)
        sdn_init_ref_time = datetime.timedelta(days=0)
        current_time = datetime.timedelta(days=0)

        #process the file
        for line in Lines:
            x = line.split("-")
            if " ORCH: FIRST IDL TO ADD.\n" in line or " ORCH: ADDING ANOTHER IDL.\n" in line:
                x[2] = x[2][:-1]
                str_ref_time = x[0]+"-"+x[1]+"-"+x[2]
                idl_init_ref_time = datetime.datetime.strptime(str_ref_time, '%Y-%m-%d %H:%M:%S,%f')
                link_ref_time = idl_init_ref_time
            elif " BLOCKCHAIN_MAPPER: COST LinkOption " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                current_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                diff = current_time - link_ref_time
                counter_link_opt = counter_link_opt + 1
                total_link_opt_time = total_link_opt_time + diff
                link_ref_time = current_time
            elif 'COST E2E_TOPOLOGY' in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                idl_final_ref_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                idl_meta = current_time
            elif " ORCH: Preparing the context to be distributed."  in line:
                x[2] = x[2][:-1]
                str_ref_time = x[0]+"-"+x[1]+"-"+x[2]
                sdn_init_ref_time = datetime.datetime.strptime(str_ref_time, '%Y-%m-%d %H:%M:%S,%f')
                sdn_ref_time = sdn_init_ref_time
            elif " BLOCKCHAIN_MAPPER: COST CONTEXT " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                sdn_final_ref_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
            elif " BLOCKCHAIN_MAPPER: COST SIP " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                current_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                diff = current_time - sdn_ref_time
                total_sip_dep_time = total_sip_dep_time + diff
                counter_sip = counter_sip + 1
                sdn_ref_time = current_time
            elif " BLOCKCHAIN_MAPPER: COST NEP " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                current_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                diff = current_time - sdn_ref_time
                total_nep_dep_time = total_nep_dep_time + diff
                counter_nep = counter_nep + 1
                sdn_ref_time = current_time
            elif " BLOCKCHAIN_MAPPER: COST NODE " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                current_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                diff = current_time - sdn_ref_time
                total_node_dep_time = total_node_dep_time + diff
                counter_node = counter_node + 1
                sdn_ref_time = current_time
            elif " BLOCKCHAIN_MAPPER: COST LINK " in line:
                x[2] = x[2][:-1]
                str_time = x[0]+"-"+x[1]+"-"+x[2]
                current_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S,%f')
                diff = current_time - sdn_ref_time
                total_link_dep_time = total_link_dep_time + diff
                counter_link = counter_link + 1
                sdn_ref_time = current_time
            else:
                pass

        # Calcuates IDL Mean Time Value per domain
        if counter_link_opt == 0:
            unit_link_opt_time = datetime.timedelta(days=0)
        else:
            unit_link_opt_time = total_link_opt_time/counter_link_opt
        if unit_link_opt_time == datetime.timedelta(days=0):
            unit_idl_meta_time = datetime.timedelta(days=0)
            idl_depl_time = datetime.timedelta(days=0)
        else:
            unit_idl_meta_time = idl_final_ref_time - idl_meta
            idl_depl_time = idl_final_ref_time - idl_init_ref_time
        if counter_sip == 0:
            sdn_sip_time = datetime.timedelta(days=0)
        else:
            sdn_sip_time = total_sip_dep_time/counter_sip
        if counter_nep == 0:
            sdn_nep_time = datetime.timedelta(days=0)
        else:
            sdn_nep_time = total_nep_dep_time/counter_nep
        if counter_node == 0:
            sdn_node_time = datetime.timedelta(days=0)
        else:
            sdn_node_time = total_node_dep_time/counter_node
        if counter_link == 0:
            sdn_link_time= datetime.timedelta(days=0)
        else:
            sdn_link_time = total_link_dep_time/counter_link
        sdn_depl_time = sdn_final_ref_time - sdn_init_ref_time

        #calculates and adds the total mean values into the table.
        updatedata_element.append("Domain " + str(domain_id))
        updatedata_element.append(str(unit_link_opt_time.total_seconds()))
        updatedata_element.append(str(counter_link_opt))
        updatedata_element.append(str(total_link_opt_time.total_seconds()))
        updatedata_element.append(str(unit_idl_meta_time.total_seconds()))
        updatedata_element.append(str(idl_depl_time.total_seconds()))
        updatedata_element.append(str(sdn_sip_time.total_seconds()))
        updatedata_element.append(str(counter_sip))
        updatedata_element.append(str(total_sip_dep_time.total_seconds()))
        updatedata_element.append(str(sdn_nep_time.total_seconds()))
        updatedata_element.append(str(counter_nep))
        updatedata_element.append(str(total_nep_dep_time.total_seconds()))
        updatedata_element.append(str(sdn_node_time.total_seconds()))
        updatedata_element.append(str(counter_node))
        updatedata_element.append(str(total_node_dep_time.total_seconds()))
        updatedata_element.append(str(sdn_link_time.total_seconds()))
        updatedata_element.append(str(counter_link))
        updatedata_element.append(str(total_link_dep_time.total_seconds()))
        updatedata_element.append(str(sdn_depl_time.total_seconds()))
        time_data.append(updatedata_element)

    #Results presentation
    print('\n')
    print (tabulate(time_data, headers=["Unidir. IDL (Unit)", "Unidir. IDL Count" , "Total Unidir. IDL" , "IDL Topo Metadata (Unit)", "Total IDL", "SIP (Unit)", "SIP Count" , "Total SIP", "NEP (Unit)", "NEP Count", "Total NEP", "Node (Unit)", "Node Count", "Total Node", "Link (Unit)", "Link Count", "Total Link", "Context"]))
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('\n')

#Calculates the cost to update the NEPs, SIPs and the IDLs for an E2E CS deployment.
def cost_E2ECS():
    totalupdate_data = []
   
    #total counters
    total_updatenep = 0
    total_updatesip = 0
    total_updatelink = 0
    total_updatephy = 0
    total_requestdep = 0
    total_updaterequestdep = 0
    total_requestterm = 0
    total_updaterequestterm = 0
    total_meangas_nep = 0
    total_meangas_sip = 0
    total_meangas_link = 0
    total_meangas_phy = 0
    total_meangas_dep = 0
    total_meangas_updatedep = 0
    total_meangas_term = 0
    total_meangas_updateterm = 0
    total_meanbytes_nep = 0
    total_meanbytes_sip = 0
    total_meanbytes_link = 0
    total_meanbytes_phy = 0
    total_meanbytes_dep = 0
    total_meanbytes_updatedep = 0
    total_meanbytes_term = 0
    total_meanbytes_updateterm = 0

    for x in range(1, 5):
        # Open file using readlines()
        path = 'results/vlink_600_400_50/domain'+str(x)+'/log_file_2021-09-27.log'
        file1 = open(path, 'r')
        Lines = file1.readlines()
        update_data = []
        
        # list of update counters
        updatecount_sip = 0
        updatecount_nep = 0
        updatecount_phyopt = 0
        updatecount_linkopt = 0
        count_depdomaincs = 0
        updatecount_depdomaincs = 0
        count_termdomaincs = 0
        updatecount_termdomaincs = 0
        gascount_updatesip = 0
        gascount_updatenep = 0
        gascount_updatephyopt = 0
        gascount_updatelinkopt = 0
        gascount_depdomaincs = 0
        gascount_updatedepdomaincs = 0
        gascount_termdomaincs = 0
        gascount_updatetermdomaincs = 0
        bytescount_udpdatesip = 0
        bytescount_udpdatenep = 0
        bytescount_udpdatephyopt = 0
        bytescount_udpdatelinkopt = 0
        bytescount_depdomaincs = 0
        bytescount_updatedepdomaincs = 0
        bytescount_terdomaincs = 0
        bytescount_updatetermdomaincs = 0

        #process the file
        for line in Lines:
            x = line.split("-")
            if 'COST_NEP_Update' in line:
                updatecount_nep +=1
                gascount_updatenep = gascount_updatenep + int(x[7])
                bytescount_udpdatenep = bytescount_udpdatenep + int(x[8])
            elif 'COST_SIP_Update' in line:
                updatecount_sip +=1
                gascount_updatesip = gascount_updatesip + int(x[7])
                bytescount_udpdatesip = bytescount_udpdatesip + int(x[8])
            elif 'COST_LinkOption_Update' in line:
                updatecount_linkopt +=1
                gascount_updatelinkopt = gascount_updatelinkopt + int(x[7])
                bytescount_udpdatelinkopt = bytescount_udpdatelinkopt + int(x[8])
            elif 'COST_PhysicalOption_Update' in line:
                updatecount_phyopt +=1
                gascount_updatephyopt = gascount_updatephyopt + int(x[7])
                bytescount_udpdatephyopt = bytescount_udpdatephyopt + int(x[8])
            elif 'COST DEPLOY_CS' in line:
                # COST DEPLOT CS is the cost to request through the BL to deploy a domain CS
                if 'COST DEPLOY_CS Update' in line:
                    updatecount_depdomaincs +=1
                    gascount_updatedepdomaincs = gascount_updatedepdomaincs + int(x[7])
                    bytescount_updatedepdomaincs = bytescount_updatedepdomaincs + int(x[8])
                else:
                    count_depdomaincs +=1
                    gascount_depdomaincs = gascount_depdomaincs + int(x[7])
                    bytescount_depdomaincs = bytescount_depdomaincs + int(x[8])
            elif 'COST TERMINATE_CS' in line:
                # COST TERMINATE CS is the cost to request through the BL to terminate a domain CS
                if 'COST TERMINATE_CS Update' in line:
                    updatecount_termdomaincs +=1
                    gascount_updatetermdomaincs = gascount_updatetermdomaincs + int(x[7])
                    bytescount_updatetermdomaincs = bytescount_updatetermdomaincs + int(x[8])
                else:
                    count_termdomaincs +=1
                    gascount_termdomaincs = gascount_termdomaincs + int(x[7])
                    bytescount_terdomaincs = bytescount_terdomaincs + int(x[8])
            else:
                pass

        #Prepares Tables with results.
        if gascount_updatenep != 0:
            mean_gas_element_updatenep = gascount_updatenep/updatecount_nep
            mean_bytes_element_updatenep = bytescount_udpdatenep/updatecount_nep
        else:
            mean_gas_element_updatenep = 0
            mean_bytes_element_updatenep = 0
        updatedata_element = []
        updatedata_element.append("Update NEP")
        updatedata_element.append(str(updatecount_nep))
        updatedata_element.append(str(mean_gas_element_updatenep))
        updatedata_element.append(str(mean_bytes_element_updatenep))
        update_data.append(updatedata_element)
        total_updatenep = total_updatenep + updatecount_nep
        total_meangas_nep = total_meangas_nep + mean_gas_element_updatenep
        total_meanbytes_nep = total_meanbytes_nep + mean_bytes_element_updatenep

        if gascount_updatesip != 0:
            mean_gas_element_updatesip = gascount_updatesip/updatecount_sip
            mean_bytes_element_updatesip = bytescount_udpdatesip/updatecount_sip
        else:
            mean_gas_element_updatesip = 0
            mean_bytes_element_updatesip = 0
        updatedata_element = []
        updatedata_element.append("Update SIP")
        updatedata_element.append(str(updatecount_sip))
        updatedata_element.append(str(mean_gas_element_updatesip))
        updatedata_element.append(str(mean_bytes_element_updatesip))
        update_data.append(updatedata_element)
        total_updatesip = total_updatesip + updatecount_sip
        total_meangas_sip = total_meangas_sip + mean_gas_element_updatesip
        total_meanbytes_sip = total_meanbytes_sip + mean_bytes_element_updatesip

        if gascount_updatelinkopt != 0:
            mean_gas_element_updatelinkopt = gascount_updatelinkopt/updatecount_linkopt
            mean_bytes_element_updatelinkopt = bytescount_udpdatelinkopt/updatecount_linkopt
        else:
            mean_gas_element_updatelinkopt = 0
            mean_bytes_element_updatelinkopt = 0
        updatedata_element = []
        updatedata_element.append("Update Link-Option")
        updatedata_element.append(str(updatecount_linkopt))
        updatedata_element.append(str(mean_gas_element_updatelinkopt))
        updatedata_element.append(str(mean_bytes_element_updatelinkopt))
        update_data.append(updatedata_element)
        total_updatelink = total_updatelink + updatecount_linkopt
        total_meangas_link = total_meangas_link + mean_gas_element_updatelinkopt
        total_meanbytes_link = total_meanbytes_link + mean_bytes_element_updatelinkopt

        if gascount_updatephyopt != 0:
            mean_gas_element_updatephyopt = gascount_updatephyopt/updatecount_phyopt
            mean_bytes_element_updatephyopt = bytescount_udpdatephyopt/updatecount_phyopt
        else:
            mean_gas_element_updatephyopt = 0
            mean_bytes_element_updatephyopt = 0
        updatedata_element = []
        updatedata_element.append("Update Physical-Option")
        updatedata_element.append(str(updatecount_phyopt))
        updatedata_element.append(str(mean_gas_element_updatephyopt))
        updatedata_element.append(str(mean_bytes_element_updatephyopt))
        update_data.append(updatedata_element)
        total_updatephy = total_updatephy + count_depdomaincs
        total_meangas_phy = total_meangas_phy + mean_gas_element_updatephyopt
        total_meanbytes_phy = total_meanbytes_phy + mean_bytes_element_updatephyopt

        if gascount_depdomaincs != 0:
            mean_gas_element_depdomaincs = gascount_depdomaincs/count_depdomaincs
            mean_bytes_element_depdomaincs = bytescount_depdomaincs/count_depdomaincs
        else:
            mean_gas_element_depdomaincs = 0
            mean_bytes_element_depdomaincs = 0
        updatedata_element = []
        updatedata_element.append("Request Domain CS Deployment")
        updatedata_element.append(str(count_depdomaincs))
        updatedata_element.append(str(mean_gas_element_depdomaincs))
        updatedata_element.append(str(mean_bytes_element_depdomaincs))
        update_data.append(updatedata_element)
        total_requestdep = + total_requestdep + count_depdomaincs
        total_meangas_dep = total_meangas_dep + mean_gas_element_depdomaincs
        total_meanbytes_dep = total_meanbytes_dep + mean_bytes_element_depdomaincs

        if gascount_updatedepdomaincs != 0:
            mean_gas_element_updatedepdomaincs = gascount_updatedepdomaincs/updatecount_depdomaincs
            mean_bytes_element_updatedepdomaincs = bytescount_updatedepdomaincs/updatecount_depdomaincs
        else:
            mean_gas_element_updatedepdomaincs = 0
            mean_bytes_element_updatedepdomaincs = 0
        updatedata_element = []
        updatedata_element.append("Update Request Domain CS Deployment")
        updatedata_element.append(str(updatecount_depdomaincs))
        updatedata_element.append(str(mean_gas_element_updatedepdomaincs))
        updatedata_element.append(str(mean_bytes_element_updatedepdomaincs))
        update_data.append(updatedata_element)
        total_updaterequestdep = total_updaterequestdep + updatecount_depdomaincs
        total_meangas_updatedep = total_meangas_updatedep + mean_gas_element_updatedepdomaincs
        total_meanbytes_updatedep = total_meanbytes_updatedep + mean_bytes_element_updatedepdomaincs

        if gascount_termdomaincs != 0:
            mean_gas_element_termdomaincs = gascount_termdomaincs/count_termdomaincs
            mean_bytes_element_termdomaincs = bytescount_terdomaincs/count_termdomaincs
        else:
            mean_gas_element_termdomaincs = 0
            mean_bytes_element_termdomaincs = 0
        updatedata_element = []
        updatedata_element.append("Request Domain CS Terminate")
        updatedata_element.append(str(count_termdomaincs))
        updatedata_element.append(str(mean_gas_element_termdomaincs))
        updatedata_element.append(str(mean_bytes_element_termdomaincs))
        update_data.append(updatedata_element)
        total_requestterm = total_requestterm + count_termdomaincs
        total_meangas_term = total_meangas_term + mean_gas_element_termdomaincs
        total_meanbytes_term = total_meanbytes_term + mean_bytes_element_termdomaincs

        if gascount_updatedepdomaincs != 0:
            mean_gas_element_updatetermdomaincs = gascount_updatetermdomaincs/updatecount_termdomaincs
            mean_bytes_element_updatetermdomaincs = bytescount_updatetermdomaincs/updatecount_termdomaincs
        else:
            mean_gas_element_updatetermdomaincs = 0
            mean_bytes_element_updatetermdomaincs = 0
        updatedata_element = []
        updatedata_element.append("Update Request Domain CS Terminate")
        updatedata_element.append(str(updatecount_termdomaincs))
        updatedata_element.append(str(mean_gas_element_updatetermdomaincs))
        updatedata_element.append(str(mean_bytes_element_updatetermdomaincs))
        update_data.append(updatedata_element)
        total_updaterequestterm = total_updaterequestterm + updatecount_termdomaincs
        total_meangas_updateterm = total_meangas_updateterm + mean_gas_element_updatetermdomaincs
        total_meanbytes_updateterm = total_meanbytes_updateterm + mean_bytes_element_updatetermdomaincs

        #DOMAIN Results presentation
        print('\n')
        print (tabulate(update_data, headers=["Element", "Nº Actions Done", "Gas/Element", "Bytes/Element"]))
        print('-----------------------------------------------------------------------')
        print('\n')

    totalupdate_data_element = []
    total_mean_updatenep = total_updatenep/4
    total_mean_meangas_nep = total_meangas_nep/4
    total_mean_meanbytes_nep = total_meanbytes_nep/4
    totalupdate_data_element.append('Update NEP')
    totalupdate_data_element.append(total_mean_updatenep)
    totalupdate_data_element.append(total_mean_meangas_nep)
    totalupdate_data_element.append(total_mean_meanbytes_nep)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_updatesip = total_updatesip/4
    total_mean_meangas_sip = total_meangas_sip/4
    total_mean_meanbytes_sip = total_meanbytes_sip/4
    totalupdate_data_element.append('Update SIP')
    totalupdate_data_element.append(total_mean_updatesip)
    totalupdate_data_element.append(total_mean_meangas_sip)
    totalupdate_data_element.append(total_mean_meanbytes_sip)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_updatelink = total_updatelink/4
    total_mean__meangas_link = total_meangas_link/4
    total_mean_meanbytes_link = total_meanbytes_link/4
    totalupdate_data_element.append('Update Link-Option')
    totalupdate_data_element.append(total_mean_updatelink)
    totalupdate_data_element.append(total_mean__meangas_link)
    totalupdate_data_element.append(total_mean_meanbytes_link)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_updatephy = total_updatephy/4
    total_mean_meangas_phy = total_meangas_phy/4
    total_mean_meanbytes_phy = total_meanbytes_phy/4
    totalupdate_data_element.append('Update Physical-Option')
    totalupdate_data_element.append(total_mean_updatephy)
    totalupdate_data_element.append(total_mean_meangas_phy)
    totalupdate_data_element.append(total_mean_meanbytes_phy)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_requestdep = total_requestdep/4
    total_mean_meangas_dep = total_meangas_dep/4
    total_mean_meanbytes_dep = total_meanbytes_dep/4
    totalupdate_data_element.append('Request Domain CS Deployment')
    totalupdate_data_element.append(total_mean_requestdep)
    totalupdate_data_element.append(total_mean_meangas_dep)
    totalupdate_data_element.append(total_mean_meanbytes_dep)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_updaterequestdep = total_updaterequestdep/4
    total_mean_meangas_updatedep = total_meangas_updatedep/4
    total_mean_meanbytes_updatedep = total_meanbytes_updatedep/4
    totalupdate_data_element.append('Update Request Domain CS Deployment')
    totalupdate_data_element.append(total_mean_updaterequestdep)
    totalupdate_data_element.append(total_mean_meangas_updatedep)
    totalupdate_data_element.append(total_mean_meanbytes_updatedep)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_requestterm = total_requestterm/4
    total_mean_meangas_term = total_meangas_term/4
    total_mean_meanbytes_term = total_meanbytes_term/4
    totalupdate_data_element.append('Request Domain CS Terminate')
    totalupdate_data_element.append(total_mean_requestterm)
    totalupdate_data_element.append(total_mean_meangas_term)
    totalupdate_data_element.append(total_mean_meanbytes_term)
    totalupdate_data.append(totalupdate_data_element)
    totalupdate_data_element = []
    total_mean_updaterequestterm = total_updaterequestterm/4
    total_mean_meangas_updateterm = total_meangas_updateterm/4
    total_mean_meanbytes_updateterm = total_meanbytes_updateterm/4
    totalupdate_data_element.append('Update NEP')
    totalupdate_data_element.append(total_mean_updaterequestterm)
    totalupdate_data_element.append(total_mean_meangas_updateterm)
    totalupdate_data_element.append(total_mean_meanbytes_updateterm)
    totalupdate_data.append(totalupdate_data_element)

    
    # TOTAL Results presentation
    print('\n')
    print (tabulate(totalupdate_data, headers=["Element", "Nº Actions Done", "Gas/Element", "Bytes/Element"]))
    print('-----------------------------------------------------------------------')
    print('\n')

#Calculates the cost to update the NEPs, SIPs and the IDLs for an E2E CS  deployment.
def time_deployments():
    time_data = []
    
    for domain_id in range(1, 5):
        # Open file using readlines()
        path = 'results/vlink_600_400_50/domain'+str(domain_id)+'/log_file_2021-09-27.log'
        file1 = open(path, 'r')
        Lines = file1.readlines()
        e2e_cs_list = []
        local_cs_list = []
        bl_cs_list = []
        updatedata_element = []

        #process the file
        for line in Lines:
            x = line.split("-")
            #if ' TIME INSTANTIATE E2E ' in line:
                #print(x)
                #print(x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11])
                #print(type(x[6]))
            if x[6] == " TIME INSTANTIATE E2E " or x[6] == " TIME TERMINATE E2E ":
                if x[6] == " TIME INSTANTIATE E2E " and e2e_cs_list == []:
                    e2e_cs_item = {}
                    e2e_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    dep = {}
                    x[12] = x[12].replace(' ', '')
                    dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                    dep["start"] = dep["start"].replace('\n', '')
                    e2e_cs_item["deployment"] = dep
                    e2e_cs_list.append(e2e_cs_item)
                else:
                    ref_uuid = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    found_e2e_cs = False
                    for e2e_cs_item in e2e_cs_list:
                        if e2e_cs_item["uuid"] == ref_uuid:
                            if x[6] == " TIME INSTANTIATE E2E ":
                                x[12] = x[12].replace(' ', '')
                                dep_end = x[12]+"-"+x[13]+"-"+x[14]
                                dep_end = dep_end.replace('\n', '')
                                e2e_cs_item["deployment"]["finish"] = dep_end
                                start =  datetime.datetime.strptime(e2e_cs_item["deployment"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(e2e_cs_item["deployment"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                e2e_cs_item["deployment"]["difference"] = diff.total_seconds()
                            elif x[6] == " TIME TERMINATE E2E " and 'termination' not in e2e_cs_item.keys():
                                term = {}
                                x[12] = x[12].replace(' ', '')
                                term["start"] = x[12]+"-"+x[13]+"-"+x[14]
                                term["start"] = term["start"].replace('\n', '')
                                e2e_cs_item["termination"] = term
                            elif x[6] == " TIME TERMINATE E2E " and 'termination' in e2e_cs_item.keys():
                                x[12] = x[12].replace(' ', '')
                                term_end = x[12]+"-"+x[13]+"-"+x[14]
                                term_end = term_end.replace('\n', '')
                                e2e_cs_item["termination"]["finish"] = term_end
                                start =  datetime.datetime.strptime(e2e_cs_item["termination"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(e2e_cs_item["termination"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                e2e_cs_item["termination"]["difference"] = diff.total_seconds()
                            else:
                                pass

                            found_e2e_cs = True
                            break
                    if found_e2e_cs == False:
                        #add new element
                        e2e_cs_item = {}
                        e2e_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                        dep = {}
                        x[12] = x[12].replace(' ', '')
                        dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                        dep["start"] = dep["start"].replace('\n', '')
                        e2e_cs_item["deployment"] = dep
                        e2e_cs_list.append(e2e_cs_item)        
            elif x[6] == " TIME INSTANTIATE LOCAL " or x[6] == " TIME TERMINATE LOCAL ":
                if x[6] == "TIME INSTANTIATE LOCAL" and local_cs_list == []:
                    local_cs_item = {}
                    local_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    dep = {}
                    x[12] = x[12].replace(' ', '')
                    dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                    dep["start"] = dep["start"].replace('\n', '')
                    local_cs_item["deployment"] = dep
                    local_cs_list.append(local_cs_item)
                else:
                    ref_uuid = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    found_local_cs = False
                    for local_cs_item in local_cs_list:
                        if local_cs_item["uuid"] == ref_uuid:
                            if x[6] == " TIME INSTANTIATE LOCAL ":
                                x[12] = x[12].replace(' ', '')
                                dep_end = x[12]+"-"+x[13]+"-"+x[14]
                                dep_end = dep_end.replace('\n', '')
                                local_cs_item["deployment"]["finish"] = dep_end
                                start =  datetime.datetime.strptime(local_cs_item["deployment"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(local_cs_item["deployment"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                local_cs_item["deployment"]["difference"] = diff.total_seconds()
                            elif x[6] == " TIME TERMINATE LOCAL " and 'termination' not in local_cs_item.keys():
                                term = {}
                                x[12] = x[12].replace(' ', '')
                                term["start"] = x[12]+"-"+x[13]+"-"+x[14]
                                term["start"] = term["start"].replace('\n', '')
                                local_cs_item["termination"] = term
                            elif x[6] == " TIME TERMINATE LOCAL " and 'termination' in local_cs_item.keys():
                                x[12] = x[12].replace(' ', '')
                                term_end = x[12]+"-"+x[13]+"-"+x[14]
                                term_end = term_end.replace('\n', '')
                                local_cs_item["termination"]["finish"] = term_end
                                start =  datetime.datetime.strptime(local_cs_item["termination"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(local_cs_item["termination"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                local_cs_item["termination"]["difference"] = diff.total_seconds()
                            else:
                                pass

                            found_local_cs = True
                            break
                    if found_local_cs == False:
                        #add new element
                        local_cs_item = {}
                        local_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                        dep = {}
                        x[12] = x[12].replace(' ', '')
                        dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                        dep["start"] = dep["start"].replace('\n', '')
                        local_cs_item["deployment"] = dep
                        local_cs_list.append(local_cs_item)   
            elif x[6] == " TIME INSTANTIATE BLOCKCHAIN " or x[6] == " TIME TERMINATE BLOCKCHAIN ":
                if x[6] == " TIME INSTANTIATE BLOCKCHAIN " and bl_cs_list == []:
                    bl_cs_item = {}
                    bl_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    dep = {}
                    x[12] = x[12].replace(' ', '')
                    dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                    dep["start"] = dep["start"].replace('\n', '')
                    bl_cs_item["deployment"] = dep
                    bl_cs_list.append(bl_cs_item)
                else:
                    ref_uuid = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                    found_bl_cs = False
                    for bl_cs_item in bl_cs_list:
                        if bl_cs_item["uuid"] == ref_uuid:
                            if x[6] == " TIME INSTANTIATE BLOCKCHAIN ":
                                x[12] = x[12].replace(' ', '')
                                dep_end = x[12]+"-"+x[13]+"-"+x[14]
                                dep_end = dep_end.replace('\n', '')
                                bl_cs_item["deployment"]["finish"] = dep_end
                                start =  datetime.datetime.strptime(bl_cs_item["deployment"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(bl_cs_item["deployment"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                bl_cs_item["deployment"]["difference"] = diff.total_seconds()
                            elif x[6] == " TIME TERMINATE BLOCKCHAIN " and 'termination' not in bl_cs_item.keys():
                                term = {}
                                x[12] = x[12].replace(' ', '')
                                term["start"] = x[12]+"-"+x[13]+"-"+x[14]
                                term["start"] = term["start"].replace('\n', '')
                                bl_cs_item["termination"] = term
                            elif x[6] == " TIME TERMINATE BLOCKCHAIN " and 'termination' in bl_cs_item.keys():
                                x[12] = x[12].replace(' ', '')
                                term_end = x[12]+"-"+x[13]+"-"+x[14]
                                term_end = term_end.replace('\n', '')
                                bl_cs_item["termination"]["finish"] = term_end
                                start =  datetime.datetime.strptime(bl_cs_item["termination"]["start"], '%Y-%m-%d %H:%M:%S.%f')
                                finish =  datetime.datetime.strptime(bl_cs_item["termination"]["finish"], '%Y-%m-%d %H:%M:%S.%f')
                                diff = finish - start
                                bl_cs_item["termination"]["difference"] = diff.total_seconds()
                            else:
                                pass

                            found_bl_cs = True
                            break
                    if found_bl_cs == False:
                        #add new element
                        bl_cs_item = {}
                        bl_cs_item["uuid"] = x[7]+"-"+x[8]+"-"+x[9]+"-"+x[10]+"-"+x[11]
                        dep = {}
                        x[12] = x[12].replace(' ', '')
                        dep["start"] = x[12]+"-"+x[13]+"-"+x[14]
                        dep["start"] = dep["start"].replace('\n', '')
                        bl_cs_item["deployment"] = dep
                        bl_cs_list.append(bl_cs_item)
            else:
                pass
        
        # Calcuates E2E Mean Time Value per domain
        e2e_deployment_time = 0
        e2e_terminate_time = 0
        e2e_counter = 0
        for e2e_cs_item in e2e_cs_list:
            if "difference" in e2e_cs_item["deployment"].keys() and "difference" in e2e_cs_item["termination"].keys():
                e2e_deployment_time = e2e_deployment_time + e2e_cs_item["deployment"]["difference"]
                e2e_terminate_time = e2e_terminate_time + e2e_cs_item["termination"]["difference"]
                e2e_counter +=1
        if e2e_counter != 0:
            depl_mean_val = e2e_deployment_time/e2e_counter
            term_mean_val = e2e_terminate_time/e2e_counter
        else:
            depl_mean_val = 0
            term_mean_val = 0
        updatedata_element.append(domain_id)
        updatedata_element.append(depl_mean_val)
        updatedata_element.append(term_mean_val)
        
        # Calcuates Local Mean Time Value per domain
        local_deployment_time = 0
        local_terminate_time = 0
        local_counter = 0
        for local_cs_item in local_cs_list:
            if "difference" in local_cs_item["deployment"].keys() and "difference" in local_cs_item["termination"].keys():
                local_deployment_time = local_deployment_time + local_cs_item["deployment"]["difference"]
                local_terminate_time = local_terminate_time + local_cs_item["termination"]["difference"]
                local_counter +=1
        if local_counter != 0:
            depl_mean_val = local_deployment_time/local_counter
            term_mean_val = local_terminate_time/local_counter
        else:
            depl_mean_val = 0
            term_mean_val = 0
        updatedata_element.append(depl_mean_val)
        updatedata_element.append(term_mean_val)
        
        # Calcuates Blockchain Mean Time Value per domain
        bl_deployment_time = 0
        bl_terminate_time = 0
        bl_counter = 0
        for bl_cs_item in bl_cs_list:
            if "difference" in bl_cs_item["deployment"].keys() and "difference" in bl_cs_item["termination"].keys():
                bl_deployment_time = bl_deployment_time + bl_cs_item["deployment"]["difference"]
                bl_terminate_time = bl_terminate_time + bl_cs_item["termination"]["difference"]
                bl_counter +=1
        if bl_counter != 0:
            depl_mean_val = bl_deployment_time/bl_counter
            term_mean_val = bl_terminate_time/bl_counter
        else:
            depl_mean_val = 0
            term_mean_val = 0
        updatedata_element.append(depl_mean_val)
        updatedata_element.append(term_mean_val)
        time_data.append(updatedata_element)
    
        print(e2e_cs_list)


    #calculates the total mean values
    total_e2e_dep = 0
    total_e2e_term = 0
    total_local_dep = 0
    total_local_term = 0
    total_bl_dep = 0
    total_bl_term = 0
    domains_counter = 0
    updatedata_element = []
    
    for time_data_item in time_data:
        total_e2e_dep = total_e2e_dep + time_data_item[1]
        total_e2e_term = total_e2e_term + time_data_item[2]
        total_local_dep = total_local_dep + time_data_item[3]
        total_local_term = total_local_term + time_data_item[4]
        total_bl_dep = total_bl_dep + time_data_item[5]
        total_bl_term = total_bl_term + time_data_item[6]
        domains_counter +=1

    #calculates and adds the total mean values into the table.
    updatedata_element.append("Total")
    total_e2e_dep = total_e2e_dep/domains_counter
    updatedata_element.append(str(total_e2e_dep))
    total_e2e_term = total_e2e_term/domains_counter
    updatedata_element.append(str(total_e2e_term))
    total_local_dep = total_local_dep/domains_counter
    updatedata_element.append(str(total_local_dep))
    total_local_term = total_local_term/domains_counter
    updatedata_element.append(str(total_local_term))
    total_bl_dep = total_bl_dep/domains_counter
    updatedata_element.append(str(total_bl_dep))
    total_bl_term = total_bl_term/domains_counter
    updatedata_element.append(str(total_bl_term))
    time_data.append(updatedata_element)

    #Results presentation
    print('\n')
    print (tabulate(time_data, headers=["Domain", "E2E Deployment", "E2E Terminate", "LOCAL Deployment", "LOCAL Terminate", "BLOCKCHAIN Deployment", "BLOCKCHAIN Terminate"]))
    print('-----------------------------------------------------------------------------------------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------------------------------------')
    print('\n')

# Calculates the usage of eahc link and how much spectrum.
def links_usage():
    test_links = {}
    ref_links = []
    used_links = []
    cs_counter = 0

    abs_model = "transparent"  # "VNODE, VLINK, TRANSPARENT"

    if abs_model == "vnode":
        # creates the list with all the existing links in the test
        for domain_id in range(1, 5):
            # Adding reference links from the IDLs context
            with open('database/interdomain-links/vnode/idl_d'+str(domain_id)+'.json') as json_file:
                data = json.load(json_file)
                for idl_item in data['e2e-topology']['interdomain-links']:
                    for link_item in idl_item['link-options']:
                        found_link = False
                        for ref_link_item in ref_links:
                            if link_item["uuid"] == ref_link_item["uuid"]:
                                found_link = True
                                break
                        if found_link == False:
                            ref_link = {}
                            ref_link["uuid"] = link_item["uuid"]
                            ref_link["counter"] = 0
                            ref_link["used_capacity"] = 0
                            ref_links.append(ref_link)
    elif abs_model == "vlink":
        # creates the list with all the existing links in the test
        for domain_id in range(1, 5):
            # Adding SDN CONTEXT reference links 
            with open('database/SDN_contexts/D'+str(domain_id)+'_vlink.json') as json_file:
                data = json.load(json_file)
                for link_item in data['tapi-common:context']['tapi-topology:topology-context']['topology'][0]['link']:
                    ref_link = {}
                    ref_link["uuid"] = link_item["uuid"]
                    ref_link["counter"] = 0
                    ref_links.append(ref_link)
        
            # Adding IDLs context reference links
            with open('database/interdomain-links/vlink_transparent/idl_d'+str(domain_id)+'.json') as json_file:
                data = json.load(json_file)
                for idl_item in data['e2e-topology']['interdomain-links']:
                    for link_item in idl_item['link-options']:
                        found_link = False
                        for ref_link_item in ref_links:
                            if link_item["uuid"] == ref_link_item["uuid"]:
                                found_link = True
                                break
                        if found_link == False:
                            ref_link = {}
                            ref_link["uuid"] = link_item["uuid"]
                            ref_link["counter"] = 0
                            ref_links.append(ref_link)
    elif abs_model == "transparent":
        # creates the list with all the existing links in the test
        for domain_id in range(1, 5):
            # Adding SDN CONTEXT reference links 
            with open('database/SDN_contexts/D'+str(domain_id)+'.json') as json_file:
                data = json.load(json_file)
                for link_item in data['tapi-common:context']['tapi-topology:topology-context']['topology'][0]['link']:
                    ref_link = {}
                    ref_link["uuid"] = link_item["uuid"]
                    ref_link["counter"] = 0
                    ref_links.append(ref_link)
        
            # Adding IDLs context reference links
            with open('database/interdomain-links/vlink_transparent/idl_d'+str(domain_id)+'.json') as json_file:
                data = json.load(json_file)
                for idl_item in data['e2e-topology']['interdomain-links']:
                    for link_item in idl_item['link-options']:
                        found_link = False
                        for ref_link_item in ref_links:
                            if link_item["uuid"] == ref_link_item["uuid"]:
                                found_link = True
                                break
                        if found_link == False:
                            ref_link = {}
                            ref_link["uuid"] = link_item["uuid"]
                            ref_link["counter"] = 0
                            ref_links.append(ref_link)
    else:
        exit()
    
    test_links["ref_links"] = ref_links
    test_links["connections"] = 0
    #print(test_links)

    # creates a list with the used links in the test.
    for domain_id in range(1, 5):
        # Open file using readlines()
        path = 'results/'+abs_model+'_600_400_50/domain'+str(domain_id)+'/log_file_2021-09-25.log'
        file1 = open(path, 'r')
        Lines = file1.readlines()

        #process the log file
        for line in Lines:
            if " TIME LINKS CAPACITY " in line:
                splitted = line.split("-")
                cap_str = splitted[8].replace("GHz", "")
                #print(cap_str)
                """
                if splitted[7] != " [] ":
                    x = line.split("[")
                    x = x[1].split("]")
                    x = x[0].split(",")
                    connection_links = []
                    for x_item in x:
                        x_item = x_item.replace("'", "")
                        x_item = x_item.replace(" ", "")
                        connection_links.append(x_item)
                    used_links.append(connection_links)  
                """ 

            if "ORCH: e2e_cs_json:" in line:
                #print(line[76:])
                cs_string = line[76:]
                cs_string = cs_string.replace("'", '"')
                cs_json = json.loads(cs_string)
                if cs_json["status"] == "DEPLOYED":
                    cs_info = {}
                    connection_links = []
                    cs_counter = cs_counter + 1
                    for route_node_item in cs_json["route-nodes"]:
                        if "link" in route_node_item:
                            if connection_links == []:
                                connection_links.append(route_node_item["link"])
                            else:
                                found_link = False
                                for check_link in connection_links:
                                    if check_link == route_node_item["link"]:
                                        found_link = True
                                        break
                                if found_link == False:
                                    connection_links.append(route_node_item["link"])
                        else:
                            pass
                    cs_info["connection_links"] = connection_links
                    cs_info["capacity"] = int(cap_str)
                    used_links.append(cs_info)
    #print(cs_counter)
    #print(str(len(used_links)))
    #print(str(used_links))


    # applies the count process
    for used_link_item in used_links:
        for used_link_ref in used_link_item["connection_links"]:
            for ref_link_item in test_links["ref_links"]:
                if used_link_ref == ref_link_item["uuid"]:
                    ref_link_item["counter"] = ref_link_item["counter"] + 1
                    ref_link_item["used_capacity"] = ref_link_item["used_capacity"] + used_link_item["capacity"]
                    break
        test_links["connections"] = test_links["connections"] + 1
    
    print(str(test_links))

## FUNCTIONS
# Select function to process the data and present it in a table
#cost_setDomains()
#time_resources()
#cost_E2ECS()
time_deployments()
#links_usage()