pragma solidity ^0.8.0;
//SPDX-License-Identifier: UNLICENSED

contract transport {
    /*##### INTERDOMAIN-LINKS INFORMATION #####*/
    /*struct IDLContext{
        //string idl_id;
        string interdomainLink;
        address idlOwner;
    }
    mapping(string => IDLContext) public IDLContext_list;
    address[] public IDLContextIds;
    uint IDLContextCount;*/
    string e2e_topology;

    /*##### DOMAIN CONTEXT INFORMATION #####*/
    struct DomainContext{
        //string domain_id;
        string name_context;
        string sip;
        string nw_topo_serv;
        string topo_metadata;
        string node_topo;
        string link_topo;
        address contextOwner;
    }
    mapping(string => DomainContext) public DomainContext_list;
    string[] public DomainContextIds;
    uint DomainContextCount;

    /*##### CONNECTIVITY SERVICE INSTANCES #####*/
    //TODO: update the structure to have an address, uuid and a status (this struct will be dynamic)
    struct CSInstance{
        string id;
        string cs_info;
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
    event notifyTopologyActions(address owner, string id, string status, string sdn_info, string name_context, string sip, string nw_topo_serv, string topo_metadata, string node_topo, string link_topo);

    /*##### INTER-DOMAIN LINKS FUNCTIONS #####*/
    // add a new set of interd-domain links
    function addIDLContext(string memory _interdomainLink, string memory _e2etop)  public returns (bool){
        //string memory _log = "Inter-Domain Links distributed and E2E Topology updated";
        string memory _status = "NEW_IDL";

        //IDLContext_list[msg.sender].interdomainLink = _interdomainLink;
        //IDLContext_list[msg.sender].idlOwner = msg.sender;
        //IDLContextIds.push(msg.sender);
        //IDLContextCount ++;
        e2e_topology = _e2etop;

        // generates and event for all the peers except the owner to update their E2E view
        emit notifyTopologyActions(msg.sender, "", _status, _interdomainLink, "", "", "", "", "", "");
        
        // generates an event for the owner with the response
        //emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // gets the information of a single context template
    function getE2EContext() public view returns (string memory){
        //string memory _idl = IDLContext_list[_owner].interdomainLink;
        //return (_idl);
        return e2e_topology;
    }
    // gets the number of context templates available in the blockchain
    //function getIDLContextCount() public view returns(uint) {
        //return IDLContextCount;
    //}
    // gets the uuid of the context template in position i (used when to get ALL context templates)
    //function getIDLContextId(uint _index) public view returns (string memory){
        //return IDLContextIds[_index];
    //}
    //TODO: DELETE IDL element

    /*##### DOMAIN CONTEXT FUNCTIONS #####*/
    // add a new domain context template
    function addContextTemplate(string memory id, string memory name_context, string memory sip, string memory nw_topo_serv, string memory topo_metadata, string memory node_topo, string memory link_topo) public returns (bool){
        //string memory _log = "SDN domain added.";
        string memory status = "NEW_DOMAIN";

        DomainContext_list[id].name_context = name_context;
        DomainContext_list[id].sip = sip;
        DomainContext_list[id].nw_topo_serv = nw_topo_serv;
        DomainContext_list[id].topo_metadata = topo_metadata;
        DomainContext_list[id].node_topo = node_topo;
        DomainContext_list[id].link_topo = link_topo;
        DomainContext_list[id].contextOwner = msg.sender;  //the peer uploading the template info is the owner
        DomainContextIds.push(id);
        DomainContextCount ++;

        // all the peers except the owner will take this event
        emit notifyTopologyActions(msg.sender, id, status, '', name_context, sip, nw_topo_serv, topo_metadata, node_topo, link_topo);
        
        //sends back to the client the response
        //emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // gets the information of a single domain context
    function getContextTemplate(string memory _id) public view returns (string memory, string memory, string memory, string memory, string memory, string memory, address){
        string memory name_context = DomainContext_list[_id].name_context;
        string memory sip = DomainContext_list[_id].sip;
        string memory nw_topo_serv = DomainContext_list[_id].nw_topo_serv;
        string memory topo_metadata = DomainContext_list[_id].topo_metadata;
        string memory node_topo = DomainContext_list[_id].node_topo;
        string memory link_topo = DomainContext_list[_id].link_topo;
        address _own = DomainContext_list[_id].contextOwner;
        
        /*return string(abi.encodePacked(a, b, c, d, e));*/

        return (name_context, sip, nw_topo_serv, topo_metadata, node_topo, link_topo, _own);
    }
    // gets the number of domain contexts available in the blockchain
    function getContextTemplateCount() public view returns(uint) {
        return DomainContextCount;
    }
    // gets the uuid of the domain context in position i (used when to get ALL context templates)
    function getContextTemplateId(uint _index) public view returns (string memory){
        return DomainContextIds[_index];
    }
    // TODO: remove specific domain context

    /*##### CONNECTIVITY SERVICE INSTANCES FUNCTIONS #####*/
    // generates an event to deploy a connectivity service
    //TODO: when needing more parameters to configure a CS, use a json as string
    function instantiateConnectivityService(address _contextOwner, string memory _cs_info, string memory _id) public returns (bool){
        string memory _status = "NEW";
        string memory _log = "Connectivity Service requested.";

        CSInstance_list[_id].id = _id;
        CSInstance_list[_id].cs_info = _cs_info;
        CSInstance_list[_id].instantiationClient = msg.sender;
        CSInstance_list[_id].contextOwner = _contextOwner;
        CSInstance_list[_id].status = _status;
        CSInstanceIds.push(_id);
        CSInstanceCount ++;
        
        //generates event to deploy connectivity service
        emit notifyTopologyActions(_contextOwner, _id, _status, _cs_info, "", "", "", "", "", "");
            
        //sends back to the client the response and 
        emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // generates an event to deploy a connectivity service
    function updateConnectivityService(string memory _id, string memory _cs_info, string memory _status) public returns (bool){
        string memory _log = "Connectivity Service Updated.";
        CSInstance_list[_id].cs_info = _cs_info;
        CSInstance_list[_id].status = _status;

        // generates event to update the connectivity service info requested by another domain
        emit notifyTopologyActions(CSInstance_list[_id].instantiationClient, _id, CSInstance_list[_id].status, CSInstance_list[_id].cs_info, "", "", "", "", "", "");
        
        //sends back to the client the response and 
        emit topology_response(msg.sender, _log, _status);
        return true;
    }
}