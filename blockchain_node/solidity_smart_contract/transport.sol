pragma solidity ^0.8.0;
//SPDX-License-Identifier: UNLICENSED

contract transport {
    /*##### INTERDOMAIN-LINKS INFORMATION #####*/
    string e2e_topology;

    /*##### DOMAIN CONTEXT INFORMATION  plus SIPs, Nodes and Links #####*/
    struct DomainContext{
        //string domain_id;
        string name_context;
        string sip;                 //list of sip uuids
        string nw_topo_serv;
        string topo_metadata;
        string node_topo;           //list of nodes uuids
        string link_topo;           //list of links uuids
        address contextOwner;
    }
    mapping(string => DomainContext) public DomainContext_list;
    string[] public DomainContextIds;
    uint DomainContextCount;
    
    struct SIPs{
        //string sip_id;
        string sip_info;
        address sipOwner;
    }
    mapping(string => SIPs) public SIPs_list;
    string[] public SIPsIds;
    uint SIPsCount;
    
    struct Nodes{
        //string nodeid;
        string node_name;
        string neps_topo;           //list of neps uuids
        address nodeOwner;
    }
    mapping(string => Nodes) public Nodes_list;
    string[] public NodesIds;
    uint NodesCount;
    
    struct NEPs{
        //string nepid;
        string nep_info;
        address nepOwner;
    }
    mapping(string => NEPs) public NEPs_list;
    string[] public NEPsIds;
    uint NEPsCount;
    
    struct Links{
        //string link_id;
        string link_info;
        address linkOwner;
    }
    mapping(string => Links) public Links_list;
    string[] public LinksIds;
    uint LinksCount;

    /*##### CONNECTIVITY SERVICE INSTANCES #####*/
    //TODO: update the structure to have an address, uuid and a status (this struct will be dynamic)
    struct CSInstance{
        string id;
        string cs_info;
        string spectrum;
        string capacity;
        string status;
        address instantiationClient;
        address contextOwner;
    }
    mapping(string => CSInstance) public CSInstance_list;
    string[] public CSInstanceIds;
    uint CSInstanceCount;

    /*##### EVENTS #####*/
    event topology_response(address requester, string log, string status);
    event notifyTopologyActions(address owner, string id, string status, string sdn_info, string name_context, string sip, string nw_topo_serv, string topo_metadata, string node_topo, string link_topo);

    /*##### INTER-DOMAIN LINKS FUNCTIONS #####*/
    // add a new set of interd-domain links
    function addIDLContext(string memory _interdomainLink, string memory _e2etop)  public returns (bool){
        //string memory _log = "Inter-Domain Links distributed and E2E Topology updated";
        string memory _status = "NEW_IDL";

        e2e_topology = _e2etop;

        // generates and event for all the peers except the owner to update their E2E view
        emit notifyTopologyActions(msg.sender, "", _status, _interdomainLink, "", "", "", "", "", "");
        
        // generates an event for the owner with the response
        //emit topology_response(msg.sender, _log, _status);
        return true;
    }
    // gets the information of a single context template
    function getE2EContext() public view returns (string memory){
        return e2e_topology;
    }
    // update e2e_topology
    function updateE2EContext(string memory _e2e_topology) public returns (bool){
        //the _id is a composition of the context uuid, the node uuid and the nep uuid
        e2e_topology = _e2e_topology;
        return true;
    }

    /*##### DOMAIN CONTEXT FUNCTIONS #####*/
    // add a new domain context template
    function addContextTemplate(string memory _id, string memory name_context, string memory sip, string memory nw_topo_serv, string memory topo_metadata, string memory node_topo, string memory link_topo) public returns (bool){
        string memory status = "NEW_DOMAIN";
        
        DomainContext_list[_id].name_context = name_context;
        DomainContext_list[_id].sip = sip;
        DomainContext_list[_id].nw_topo_serv = nw_topo_serv;
        DomainContext_list[_id].topo_metadata = topo_metadata;
        DomainContext_list[_id].node_topo = node_topo;
        DomainContext_list[_id].link_topo = link_topo;
        DomainContext_list[_id].contextOwner = msg.sender;  //the peer uploading the template info is the owner
        DomainContextIds.push(_id);
        DomainContextCount ++;
        
        // all the peers except the owner will take this event
        emit notifyTopologyActions(msg.sender, _id, status, '', name_context, sip, nw_topo_serv, topo_metadata, node_topo, link_topo);
        //emit notifyTopologyActions(msg.sender, _id, _status, "", "", "", "", "", "", "");

        //sends back to the client the response
        //emit topology_response(msg.sender, _log, _status);

        return true;
    }
    // add a new sip
    function addSip(string memory _id, string memory sip_info) public returns (bool){
        //the _id is a composition of the context uuid and the sip uuid
        SIPs_list[_id].sip_info = sip_info;
        SIPs_list[_id].sipOwner = msg.sender;  //the peer uploading the sip info is the owner
        SIPsIds.push(_id);
        SIPsCount ++;
        return true;
    }
    // update a sip
    function updateSip(string memory _id, string memory sip_info) public returns (bool){
        //the _id is a composition of the context uuid, the node uuid and the nep uuid
        SIPs_list[_id].sip_info = sip_info;
        return true;
    }
    // add a new node
    function addNode(string memory _id, string memory node_name, string memory neps_topo) public returns (bool){
        //the _id is a composition of the context uuid and the node uuid
        Nodes_list[_id].node_name = node_name;
        Nodes_list[_id].neps_topo = neps_topo;
        Nodes_list[_id].nodeOwner = msg.sender;  //the peer uploading the node info is the owner
        NodesIds.push(_id);
        NodesCount ++;
        return true;
    }
    // add a new nep
    function addNep(string memory _id, string memory nep_info) public returns (bool){
        //the _id is a composition of the context uuid and the node uuid
        NEPs_list[_id].nep_info = nep_info;
        NEPs_list[_id].nepOwner = msg.sender;  //the peer uploading the node info is the owner
        NEPsIds.push(_id);
        NEPsCount ++;
        return true;
    }
    // update a nep
    function updateNep(string memory _id, string memory nep_info) public returns (bool){
        //the _id is a composition of the context uuid, the node uuid and the nep uuid
        NEPs_list[_id].nep_info = nep_info;
        return true;
    }
    // add a new link
    function addLink(string memory _id, string memory link_info) public returns (bool){
        //the _id is a composition of the context uuid and the link uuid
        Links_list[_id].link_info = link_info;
        Links_list[_id].linkOwner = msg.sender;  //the peer uploading the link info is the owner
        LinksIds.push(_id);
        LinksCount ++;
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
    // gets the information of a single sip
    function getSIP(string memory _id) public view returns (string memory){
        string memory sip = SIPs_list[_id].sip_info;
        return (sip);
    }
    // gets the information of a single node
    function getNode(string memory _id) public view returns (string memory, string memory){
        string memory node_name = Nodes_list[_id].node_name;
        string memory neps_topo = Nodes_list[_id].neps_topo;
        return (node_name, neps_topo);
    }
    // gets the number of nodes
    function getNodeCount() public view returns(uint) {
        return NodesCount;
    }
    // gets the information of a single nep
    function getNep(string memory _id) public view returns (string memory){
        string memory nep = NEPs_list[_id].nep_info;
        return (nep);
    }
    // gets the information of a single link
    function getLink(string memory _id) public view returns (string memory){
        string memory link = Links_list[_id].link_info;
        return (link);
    }

    /*##### CONNECTIVITY SERVICE INSTANCES FUNCTIONS #####*/
    // generates an event to deploy a connectivity service
    //TODO: when needing more parameters to configure a CS, use a json as string
    //(address, cs_json["uuid"], cs_string, spectrum_string, capacity_string)
    function instantiateConnectivityService(address _contextOwner, string memory _id, string memory _cs_info, string memory _spectrum, string memory _capacity) public returns (bool){
        string memory _status = "NEW";
        string memory _log = "Connectivity Service requested.";

        CSInstance_list[_id].id = _id;
        CSInstance_list[_id].cs_info = _cs_info;
        CSInstance_list[_id].spectrum = _spectrum;
        CSInstance_list[_id].capacity = _capacity;
        CSInstance_list[_id].instantiationClient = msg.sender;
        CSInstance_list[_id].contextOwner = _contextOwner;
        CSInstance_list[_id].status = _status;
        CSInstanceIds.push(_id);
        CSInstanceCount ++;
        
        //generates event to deploy connectivity service
        emit notifyTopologyActions(_contextOwner, _id, _status, _cs_info, _spectrum, "", "", _capacity, "", "");
            
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