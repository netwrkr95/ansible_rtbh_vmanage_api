"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage

Note: All the three arguments are manadatory
"""
import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from Cookie import SimpleCookie

class rest_api_lib:
    def __init__(self, vmanage_ip, rawcookie):
        self.vmanage_ip = vmanage_ip

        simplecookie = SimpleCookie()
        simplecookie.load(rawcookie)

        cookie = {}
        for key, morsel in simplecookie.items():
            cookie[key] = morsel.value

        self.session = requests.session()
        self.session.cookies.update(cookie)

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:8443/dataservice/%s" % (self.vmanage_ip, mount_point)
        response = self.session.get(url, verify=False)
        data = response.content
        return response

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:8443/dataservice/%s" % (self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        response = self.session.post(url=url, data=payload, headers=headers, verify=False)
        return response

    def post_request2(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:8443/dataservice/%s" % (self.vmanage_ip, mount_point)
        response = self.session.post(url=url, data=payload, headers=headers, verify=False)
        return response

    def put_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """PUT request"""
        url = "https://%s:8443/dataservice/%s" % (self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        response = self.session.put(url=url, data=payload, headers=headers, verify=False)
        return response

    def get_vpn_list_by_name(self, name):
        response = self.get_request('template/policy/list/vpn')
        vpn_lists = response.json()['data']
        for vpn_list in vpn_lists:
            if vpn_list['name'] == name:
                return vpn_list['listId'], vpn_list['entries']
        return None, None

    def get_site_list_by_name(self, name):
        response = self.get_request('template/policy/list/site')
        site_lists = response.json()['data']
        for site_list in site_lists:
            if site_list['name'] == name:
                return site_list['listId'], site_list['entries']
        return None, None

    def get_dataprefix_list_by_name(self, name):
        response = self.get_request('template/policy/list/dataprefix')
        dataprefix_lists = response.json()['data']
        for dataprefix_list in dataprefix_lists:
            if dataprefix_list['name'] == name:
                return dataprefix_list['listId'], dataprefix_list['entries']
        return None, None

    def get_topology_by_name(self, name):
        response = self.get_request('template/policy/definition/hubandspoke')
        topologies = response.json()['data']
        for topology in topologies:
            if topology['name'] == name:
                return topology['definitionId']
        return None

    def get_topology_details(self, definitionId):
        response = self.get_request('template/policy/definition/hubandspoke/' + definitionId)
        definition = response.json()
        vpn_listId = definition['definition']['vpnList']
        spoke_listId = definition['definition']['subDefinitions'][0]['spokes'][0]['siteList']
        hub_listId = definition['definition']['subDefinitions'][0]['spokes'][0]['hubs'][0]['siteList']
        return vpn_listId, spoke_listId, hub_listId

    def get_vsmart_policyId_by_name(self, name):
        response = self.get_request('template/policy/vsmart')
        policies = response.json()['data']
        for policy in policies:
            if policy['policyName'] == name:
                policyId = policy['policyId']
                topologyId = json.loads(policy['policyDefinition'])['assembly'][0]['definitionId']
                isactivated = policy['isPolicyActivated']
                return policyId, topologyId, isactivated
        return None, None, None

    def get_app_list_by_name(self, name):
        response = self.get_request('template/policy/list/app')
        app_lists = response.json()['data']
        for app_list in app_lists:
            if app_list['name'] == name:
                return app_list['listId'], app_list['entries']
        return None, None