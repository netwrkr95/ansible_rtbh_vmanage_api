#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.viptela import rest_api_lib
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    # Define Ansible module argument spec
    module_args = {
        "vmanage_ip": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "dataprefixes": {"required": True, "type": "list"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        }
    }

    # Instantiate Ansible module object
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Load all the Ansible parameters into local variables\
    vmanage_ip = module.params['vmanage_ip']
    username = module.params['username']
    password = module.params['password']
    name = module.params['name']
    description = module.params['description']
    entries = []
    for dataprefix in module.params['dataprefixes']:
        entries.append({"ipPrefix": str(dataprefix)})
    # Create requests playload for Post and Put methods
    payload = {
        "name": name,
        "description": description,
        "entries": entries
    }

    # Instantiate vmanage requests session
    obj = rest_api_lib(vmanage_ip, username, password)
    # Check if VPN list already exists and get VPN list entries
    listId, current_entries = obj.get_dataprefix_list_by_name(module.params['name'])

    # If the data prefix list does not exist, create it via post
    if not listId:
        if module.check_mode:
            module.exit_json(changed=True)
        response = obj.post_request('template/policy/list/dataprefix', payload=payload)  
        if response.status_code == 200:
            listId = response.json()['listId']
            module.exit_json(changed=True, listId=listId)
        else:
            module.fail_json(msg="Error", listId=listId)
    # If the data prefix list does exist, compare the VPN entries, and if necessary, update via post        
    if listId:
        if current_entries == entries:
            module.exit_json(changed=False, msg="No changes needed", listId=listId)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            obj.put_request('template/policy/list/dataprefix/' + listId, payload=payload)
            module.exit_json(changed=True, msg="Updating list", listId=listId)

if __name__ == '__main__':
    main()
