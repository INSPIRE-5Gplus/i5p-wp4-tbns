#!/usr/local/bin/python3.4

#temporary database for Network Slice Instances
nsi_db=[]

#temporary database for connectivity services
cs_db=[]


def update_db(element_id, db_element, selected_db):
    if selected_db == "slices":
        for nsi_element in nsi_db:
            if nsi_element['id'] == element_id:
                # TODO: verify if this overwrite all the element with the updated one
                nsi_element = db_element
    elif selected_db == "conn_services":
        pass
    else:
        # TODO:error management
        pass