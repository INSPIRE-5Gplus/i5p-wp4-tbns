pragma solidity ^0.8.0;
//SPDX-License-Identifier: UNLICENSED

contract Slicing {
    /*##### SLICE TEMPLATE #####*/
    //TODO: add a new variable having all the nst_json as string.
    struct SliceTemplate {
        //string templateId;     //085a72f3-04d4-4cfd-86bf-cd0f66d38e75  //used as the mapping KEY
        string name;            //firewall
        string version;         //2.1
        string vendor;          //cttc
        uint price;             // we will always work with ether
        string unit;            //unit of the price
        address templateOwner;      //address of the node uploading the slice template
    }
    mapping(string => SliceTemplate) public sliceTemplate_list;
    string[] public sliceTemplateIds;
    uint sliceTemplateCount;
    
    /*##### SLICE INSTANCES #####*/
    //TODO: add a new variable having all the nsi_json as string.
    struct SliceInstance{
        string sliceInstanceId;         //instantiation uuid
        string sliceTemplateId;         //slice template uuid
        string status;                  //[INSTANTIATING, INSTANTIATED, TERMINATING, TERMINATED, ERROR]
        string log;                     //to inform in case of error
        string nfvicp_cidr;             //data flow IP range
        string nfvicp_sip;              //sip element to get in/out the data flow
        address instantiationClient;    //node address requesting the instantiation (only this should be able to terminate)
        address templateOwner;          //node address deploying the instantiation
    }
    mapping(string => SliceInstance) public sliceInstances_list; //the key to each value is requestId given by the requester
    string[] public sliceInstancesIds;
    uint sliceInstancesCount;

    /*##### EVENTS #####*/
    event templateRemoved (string log);
    event slice_response(address requester, string log, string status);
    event notifySliceInstanceActions(address owner, string templateId, string instanceId, string status);

    /*##### SLICE TEMPLATE FUNCTIONS #####*/
    // add a new slice template
    function addSliceTemplate(string memory _templateId, string memory _name, string memory _version, string memory _vendor, uint _price, string memory _unit) public returns (bool){
        sliceTemplate_list[_templateId].name = _name;
        sliceTemplate_list[_templateId].version = _version;
        sliceTemplate_list[_templateId].vendor = _vendor;
        sliceTemplate_list[_templateId].price = _price;
        sliceTemplate_list[_templateId].unit = _unit;
        sliceTemplate_list[_templateId].templateOwner = msg.sender;   //the nfvo uploading the template info is the owner
        sliceTemplateIds.push(_templateId);
        sliceTemplateCount ++;
        return true;
    }
    //WRONG NAME AND WAY OF DOING!!!! AN ELEMENT CANNOT BE REMOVED BUT IT MUST BE DEACTIVATED!!!
    // remove specific slice template
    function removeSliceTemplate(string memory _templateId) public returns(bool){
        string memory _log;
        if (sliceTemplate_list[_templateId].templateOwner == msg.sender){
            delete sliceTemplate_list[_templateId];
            
            // ### the following piece of code is to re-adapt the sliceTemplateIds array ###
            // look for the key that correspond to the remove value service ID
            uint found_id;
            for (uint i = 0; i < sliceTemplateIds.length-1; i++){
                if ((keccak256(abi.encodePacked(sliceTemplateIds[i]))) == (keccak256(abi.encodePacked(_templateId)))){
                    found_id = i;
                    break;
                }
            }
            // substitutes the element to delete witht the next one in the array
            for (uint i = found_id; i < sliceTemplateIds.length-1; i++){
                sliceTemplateIds[i] = sliceTemplateIds[i+1];
            }
            // once all elements are move to the previous position within the array, reduces the array lenght
            delete sliceTemplateIds[sliceTemplateIds.length-1];
            sliceTemplateCount --;
            _log = "Slice Template Removed";
        } else {
            _log = "ERROR: Only the owner can remove this slice template";
        }
        emit templateRemoved(_log);
        return true;
    }
    // gets the information of a single slice template
    function getSliceTemplate(string memory _templateId) public view returns (string memory, string memory, string memory, uint, string memory, address){
        string memory _nam = sliceTemplate_list[_templateId].name;
        string memory _ver = sliceTemplate_list[_templateId].version;
        string memory _ven = sliceTemplate_list[_templateId].vendor;
        uint _pri = sliceTemplate_list[_templateId].price;
        string memory _uni = sliceTemplate_list[_templateId].unit;
        address _own = sliceTemplate_list[_templateId].templateOwner;
        return (_nam, _ver, _ven, _pri, _uni, _own);
    }
    // gets the number of slice templates available in the blockchain
    function getSliceTemplateCount() public view returns(uint) {
        return sliceTemplateCount;
    }
    // gets the uuid of the slice template in position i (used when user requests get ALL slice templates)
    function getSliceTemplateId(uint _id) public view returns (string memory){
        return sliceTemplateIds[_id];
    }
    // check if a slice template exists based on name/version/vendor
    function sliceTemplateExistance (string memory _name, string memory _version, string memory _vendor) public view returns(bool) {
        bool template_found;
        for (uint i = 0; i < sliceTemplateCount; i++){
            string memory _templateId = sliceTemplateIds[i];
            string memory tem_name = sliceTemplate_list[_templateId].name;
            string memory tem_version = sliceTemplate_list[_templateId].version;
            string memory tem_vendor = sliceTemplate_list[_templateId].vendor;

            // not possible to compare string, but hashs
            if (
                (keccak256(abi.encodePacked(_name)) == keccak256(abi.encodePacked(tem_name))) &&
                (keccak256(abi.encodePacked(_version)) == keccak256(abi.encodePacked(tem_version))) &&
                (keccak256(abi.encodePacked(_vendor)) == keccak256(abi.encodePacked(tem_vendor)))
                ){
                template_found = true;
                break;
            }
            template_found = false;
        }
        return template_found;
    }

    /*##### SLICE INSTANCES FUNCTIONS #####*/
    // request slice instantiation
    function instantiateSlice (string memory _sliceInstanceId, string memory _sliceTemplateId) public returns (bool){
        address _own = sliceTemplate_list[_sliceTemplateId].templateOwner;
        address _requester = msg.sender;
        string memory _log;
        string memory _status;
        
        if (sliceTemplate_list[_sliceTemplateId].templateOwner != msg.sender){
            _log = "Deploying Service Requested.";
            _status = "INSTANTIATING";
        
            //NOTE: the value sliceInstanceId is aaded by the owner when ready.
            sliceInstances_list[_sliceInstanceId].sliceInstanceId = _sliceInstanceId;
            sliceInstances_list[_sliceInstanceId].sliceTemplateId = _sliceTemplateId;
            sliceInstances_list[_sliceInstanceId].status = _status;
            sliceInstances_list[_sliceInstanceId].log = _log;
            sliceInstances_list[_sliceInstanceId].instantiationClient = _requester;
            sliceInstances_list[_sliceInstanceId].templateOwner = _own;
            sliceInstancesIds.push(_sliceInstanceId);
            sliceInstancesCount ++;
            
            // warns all peers but only the template owner takes it to instantiate it
            emit notifySliceInstanceActions(_own, _sliceTemplateId, _sliceInstanceId, _status);
        } else {
            _log = "You are the owner of the template, use your local resources.";
            _status = "ERROR";
        }
        //sends back to the client the response and 
        emit slice_response(_requester, _log, _status);
        return true;
    }
    // request slice termination
    function terminateSlice (string memory _sliceInstanceId) public returns (bool){
        address _own = sliceInstances_list[_sliceInstanceId].templateOwner;
        string memory _sliceTemplateId = sliceInstances_list[_sliceInstanceId].sliceTemplateId;
        string memory _log;
        string memory _status;
        
        if (sliceInstances_list[_sliceInstanceId].instantiationClient == msg.sender){
            _log = "Requested to be terminated.";
            _status = "TERMINATING";
            sliceInstances_list[_sliceInstanceId].status = _status;
            sliceInstances_list[_sliceInstanceId].log = _log;
            emit notifySliceInstanceActions(_own, _sliceTemplateId, _sliceInstanceId, _status);
        } else {
            _log = "Not possible to terminate this instantiation, you are not the owner.";
            _status = "ERROR";
        }
        emit slice_response(msg.sender, _log, _status);
        return true;
    }
    // gets the information of a single slice instantiation
    function getSliceInstance(string memory _sliceInstanceId) public view returns (string memory, string memory, string memory, string memory, address, address){
        sliceInstances_list[_sliceInstanceId].sliceInstanceId;
        string memory _sliceTemplateId = sliceInstances_list[_sliceInstanceId].sliceTemplateId;
        string memory _status = sliceInstances_list[_sliceInstanceId].status;
        string memory _log = sliceInstances_list[_sliceInstanceId].log;
        address _instantiationClient = sliceInstances_list[_sliceInstanceId].instantiationClient;
        address _templateOwner = sliceInstances_list[_sliceInstanceId].templateOwner;
        return (_sliceInstanceId, _sliceTemplateId, _status, _log, _instantiationClient, _templateOwner);
    }
    // gets the number of slice instances
    function getSliceInstancesCount() public view returns(uint) {
        return sliceInstancesCount;
    }
    // gets the uuid of the slice instantiation in position i (used when get ALL nsi is requested)
    function getSliceInstanceId(uint _id) public view returns (string memory){
        return sliceInstancesIds[_id];
    }
    // updates the status of an instance element
    function updateInstance (string memory _instanceId, string memory _status, string memory _log) public returns (bool){
        address _instanceOwner = sliceInstances_list[_instanceId].instantiationClient;
        address _templateOwner = sliceInstances_list[_instanceId].templateOwner;
        string memory _templateId = sliceInstances_list[_instanceId].sliceTemplateId;
        if (_templateOwner == msg.sender){
            if(keccak256(abi.encodePacked(_status)) == keccak256(abi.encodePacked("INSTANTIATED"))){
                sliceInstances_list[_instanceId].status = _status;
                sliceInstances_list[_instanceId].log = _log;
                _log = "User informed about the slice instantiation.";
            } else if (keccak256(abi.encodePacked(_status)) == keccak256(abi.encodePacked("TERMINATED"))) {
                sliceInstances_list[_instanceId].status = _status;
                sliceInstances_list[_instanceId].log = _log;
                _log = "User informed about the slice termination.";
            } else {
                //ERROR
                sliceInstances_list[_instanceId].status = _status;
                sliceInstances_list[_instanceId].log = _log;
            }
            emit notifySliceInstanceActions(_instanceOwner, _templateId, _instanceId, _status);
        } else {
            _log = "You're NOT the owner, you cannot modify it!";
            _status = "ERROR";
        }
        emit slice_response(_templateOwner, _log, _status);
        return false;
    }
}