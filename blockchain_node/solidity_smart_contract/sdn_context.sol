pragma solidity ^0.7.0;
//SPDX-License-Identifier: UNLICENSED

contract transport {
    /*##### CONTEXT SERVICE TEMPLATES #####*/
    struct ContextTemplate{
        //string domain_id;
        string context;
        uint price;
        string unit;
        address contextOwner;
    }
    mapping(string => ContextTemplate) public ContextTemplate_list;
    string[] public ContextTemplateIds;
    uint ContextTemplateCount;

    /*##### CONNECTIVITY SERVICE INSTANCES #####*/
    //TODO: update the structure to have an address, uuid and a status (this struct will be dynamic)
    struct CSInstance{
        string id;
        string instance_id;
        string vl_ref;
        string config_params;
        //string source_sip;
        //string destination_sip;
        //string cidr;
        //uint capacity;
        //string capacity_unit;   //Gbps
        string status;
        address instantiationClient;
        address contextOwner;
    }
    mapping(string => CSInstance) public CSInstance_list;
    string[] public CSInstanceIds;
    uint CSInstanceCount;

    /*##### EVENTS #####*/
    //event templateRemoved (string log);
    event topology_response(address requester, string log, string status);
    event notifyTopologyActions(address owner, string id, string vl_ref, string instance_id, string status, string context, string config_params);

    /*##### CONTEXT TEMPLATE FUNCTIONS #####*/
    // add a new context template
    function addContextTemplate(string memory _id, string memory _context, uint _price, string memory _unit) public returns (bool){
        string memory _log = "SDN domain added.";
        string memory _status = "NEW_DOMAIN";

        ContextTemplate_list[_id].context = _context;
        ContextTemplate_list[_id].price = _price;
        ContextTemplate_list[_id].unit = _unit;
        ContextTemplate_list[_id].contextOwner = msg.sender;   //the nfvo uploading the template info is the owner
        ContextTemplateIds.push(_id);
        ContextTemplateCount ++;

        // all the peers except the owner will take this event
        emit notifyTopologyActions(msg.sender, _id, "", "", _status, _context, "");
        
        //sends back to the client the response
        emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // TODO: remove specific context template
    function deactivateContextTemplate(string memory _templateId) public returns(bool){
        // TODO: add a status parameter in the strcut to deactivate when a domain wants to leave the blockchain
    }
    // gets the information of a single context template
    function getContextTemplate(string memory _templateId) public view returns (string memory, uint, string memory, address){
        string memory _top = ContextTemplate_list[_templateId].topology;
        uint _pri = ContextTemplate_list[_templateId].price;
        string memory _uni = ContextTemplate_list[_templateId].unit;
        address _own = ContextTemplate_list[_templateId].contextOwner;
        return (_top, _pri, _uni, _own);
    }
    // gets the number of context templates available in the blockchain
    function getContextTemplateCount() public view returns(uint) {
        return ContextTemplateCount;
    }
    // gets the uuid of the context template in position i (used when to get ALL context templates)
    function getContextTemplateId(uint _index) public view returns (string memory){
        return ContextTemplateIds[_index];
    }

    /*##### CONNECTIVITY SERVICE INSTANCES FUNCTIONS #####*/
    // generates an event to deploy a connectivity service
    //TODO: when needing more parameters to configure a CS, use a json as string
    function instantiateConnectivityService(address _contextOwner, string memory _id, string memory _vl_ref,  string memory _config_params) public returns (bool){
        string memory _status = "NEW";
        string memory _log = "Connectivity Service requested.";

        CSInstance_list[_id].id = _id;
        CSInstance_list[_id].vl_ref = _vl_ref;
        CSInstance_list[_id].instance_id = "";
        CSInstance_list[_id].config_params = _config_params;
        CSInstance_list[_id].instantiationClient = msg.sender;
        CSInstance_list[_id].contextOwner = _contextOwner;
        CSInstance_list[_id].status = _status;
        CSInstanceIds.push(_id);
        CSInstanceCount ++;
        
        //generates event to deploy connectivity service
        emit notifyTopologyActions(_contextOwner, _id, _vl_ref, "", _status, "", _config_params);
            
        //sends back to the client the response and 
        emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // generates an event to deploy a connectivity service
    function updateConnectivityService(string memory _id, string memory _instanceId, string memory _status) public returns (bool){
        string memory _log = "Connectivity Service Updated.";
        CSInstance_list[_id].instance_id = _instanceId;
        CSInstance_list[_id].status = _status;

        // generates event to update the connectivity service info requested by another domain
        emit notifyTopologyActions(CSInstance_list[_id].instantiationClient, _id, CSInstance_list[_id].vl_ref, _instanceId, _status, "", "");
        
        //sends back to the client the response and 
        emit topology_response(msg.sender, _log, _status);
        return true;
    }
}