'''
JSON schemas used by playnetmano httpserver.py module to parse the different files and messages sent through the API 
'''

#Basis schemas
nameshort_schema={"type" : "string", "minLength":1, "maxLength":24, "pattern" : "^[^,;()'\"]+$"}
name_schema={"type" : "string", "minLength":1, "maxLength":1024, "pattern" : "^[^,;()'\"]+$"}
xml_text_schema={"type" : "string", "minLength":1, "maxLength":2000, "pattern" : "^[^']+$"}
description_schema={"type" : ["string","null"], "maxLength":200, "pattern" : "^[^'\"]+$"}
id_schema_fake = {"type" : "string", "minLength":2, "maxLength":36 }  #"pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
id_schema = {"type" : "string", "pattern": "^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$"}
pci_schema={"type":"string", "pattern":"^[0-9a-fA-F]{4}(:[0-9a-fA-F]{2}){2}\.[0-9a-fA-F]$"}
http_schema={"type":"string", "pattern":"^https?://[^'\"=]+$"}
bandwidth_schema={"type":"string", "pattern" : "^[0-9]+ *([MG]bps)?$"}
memory_schema={"type":"string", "pattern" : "^[0-9]+ *([MG]i?[Bb])?$"}
integer0_schema={"type":"integer","minimum":0}
integer1_schema={"type":"integer","minimum":1}
path_schema={"type":"string", "pattern":"^(\.(\.?))?(/[^/"":{}\ \(\)]+)+$"}
vlan_schema={"type":"integer","minimum":1,"maximum":4095}
vlan1000_schema={"type":"integer","minimum":1000,"maximum":4095}
mac_schema={"type":"string", "pattern":"^[0-9a-fA-F][02468aceACE](:[0-9a-fA-F]{2}){5}$"}  #must be unicast LSB bit of MSB byte ==0 
ip_schema={"type":"string","pattern":"^([0-9]{1,3}.){3}[0-9]{1,3}$"}
port_schema={"type":"integer","minimum":1,"maximum":65534}
metadata_schema={
    "type":"object",
    "properties":{
        "architecture": {"type":"string"},
        "use_incremental": {"type":"string","enum":["yes","no"]},
        "vpci": pci_schema,
        "os_distro": {"type":"string"},
        "os_type": {"type":"string"},
        "os_version": {"type":"string"},
        "bus": {"type":"string"}
    }
}


#Schema for the configuration file
config_schema = {
    "title":"configuration response information schema",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type":"object",
    "properties":{
        "http_port": port_schema,
        "http_host": name_schema,
        "nfvo_db_host": name_schema,
        "nfvo_db_user": name_schema,
        "nfvo_db_passwd": {"type":"string"},
        "nfvo_db_name": name_schema,
        "vnfm_db_host": name_schema,
        "vnfm_db_user": name_schema,
        "vnfm_db_passwd": {"type": "string"},
        "vnfm_db_name": name_schema,
        "nfvo_log_path": name_schema,
        "nfvo_log_file_size": integer0_schema,
        "nfvo_log_file_num": integer0_schema,
        "nfvo_log_level": name_schema,
        "vnfm_log_path": name_schema,
        "vnfm_log_file_size": integer0_schema,
        "vnfm_log_file_num": integer0_schema,
        "vnfm_log_level": name_schema,
        "vim_ip": name_schema,
        "vim_port": port_schema,
    },
    "required": ['nfvo_db_host', 'nfvo_db_user', 'nfvo_db_passwd', 'nfvo_db_name', 'vnfm_db_host', 'vnfm_db_user', 'vnfm_db_passwd', 'vnfm_db_name'],
    "additionalProperties": False
}

