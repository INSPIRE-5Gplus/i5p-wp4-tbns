pragma solidity ^0.7.0;
//SPDX-License-Identifier: UNLICENSED

contract transport {
    /*##### CONTEXT SERVICE TEMPLATES #####*/
    struct ContextTemplate{
        //string domain_id;
        string topology;
        uint price;
        string unit;
        address contextOwner;
    }
    mapping(string => ContextTemplate) public ContextTemplate_list;
    string[] public ContextTemplateIds;
    uint ContextTemplateCount;

    /*##### CONNECTIVITY SERVICE INSTANCES #####*/
    struct CSInstance{
        string instance_id;
        string ref_id;
        string source_sip;
        string destination_sip;
        //uint capacity;
        //string capacity_unit;   //Gbps
        //<cidr> constraints ????
        address instantiationClient;
        address contextOwner;
    }

    /*##### CONTEXT TEMPLATE FUNCTIONS #####*/
    // add a new context template
    function addContextTemplate(string memory _templateId, string memory _topology, uint _price, string memory _unit) public returns (bool){
        ContextTemplate_list[_templateId].topology = _topology;
        ContextTemplate_list[_templateId].price = _price;
        ContextTemplate_list[_templateId].unit = _unit;
        ContextTemplate_list[_templateId].contextOwner = msg.sender;   //the nfvo uploading the template info is the owner
        ContextTemplateIds.push(_templateId);
        ContextTemplateCount ++;
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
    function getContextTemplateId(uint _id) public view returns (string memory){
        return ContextTemplateIds[_id];
    }
}