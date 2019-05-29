#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.viptela_cookie import rest_api_lib
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    # Define Ansible module argument spec
    module_args = {
        "vmanage_ip": {"required": True, "type": "str"},
        "cookie": {"required": True, "type": "str"}
    }

    # Instantiate Ansible module object
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Load all the Ansible parameters into local variables\
    vmanage_ip = module.params['vmanage_ip']
    cookie = module.params['cookie']

    # Instantiate vmanage requests session
    obj = rest_api_lib(vmanage_ip, cookie)

    # Create requests playload for Post and Put methods
    payload = "{\n    \"deviceTemplateList\": [{\n        \"templateId\": \"b1b3d1d4-8890-4e96-b586-c014f4f6d225\",\n        \"device\": [{\n            \"csv-status\": \"complete\",\n            \"csv-deviceId\": \"623b52d8-82a3-4bcb-87d9-346acc0bbb15\",\n            \"csv-deviceIP\": \"10.255.255.3\",\n            \"csv-host-name\": \"vsmart1\",\n            \"//system/host-name\": \"vsmart1\",\n            \"//system/system-ip\": \"10.255.255.3\",\n            \"//system/site-id\": \"1\",\n            \"/0/eth0/interface/ip/address\": \"199.66.188.83/26\",\n            \"csv-templateId\": \"b1b3d1d4-8890-4e96-b586-c014f4f6d225\"\n        }],\n        \"isEdited\": true,\n        \"isMasterEdited\": false\n    }]\n}"

    response = obj.post_request2('template/device/config/attachfeature', payload=payload)
    module.exit_json(changed=True, msg="Updating Vsmart Policy")

if __name__ == '__main__':
    main()
