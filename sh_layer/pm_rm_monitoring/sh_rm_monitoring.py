#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import collections
import re
import json
import ast

from novaclient import client as novaclient
from neutronclient.neutron import client as neutronclient
import cinderclient.v1.client as cinderclient
import keystoneclient.v2_0.client as keystoneclient
import swiftclient.client as swiftclient

from keystoneauth1.identity import v2
from keystoneauth1 import session

from sh_layer import vimconn
from sh_layer import vimconn_openstack
import resource_db



# Print unicode text to the terminal
reload(sys)
sys.setdefaultencoding("utf-8")

# --
# All Globals should be defined here
#
global global_config
global_config = {'db_host': '116.89.184.43',
                  'db_user': 'root',
                  'db_passwd': '',
                  'db_name': 'mano_db'
                 }

os_username = 'admin'
os_password = 'fncp2015'
os_auth_url = 'http://129.254.39.208:5000/v2.0/'
_debug = False
# new para
os_url = 'http://129.254.39.208:35357/v2.0'


#Static flavors list
flavorListDefault = [
    'm1.tiny',
    'm1.small',
    'm1.medium',
    'm1.large',
    'm1.xlarge',
    'm1.2xlarge',
    'm1.4xlarge',
    'm1.8xlarge'
]

def __remove_quotes_in_quotas_limits_list(data):
    '''remove single quotes ' of list of quotas and limits'''
    for k in data:
        if type(k) == str:
            if "'" in k:
                data[k] = data[k].replace("'","")
    return data

def __remove_quotes_dict(data):
    '''remove single quotes ' of any string content of data dictionary'''
    for k,v in data.items():
        if type(k) == str:
            if "" in v:
                data[k] = data[k].replace("","'")
    return data


def __str2db_format(data):
    '''Convert string data to database format.
    If data is None it returns the 'Null' text,
    otherwise it returns the text surrounded by quotes ensuring internal quotes are escaped.
    '''
    if data==None:
        return 'Null'
    out=str(data)
    if "'" not in out:
        return "'" + out + "'"
    elif '"' not in out:
        return '"' + out + '"'
    else:
        return json.dumps(out)

def convert_string_2_dict(input):
    return 0


def __replace_single_quotes(self, data):
    '''replace single quotes ' of any string content of data dictionary'''
    for k,v in data.items():
        if type(v) == str:
            if "'" in v:
                data[k] = data[k].replace("'",'"')


# --
# some helper functions
#
def load_creds_env():
    global os_username, os_password, os_auth_url
    os_username = os.environ['OS_USERNAME']
    os_password = os.environ['OS_PASSWORD']
    os_auth_url = os.environ['OS_AUTH_URL']


def get_keystone_creds():
    global os_username, os_password, os_auth_url
    if os_username == None or os_password == None or os_auth_url == None:
        load_creds_env()

    d = {}
    d['username'] = os_username
    d['password'] = os_password
    d['auth_url'] = os_auth_url
 #   d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


def get_nova_creds():
    d = {}
    d['username']   = os.environ['OS_USERNAME']
    d['api_key']    = os.environ['OS_PASSWORD']
    d['auth_url']   = os.environ['OS_AUTH_URL']
    pass

# def get_neutron_creds():
#     d = {}
#     d['username']   = os.environ['OS_USERNAME']
#     d['api_key']    = os.environ['OS_PASSWORD']
#     d['auth_url']   = os.environ['OS_AUTH_URL']
#     pass

def get_nova_client(p_tenant_name):
    return novaclient.Client("2", os_username, os_password, p_tenant_name, os_auth_url, service_type='compute')

def get_neutron_client(p_tenant_name):
    # vimco = vimconn_openstack.vimconnector(uuid="", name="", tenant=p_tenant_name, url="http://223.194.33.59:5000/v2.0",
    #                                               url_admin="", user="admin", passwd="stack")
    # neutron = vimco._reload_connection_tenant(project_iid=p_tenant_name)

    return neutronclient.Client('2.0', auth_url=os_auth_url, token=get_keystone_client().auth_token, username=os_username, tenant_name=p_tenant_name, password=os_password, public_network='public')

def get_cinder_client(p_tenant_name):
    return cinderclient.Client(os_username, os_password, p_tenant_name, os_auth_url)

def get_keystone_client():
    creds = get_keystone_creds()
    return keystoneclient.Client(**creds)

#
# get keystone function which is used in get_users_per_tenant_details() function to call
# "tenants.list_users(tenant.id)"
#
def get_keystone(p_tenant_name):
    """Returns a Keystone.Client instance."""
    auth = v2.Password(username=os_username, password=os_password,
                  tenant_name=p_tenant_name, auth_url=os_auth_url)
    sess = session.Session(auth=auth)
    keystone = keystoneclient.Client(session=sess)
    # print keystone.tenants.list_users('a2f35a11a77e4286af46c8c0b3fcd2d3')
    return keystone

# --
# def get_token():
#     auth = v2.Password(auth_url=os_auth_url, username=os_username, password=os_password, tenant_name='admin')
#     sess = session.Session(auth=auth, verify=False)
#     token = auth.get_token(sess)
#     print token
#     return token
#
# --
# def new_get_token_keystone():
#     token_admin = get_token()
#     auth = v2.Token(auth_url=os_url, token=token_admin)
#     sess = session.Session(auth=auth)
#     keystone= keystoneclient.Client(session=sess)
#     print keystone
#     print keystone.tenants.list()
#     return keystone


def get_swift_client(p_tenant_name):
    return swiftclient.Connection(authurl=os_auth_url, user=os_username, key=os_password, tenant_name=p_tenant_name, auth_version='2')


# --
# get_flavor_count()
# Returns a flavor:count for a given tenant
#
def get_flavor_count(p_nova_client):
    instanceList = p_nova_client.servers.list()

    cnt_inst_flavor_distribution = {}
    cnt_inst_flavor_distribution['custom'] = 0

    global flavorListDefault
    for fname in flavorListDefault:
        cnt_inst_flavor_distribution[fname] = 0

    for inst in instanceList:
        t_inst_flav = inst.flavor['id']
        flavor = p_nova_client.flavors.get(t_inst_flav)

        if cnt_inst_flavor_distribution.has_key(flavor.name):
            cnt_inst_flavor_distribution[flavor.name] = cnt_inst_flavor_distribution[flavor.name] + 1
        else:
            cnt_inst_flavor_distribution['custom'] = cnt_inst_flavor_distribution['custom'] + 1

    return cnt_inst_flavor_distribution

# --
# get_users_per_tenant_details()
# Returns number of users and list users for a given tenant, to get correctly keystone client for counting list users
# need to call get_keystone(p_tenant_name) instead of get_keystone_client() as usual
#
def _get_users_per_tenant_details():
    """Retrieves stats from keystone"""
    # get keystone client from get_keystone(p_tenant_name) function which have 'power'
    # to fully access keystone functions in lib
    # Count number of users in a tenant

    # get_keystone_client() is called
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    # initiate users_dict
    users_data = {}
    for tenant in tenantlist:

        # invoke another function to get new keystone client for getting users list per tenant
        t_keystone = get_keystone(tenant.name)

        # t_users_cnt = len(t_keystone.tenants.list_users(tenant.id))
        t_users_list = t_keystone.tenants.list_users(tenant.id)
        users_data[tenant.name] = t_users_list

    return users_data, keystone

def convert_user_str_2_dict(data):
    '''
    this function is to convert data format from _get_users_per_tenant_details function : string format to dictionary format for each of user in a given tenant

    :param data: is string format including user info in a  given tenant
    :return: dict format of a user in a given tenant
    '''
    # notice keep a space behind "<User " in below code line to avoid the issue when using literal_eval() function
    data = str(data).lstrip('<User ')
    t_user_str = (data.rstrip('>'))
    t_user_dict= ast.literal_eval(t_user_str)
    # print t_user_dict

    return t_user_dict

def get_users_per_tenant():
    users_data, keystone = _get_users_per_tenant_details()
    tenantlist = keystone.tenants.list()
    t_users_list = []
    for tenant in tenantlist:
        t_users_data= users_data[tenant.name]

        for t_user in t_users_data:
            t_user_dict = convert_user_str_2_dict(t_user)
            #insert tenant name and tenant id into t_user_dict to identify exactly which tenant user is being located - easy to keep track when storing in DB
            t_user_dict['tenant_name'] = tenant.name
            t_user_dict['tenant_id'] = tenant.id
            t_users_list.append(t_user_dict)

    return t_users_list


def get_user_quota(p_nova_client, p_keystone_client):
    tenantlist = p_keystone_client.tenants.list()
    novaclient
    for tenant in tenantlist:
        t_users_cnt = len(p_keystone_client.tenants.list_users(tenant.id))
        t_users_list = p_keystone_client.tenants.list_users(tenant.id)
        limits = nova.limits.get(tenant_id=tenant.id).absolute

        user_quota = nova.quotas.get(tenant_id=tenant.id, user_id='ffbc3c72aa9f44769f3430093c59c457')
        print "print  user_quota for demo user"
        print user_quota








# --
# get_instance_details()
# Returns vpcu, vmem, disk, floatingIP for a given tenant
#
def get_instance_details(p_nova_client):
    instanceList    = p_nova_client.servers.list()
    floatIpList     = p_nova_client.floating_ips.list()

    cnt_instances               = len(instanceList)
    cnt_instances_active        = 0
    cnt_vcpu                    = 0
    cnt_vcpu_active             = 0
    cnt_ram                     = 0
    cnt_ram_active              = 0
    cnt_disk                    = 0
    cnt_ephemeral               = 0
    cnt_floatip                 = len(floatIpList)
    cnt_floatip_disassociated   = 0


    for inst in instanceList:
        t_inst_flav = inst.flavor['id']

        flavor = p_nova_client.flavors.get(t_inst_flav)
        t_inst_vcpu = flavor.vcpus
        t_inst_ram  = flavor.ram
        # print "ram for created instance"
        # print t_inst_ram
        t_inst_disk = flavor.disk
        t_inst_ephemeral = flavor.ephemeral

        cnt_vcpu = cnt_vcpu + t_inst_vcpu
        cnt_ram  = cnt_ram + t_inst_ram
        cnt_disk = cnt_disk + t_inst_disk
        cnt_ephemeral = cnt_ephemeral + t_inst_ephemeral

        if inst.status == "ACTIVE":
            cnt_instances_active = cnt_instances_active + 1
            cnt_vcpu_active = cnt_vcpu_active + t_inst_vcpu
            cnt_ram_active = cnt_ram_active + t_inst_ram

    for floatip in floatIpList:
        if floatip.instance_id == None:
            cnt_floatip_disassociated = cnt_floatip_disassociated + 1

    summary = {}
    summary['total_instances'] = cnt_instances
    summary['total_instances_active'] = cnt_instances_active
    summary['total_vcpu']   = cnt_vcpu
    summary['total_vcpu_active'] = cnt_vcpu_active

    summary['total_ram']    = cnt_ram
    summary['total_ram_active'] = cnt_ram_active

    summary['total_disk']   = cnt_disk
    summary['total_ephemeral'] = cnt_ephemeral
    summary['total_floatingip_allocated'] = cnt_floatip
    summary['total_floatingip_disassocated'] = cnt_floatip_disassociated

    return summary

# --
# get_networks_details()
# Returns details of networks utilization for a tenant
#
def get_networks_details(p_neutron_client):

    global public_network
    public_network = 'public'
    summary = {}

    # filter to get any id in a dict
    kwargs = {'retrieve_all': True, 'fields': 'id'}
    # kwargs = {'retrieve_all': True, 'fields': 'id', 'fields': 'status'}

    #================================
    # list of networks info in a tenant
    #================================

    # get number of networks,networks id, networks status in a tenant
    t_networks_total = len(p_neutron_client.list_networks(**kwargs)['networks'])
    t_networks_active = 0
    t_networks_inactive = 0
    t_networks_id = p_neutron_client.list_networks(**kwargs)['networks']

    # Filter to get all needed attributes of a router in a tenant
    kwargs_networks = {'retrieve_all': True, 'fields': ['name', 'id' ,'status', 'tenant_id', 'updated_at', 'created_at', 'admin_state_up',
                                               'mtu','subnets' ,'security_groups', 'port_security_enabled', 'provider:segmentation_id',
                                               'provider:network_type']}
    t_networks_attributes = p_neutron_client.list_networks(**kwargs_networks)['networks']


    # get a dictionary of list networks in a tenant with all attributes
    #t_networks_dict = p_neutron_client.list_networks()['networks']
    for t_network in t_networks_attributes:
        if t_network['status'] =='ACTIVE':
            t_networks_active = t_networks_active + 1

        else:
            t_networks_inactive = t_networks_inactive + 1

    #================================
    # list of ports info in a tenant
    #================================
    # get number of ports,ports id, ports status in a tenant
    t_ports_total = len(p_neutron_client.list_ports(**kwargs)["ports"])
    t_ports_active = 0
    t_ports_inactive = 0  #any other states should be go here

    # Filter to get all needed attributes of a router in a tenant
    kwargs_port = {'retrieve_all': True, 'fields': ['name', 'id', 'mac_address' ,'status', 'tenant_id', 'updated_at', 'created_at', 'admin_state_up',
                                               'fixed_ips','network_id' ,'security_groups', 'port_security_enabled', 'binding:vif_details',
                                               'binding:vif_type', 'binding:host_id', 'device_id']}
    t_ports_attributes = p_neutron_client.list_ports(**kwargs_port)['ports']

    # get list of all ports in a tenant (dict format each element)
    #t_ports_dict = p_neutron_client.list_ports()['ports']
    for t_port in t_ports_attributes:
        if t_port['status'] == 'ACTIVE':
            t_ports_active = t_ports_active + 1

        else:
            t_ports_inactive = t_ports_inactive + 1

    #================================
    # list of routers info in a tenant
    #================================
    # get number of routers,routers id, routers status in a tenant
    t_routers_total = len(p_neutron_client.list_routers(**kwargs)["routers"])
    t_routers_active = 0
    t_routers_inactive = 0  #any other states should be go here

    # Filter to get all needed attributes of a router in a tenant
    kwargs_routers = {'retrieve_all': True, 'fields': ['name', 'id', 'status', 'tenant_id', 'admin_state_up', 'external_gateway_info']}

    t_routers_attributes = p_neutron_client.list_routers(**kwargs_routers)['routers']
    # Result from t_routers_attributes:  [{u'external_gateway_info': {u'network_id': u'6b971d7b-f1ad-4b78-977b-44ac5c871c04',
    #  u'enable_snat': True, u'external_fixed_ips': [{u'subnet_id': u'9f048ae2-182d-4230-a20d-4367e563ace9',
    # u'ip_address': u'172.24.4.2'}, {u'subnet_id': u'a2118904-eaaa-4d2a-b0e7-2e6e61191f3c', u'ip_address': u'2001:db8::1'}]},
    #  u'tenant_id': u'a2f35a11a77e4286af46c8c0b3fcd2d3', u'id': u'c63549ba-548c-47f4-89ec-810549f0a68f', u'name': u'router1'},
    # {u'external_gateway_info': {u'network_id': u'6b971d7b-f1ad-4b78-977b-44ac5c871c04', u'enable_snat': True, u'external_fixed_ips': [{u'subnet_id': u'9f048ae2-182d-4230-a20d-4367e563ace9', u'ip_address': u'172.24.4.3'}, {u'subnet_id': u'a2118904-eaaa-4d2a-b0e7-2e6e61191f3c', u'ip_address': u'2001:db8::3'}]}, u'tenant_id': u'c1bb85f009f647139c767eeaaba3d258', u'id': u'e233f701-2969-4644-bc27-84ad979a5880', u'name': u'test1'}]

    # get list of all routers in a tenant (dict format each element)
    # t_routers_dict = p_neutron_client.list_routers()['routers']
    for t_router in t_routers_attributes:
        if t_router['status'] == 'ACTIVE':
            t_routers_active = t_routers_active + 1

        else:
            t_routers_inactive = t_routers_inactive + 1

    #================================
    # list of Floating IP info in a tenant
    #================================
    # get number of Floating IP : used, total and available in a tenant
    t_floatingips_total = _estimate_total_ip(p_neutron_client)
    # t_floatingips_total = int(t_floatingips_data)
    t_floatingips_usage = len(p_neutron_client.list_floatingips(**kwargs)['floatingips'])
    t_floatingips_available = t_floatingips_total - t_floatingips_usage

    # filter to get floating id and status of coresponding floating id in a dict format
    kwargs_floatings = {'retrieve_all': True, 'fields': ['id', 'tenant_id', 'floating_ip_address', 'floating_network_id', 'status', 'router_id', 'port_id', 'fixed_ip_address']}

    # obtain list of floatingip id and corresponding status of floatingip
    t_floatingips_attributes = p_neutron_client.list_floatingips(**kwargs_floatings)['floatingips']  # obtain the list of dict that based on defined filter like [{u'status': u'DOWN', u'id': u'81cc8457-b702-4f17-b6a9-c4f421f35b57'}, {u'status': u'DOWN', u'id': u'98ee9a6c-221f-46cf-b965-08a8a342831f'}] or [{u'id': u'98ee9a6c-221f-46cf-b965-08a8a342831f'}]

    if public_network:
        total_ip = _estimate_total_ip(p_neutron_client)
        #stats['floatingips_usage'].append(total_ip)
    if any(e['alias'] == 'lbaas' for e in p_neutron_client.list_extensions()['extensions']):
        t_lbaas_vips_total = len(p_neutron_client.list_vips(**kwargs)["vips"])
        t_lbaas_pools_total= len(p_neutron_client.list_pools(**kwargs)["pools"])
    snat = 0
    for router in p_neutron_client.list_routers()['routers']:
        if router['external_gateway_info'] and router['external_gateway_info']['enable_snat']:
            snat += 1
    t_snat_external_gateway = snat

    # get list of all routers in a tenant (dict format each element)
    t_floatingips_active = 0
    t_floatingips_inactive = 0
    # t_floatingips_dict = p_neutron_client.list_floatingips()['floatingips']
    for t_floatingip in t_floatingips_attributes:
        if t_floatingip['status'] == 'ACTIVE':
            t_floatingips_active = t_floatingips_active + 1

        else:
            t_floatingips_inactive = t_floatingips_inactive + 1

    #================================
    # list of Subnets info in a tenant
    #================================
    # get number of subnets : used, total and available in a tenant
    t_subnets_total = len(p_neutron_client.list_subnets(**kwargs)["subnets"])

    # Filter to get all needed attributes of a subnet in a tenant
    kwargs_subnets = {'retrieve_all': True, 'fields': ['name', 'id', 'tenant_id', 'updated_at', 'created_at',
                                               'network_id' ,'allocation_pools', 'gateway_ip', 'ipv6_address_mode',
                                               'ip_version', 'cidr', 'dns_nameservers']}
    t_subnets_attributes = p_neutron_client.list_subnets(**kwargs_subnets)['subnets']

    summary['total_networks']                = t_networks_total
    summary['total_networks_active']         = t_networks_active
    summary['total_networks_inactive']       = t_networks_inactive
    summary['total_networks_attributes']     = t_networks_attributes

    summary['total_ports']                   = t_ports_total
    summary['total_ports_active']            = t_ports_active
    summary['total_ports_inactive']          = t_ports_inactive
    summary['total_ports_attributes']        = t_ports_attributes

    summary['total_floatingips']             = t_floatingips_total
    summary['total_floatingips_usage']       = t_floatingips_usage
    summary['total_floatingips_available']   = t_floatingips_available
    summary['total_floatingip_active']       = t_floatingips_active
    summary['total_floatingip_inactive']     = t_floatingips_inactive
    summary['total_floatingip_attributes']   = t_floatingips_attributes

    summary['total_routers']                 = t_routers_total
    summary['total_routers_active']          = t_routers_active
    summary['total_routers_inactive']        = t_routers_inactive
    summary['total_routers_attributes']      = t_routers_attributes

    summary['total_subnets']                 = t_subnets_total
    # summary['total_subnets_active']          = t_subnets_active
    # summary['total_subnets_inactive']        = t_subnets_inactive
    summary['total_subnets_attributes']      = t_subnets_attributes

    summary['total_snat_external_gateway']   = t_snat_external_gateway
    summary['total_lbaas_vips']                   = t_lbaas_vips_total
    summary['total_lbaas_pools']                   = t_lbaas_pools_total

    return summary

def _estimate_total_ip(p_neutron_client):
    # global public_network

    total_ip = 0
    subnet_mask = re.compile('[^/]+/(\d{1,2})')
    subnets_from_public_network = []
    try:
        subnets_from_public_network = p_neutron_client.list_networks(
            name=public_network)['networks'][0]['subnets'] # obtain subnets ID [u'771e1289-7b9c-4d38-8150-5a1170034fe5', u'b7ad90cf-d459-43bb-9f49-359dcaf347f0']
    except Exception as e:
        print "Cannot get subnets associated with %s network: %s" % \
                    (public_network, e)
        return None

    for public_subnet_id in subnets_from_public_network:
        net_info = p_neutron_client.list_subnets(
            id=public_subnet_id,
            fields=['cidr', 'gateway_ip'])['subnets'][0]  # net info {u'cidr': u'172.24.4.0/24', u'gateway_ip': u'172.24.4.1'} {u'cidr': u'2001:db8::/64',u'gateway_ip': u'2001:db8::2'}
        subnet_match = subnet_mask.match(net_info['cidr'])
        if not subnet_match:
            print"Cannot retrieve the subnet mask of subnet_id %s" % \
                        public_subnet_id
            next
        subnet = int(subnet_match.group(1))
        ips_number = 2**(32 - subnet)
        if 'gateway_ip' in net_info and net_info['gateway_ip']:
            ips_number -= 1
        ips_number -= 2
        total_ip += ips_number
    #print "total number of floating IP: %d " % total_ip
    # print total_ip
    return total_ip


# --
# get_volume_details()
# Returns details of volume utilization for a tenant
#
def get_volume_details(p_cinder_client):
    volumelist = p_cinder_client.volumes.list()
    snapshotlist = p_cinder_client.volume_snapshots.list()
    total_provisioned = 0
    total_volume_snapshots_cnt = 0
    total_volume_snapshots_provisioned = 0
    for volumes in volumelist:
        total_provisioned = total_provisioned + volumes.size  # (volumes.size * 1024 * 1024 * 1024)

    for snapshot in snapshotlist:
        total_volume_snapshots_provisioned = total_volume_snapshots_cnt + snapshot.size # (snapshot.size * 1024 * 1024 * 1024)


    summary = {}
    summary['total_vols_count'] = len(volumelist)
    summary['total_vols_provisioned_capacity'] = total_provisioned
    summary['total_snapshots_count'] = len(snapshotlist)
    summary['total_snapshots_provisioned_capacity'] = total_volume_snapshots_provisioned
    return summary


# --
# get_object_details()
# Returns details of object utilization for a tenant
#
def get_object_details(p_swift_client):
    summary = {}
    t_object_store = p_swift_client.get_account()

    summary['total_container_count']     = int(t_object_store[0]['x-account-container-count'])
    summary['total_object_count']        = int(t_object_store[0]['x-account-object-count'])
    summary['total_object_storage_used'] = float("{0:.2f}".format(int(t_object_store[0]['x-account-bytes-used']) / (1024*1024*1024)))
    return summary


# --
# get_all_tenant_flavorcount()
# Returns dict of dict for all tenants
# This is of the form
#    d['Tenant_Name'] = {
#        "m1.tiny"       : int,
#        "m1.small"      : int,
#        "m1.medium"     : int,
#        "m1.large"      : int,
#        "m1.xlarge"     : int,
#        "m1.2xlarge"    : int,
#        "m1.4xlarge"    : int,
#        "m1.8xlarge"    : int,
#        "custom"        : int
#    }
#
def get_all_tenant_flavorcount():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    global _debug
    if _debug:
        print '[+] Crunching flavor stats for all tenants ...'

    d = {}

    for tenant in tenantlist:

        if tenant.enabled == False:
            t_tenant_name = tenant.name

            d[t_tenant_name] = {
                'm1.tiny'   : 'disabled',
                'm1.small'  : 'disabled',
                'm1.medium' : 'disabled',
                'm1.large'  : 'disabled',
                'm1.xlarge' : 'disabled',
                'm1.2xlarge': 'disabled',
                'm1.4xlarge': 'disabled',
                'm1.8xlarge': 'disabled',
                'custom'    : 'disabled',
            }

        else:
            nova = get_nova_client(tenant.name)
            t_tenant_name = tenant.name
            t_flavor_details = get_flavor_count(nova)

            d[t_tenant_name] = {
                'm1.tiny'   : t_flavor_details['m1.tiny'],
                'm1.small'  : t_flavor_details['m1.small'],
                'm1.medium' : t_flavor_details['m1.medium'],
                'm1.large'  : t_flavor_details['m1.large'],
                'm1.xlarge' : t_flavor_details['m1.xlarge'],
                'm1.2xlarge': t_flavor_details['m1.2xlarge'],
                'm1.4xlarge': t_flavor_details['m1.4xlarge'],
                'm1.8xlarge': t_flavor_details['m1.8xlarge'],
                'custom'    : t_flavor_details['custom']
            }

        if _debug == True:
            print "    [-] %s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (t_tenant_name,
                    t_flavor_details['m1.tiny'],
                    t_flavor_details['m1.small'],
                    t_flavor_details['m1.medium'],
                    t_flavor_details['m1.large'],
                    t_flavor_details['m1.xlarge'],
                    t_flavor_details['m1.2xlarge'],
                    t_flavor_details['m1.4xlarge'],
                    t_flavor_details['m1.8xlarge'],
                    t_flavor_details['custom'] )

    return d


# --
# get_all_tenant_utilization()
# Returns a (k,v) dict where k = tenantname and v is dict of pulled values
#
def get_all_tenant_utilization():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    global _debug
    if _debug == True:
        print '[+] Crunching utilization stats for all tenants ...'

    aggr_users_cnt = 0
    aggr_inst_prov = 0
    aggr_inst_active = 0
    aggr_vcpu_prov = 0
    aggr_vcpu_active = 0
    aggr_ram_prov = 0
    aggr_ram_active = 0
    aggr_disk_prov = 0
    aggr_floatip_alloc = 0
    aggr_floatip_disassoc = 0
    aggr_persist_vol_count       = 0
    aggr_persist_provisioned_vol_value  = 0
    aggr_persist_snapshot_count  = 0
    aggr_persist_provisoned_snapshots_value  = 0
    aggr_container_count    = 0
    aggr_object_count = 0
    aggr_object_storage_used = 0

    aggr_networks_prov = 0
    aggr_networks_active = 0
    aggr_networks_inactive = 0

    aggr_ports_prov = 0
    aggr_ports_active = 0
    aggr_ports_inactive = 0

    aggr_floatingips_prov = 0
    aggr_floatingips_allocated = 0
    aggr_floatingips_available = 0
    aggr_floatingips_active = 0
    aggr_floatingips_inactive = 0

    aggr_routers_prov = 0
    aggr_routers_active = 0
    aggr_routers_inactive = 0

    aggr_subnets_prov = 0

    aggr_snat_external_gateway_prov = 0
    aggr_lbaas_vips_prov = 0
    aggr_lbaas_pools_prov = 0


    # Will be returning an aggregate at the end .. so lets use OrderedDict()
    d = collections.OrderedDict()

    for tenant in tenantlist:

        # Skip disabled tenants
        if tenant.enabled == False:
            t_tenant_name           = tenant.name
            t_users_cnt             = 'disabled'
            t_users_list            = 'disabled'
            t_instances             = 'disabled'
            t_instances_active      = 'disabled'
            t_vcpu                  = 'disabled'
            t_vcpu_active           = 'disabled'
            t_ram                   = 'disabled'
            t_ram_active            = 'disabled'
            t_disk_ephemeral        = 'disabled'
            t_float_allocated       = 'disabled'
            t_float_disassociated   = 'disabled'
            t_persist_volcount      = 'disabled'
            t_persist_provisioned_vol_value         = 'disabled'
            t_persist_snapshot_count                = 'disabled'
            t_persist_provisioned_snapshot_value   = 'disabled'
            t_container_count       = 'disabled'
            t_object_count          = 'disabled'
            t_object_storage_used   = 'disabled'
            t_networks_total        = 'disabled'
            t_networks_active       = 'disabled'
            t_networks_inactive     = 'disabled'
            t_networks_attributes   = 'disabled'
            t_ports_total           = 'disabled'
            t_ports_active          = 'disabled'
            t_ports_inactive        = 'disabled'
            t_ports_attributes      = 'disabled'
            t_floatingips_total     = 'disabled'
            t_floatingips_usage     = 'disabled'
            t_floatingips_available = 'disabled'
            t_floatingips_active    = 'disabled'
            t_floatingips_inactive  = 'disabled'
            t_floatingips_attributes= 'disabled'
            t_routers_total         = 'disabled'
            t_routers_active        = 'disabled'
            t_routers_inactive      = 'disabled'
            t_routers_attributes    = 'disabled'
            t_subnets_total         = 'disabled'
            t_subnets_attributes    = 'disabled'
            t_snat_external_gateway = 'disabled'
            t_lbaas_vips_total      = 'disabled'
            t_lbaas_pools_total     = 'disabled'


        else :
            # Un_used code---this part of code has been move to get_users_per_tenant_details()

            # get keystone client from get_keystone(p_tenant_name) function which have 'power'
            # to fully access keystone functions in lib
            t_keystone = get_keystone(tenant.name)
            t_users_cnt = len(t_keystone.tenants.list_users(tenant.id))
            t_users_list = t_keystone.tenants.list_users(tenant.id)
            # print " user list"
            # print t_users_list

            nova = get_nova_client(tenant.name)
            cinder = get_cinder_client(tenant.name)
            swift = get_swift_client(tenant.name)
            neutron = get_neutron_client(tenant.name)

            compute_summary = get_instance_details(nova)
            storage_summary = get_volume_details(cinder)
            object_summary  = get_object_details(swift)
            neutron_summary = get_networks_details(neutron)
            # print neutron_summary

            t_tenant_name               = tenant.name
            t_users_cnt                 = t_users_cnt
            t_users_list                = t_users_list
            t_instances                 = compute_summary['total_instances']
            t_instances_active          = compute_summary['total_instances_active']
            t_vcpu                      = compute_summary['total_vcpu']
            t_vcpu_active               = compute_summary['total_vcpu_active']
            t_ram                       = compute_summary['total_ram'] #/ 1024
            t_ram_active                = compute_summary['total_ram_active'] #/ 1024
            t_disk_ephemeral            = compute_summary['total_disk'] + compute_summary['total_ephemeral']
            t_float_allocated           = compute_summary['total_floatingip_allocated']
            t_float_disassociated       = compute_summary['total_floatingip_disassocated']
            t_persist_volcount          = storage_summary['total_vols_count']
            t_persist_provisioned_vol_value       = storage_summary['total_vols_provisioned_capacity']
            t_persist_snapshot_count       = storage_summary['total_snapshots_count']
            t_persist_provisioned_snapshot_value       = storage_summary['total_snapshots_provisioned_capacity']
            t_container_count           = object_summary['total_container_count']
            t_object_count              = object_summary['total_object_count']
            t_object_storage_used       = object_summary['total_object_storage_used']
            t_networks_total            = neutron_summary['total_networks']
            t_networks_active           = neutron_summary['total_networks_active']
            t_networks_inactive         = neutron_summary['total_networks_inactive']
            t_networks_attributes       = neutron_summary['total_networks_attributes']
            t_ports_total               = neutron_summary['total_ports']
            t_ports_active              = neutron_summary['total_ports_active']
            t_ports_inactive            = neutron_summary['total_ports_inactive']
            t_ports_attributes          = neutron_summary['total_ports_attributes']
            t_floatingips_total         = neutron_summary['total_floatingips']
            t_floatingips_usage         = neutron_summary['total_floatingips_usage']
            t_floatingips_available     = neutron_summary['total_floatingips_available']
            t_floatingips_active        = neutron_summary['total_floatingip_active']
            t_floatingips_inactive      = neutron_summary['total_floatingip_inactive']
            t_floatingips_attributes    = neutron_summary['total_floatingip_attributes']
            t_routers_total             = neutron_summary['total_routers']
            t_routers_active            = neutron_summary['total_routers_active']
            t_routers_inactive          = neutron_summary['total_routers_inactive']
            t_routers_attributes        = neutron_summary['total_routers_attributes']
            t_subnets_total             = neutron_summary['total_subnets']
            t_subnets_attributes        = neutron_summary['total_subnets_attributes']
            t_snat_external_gateway     = neutron_summary['total_snat_external_gateway']
            t_lbaas_vips_total          = neutron_summary['total_lbaas_vips']
            t_lbaas_pools_total         = neutron_summary['total_lbaas_pools']


            # For calculate total resources in whole tenants
            aggr_users_cnt              = aggr_users_cnt + t_users_cnt
            aggr_inst_prov              = aggr_inst_prov + t_instances
            aggr_inst_active            = aggr_inst_active + t_instances_active
            aggr_vcpu_prov              = aggr_vcpu_prov + t_vcpu
            aggr_vcpu_active            = aggr_vcpu_active + t_vcpu_active
            aggr_ram_prov               = aggr_ram_prov + t_ram
            aggr_ram_active             = aggr_ram_active + t_ram_active
            aggr_disk_prov              = aggr_disk_prov + t_disk_ephemeral
            aggr_floatip_alloc          = aggr_floatip_alloc + t_float_allocated
            aggr_floatip_disassoc       = aggr_floatip_disassoc + t_float_disassociated
            aggr_persist_vol_count       = aggr_persist_vol_count + t_persist_volcount
            aggr_persist_provisioned_vol_value    = aggr_persist_provisioned_vol_value + t_persist_provisioned_vol_value
            aggr_persist_snapshot_count    = aggr_persist_snapshot_count + t_persist_snapshot_count
            aggr_persist_provisoned_snapshots_value    = aggr_persist_provisoned_snapshots_value + t_persist_provisioned_snapshot_value
            aggr_object_count           = aggr_object_count + t_object_count
            aggr_object_storage_used    = aggr_object_storage_used + t_object_storage_used

            aggr_networks_prov          = aggr_networks_prov + t_networks_total
            aggr_networks_active        = aggr_networks_active + t_networks_active
            aggr_networks_inactive      = aggr_networks_inactive + t_networks_inactive

            aggr_ports_prov             = aggr_ports_prov + t_ports_total
            aggr_ports_active           = aggr_ports_active + t_ports_active
            aggr_ports_inactive         = aggr_ports_inactive + t_ports_inactive

            aggr_floatingips_prov       = aggr_floatingips_prov + t_floatingips_total
            aggr_floatingips_allocated  = aggr_floatingips_allocated + t_floatingips_usage
            aggr_floatingips_available  = aggr_floatingips_available + t_floatingips_available
            aggr_floatingips_active     = aggr_floatingips_active + t_floatingips_active
            aggr_floatingips_inactive   = aggr_floatingips_inactive + t_floatingips_inactive

            aggr_routers_prov           = aggr_routers_prov + t_routers_total
            aggr_routers_active         = aggr_routers_active + t_routers_active
            aggr_routers_inactive       = aggr_routers_inactive + t_routers_inactive

            aggr_subnets_prov           = aggr_subnets_prov + t_subnets_total

            aggr_snat_external_gateway_prov = aggr_snat_external_gateway_prov + t_snat_external_gateway
            aggr_lbaas_vips_prov            = aggr_lbaas_vips_prov + t_lbaas_vips_total
            aggr_lbaas_pools_prov           = aggr_lbaas_pools_prov + t_lbaas_pools_total




        # Inst_Prov,Inst_Active,VCPU_Prov,VCPU_Active,RAM_Prov,RAM_Active,Disk_Prov_GB,FloatIP_Alloc,FloatIP_Disassoc,Vols_Prov,Vols_Prov_GB,Object_Containers,Object_Count,Object_Storage_Used_GB"
        # k,v where k becomes header
        d[t_tenant_name] = {
            'Users_count'           : t_users_cnt,
            'Users_list'            : t_users_list,
            'Inst_Prov'             : t_instances,
            'Inst_Active'           : t_instances_active,
            'VCPU_Prov'             : t_vcpu,
            'VCPU_Active'           : t_vcpu_active,
            'RAM_Prov'              : t_ram,
            'RAM_Active'            : t_ram_active,
            'Disk_Prov_GB'          : t_disk_ephemeral,
            'FloatIP_Alloc'         : t_float_allocated,
            'FloatIP_Disassoc'      : t_float_disassociated,
            'Vols_Prov'             : t_persist_volcount,
            'Vols_Prov_GB'          : t_persist_provisioned_vol_value,
            'Snapshot_Prov'         : t_persist_snapshot_count,
            'Snapshot_Prov_GB'      : t_persist_provisioned_snapshot_value,
            'Object_Containers'     : t_container_count,
            'Object_Count'          : t_object_count,
            'Object_Storage_Used_GB': t_object_storage_used,
            'Networks_Prov'         : t_networks_total,
            'Networks_Active'       : t_networks_active,
            'Networks_Inactive'     : t_networks_inactive,
            'Networks_Attributes'   : t_networks_attributes,
            'Ports_Prov'            : t_ports_total,
            'Ports_Active'          : t_ports_active,
            'Ports_Inactive'        : t_ports_inactive,
            'Ports_Attributes'      : t_ports_attributes,
            'Floating_IPs_Prov'     : t_floatingips_total,
            'Floating_IPs_Usage'    : t_floatingips_usage,
            'Floating_IPs_Available': t_floatingips_available,
            'Floating_IPs_Active'   : t_floatingips_active,
            'Floating_IPs_Inactive' : t_floatingips_inactive,
            'Floating_IPs_Attributes': t_floatingips_attributes,
            'Routers_Prov'          : t_routers_total,
            'Routers_Active'        : t_routers_active,
            'Routers_Inactive'      : t_routers_inactive,
            'Routers_Attributes'    : t_routers_attributes,
            'Subnets_Prov'          : t_subnets_total,
            'Subnets_Attributes'    : t_subnets_attributes,
            'Snat_external_gateway_Prov': t_snat_external_gateway,
            'Lbaas_Vips_Prov'       : t_lbaas_vips_total,
            'Lbaas_Pools_Prov'      : t_lbaas_pools_total

        }

        if _debug == True:
            print " [-] %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, \
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
                    t_users_cnt,
                    t_users_list,
                    t_tenant_name,
                    t_instances,
                    t_instances_active,
                    t_vcpu,
                    t_vcpu_active,
                    t_ram,
                    t_ram_active,
                    t_disk_ephemeral,
                    t_float_allocated,
                    t_float_disassociated,
                    t_persist_volcount,
                    t_persist_provisioned_vol_value,
                    t_persist_snapshot_count,
                    t_persist_provisioned_snapshot_value,
                    t_container_count,
                    t_object_count,
                    t_object_storage_used,
                    t_networks_total,
                    t_networks_active,
                    t_networks_inactive,
                    t_networks_attributes,
                    t_ports_total,
                    t_ports_active,
                    t_ports_inactive,
                    t_ports_attributes,
                    t_floatingips_total,
                    t_floatingips_usage,
                    t_floatingips_available,
                    t_floatingips_active,
                    t_floatingips_inactive,
                    t_floatingips_attributes,
                    t_routers_total,
                    t_routers_active,
                    t_routers_inactive,
                    t_routers_attributes,
                    t_subnets_total,
                    t_subnets_attributes,
                    t_snat_external_gateway,
                    t_lbaas_vips_total,
                    t_lbaas_pools_total
            )

    # Print Aggregates
    if _debug == True:
        print " [-] Total,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s" % (
                aggr_users_cnt,
                aggr_inst_prov,
                aggr_inst_active,
                aggr_vcpu_prov,
                aggr_vcpu_active,
                aggr_ram_prov,
                aggr_ram_active,
                aggr_disk_prov,
                aggr_floatip_alloc,
                aggr_floatip_disassoc,
                aggr_persist_vol_count,
                aggr_persist_provisioned_vol_value,
                aggr_persist_snapshot_count,
                aggr_persist_provisoned_snapshots_value,
                aggr_container_count,
                aggr_object_count,
                aggr_object_storage_used,
                aggr_networks_prov,
                aggr_networks_active,
                aggr_networks_inactive,
                aggr_ports_prov,
                aggr_ports_active,
                aggr_ports_inactive,
                aggr_floatingips_prov,
                aggr_floatingips_allocated,
                aggr_floatingips_available,
                aggr_floatingips_active,
                aggr_floatingips_inactive,
                aggr_floatingips_inactive,
                aggr_routers_prov,
                aggr_routers_active,
                aggr_routers_inactive,
                aggr_subnets_prov,
                aggr_snat_external_gateway_prov,
                aggr_lbaas_vips_prov,
                aggr_lbaas_pools_prov
        )

    # Adding aggregates at the end of ordered dict
    d['_Total'] = {
            'Users_count'       : aggr_users_cnt,
            'Inst_Prov'         : aggr_inst_prov,
            'Inst_Active'       : aggr_inst_active,
            'VCPU_Prov'         : aggr_vcpu_prov,
            'VCPU_Active'       : aggr_vcpu_active,
            'RAM_Prov'          : aggr_ram_prov,
            'RAM_Active'        : aggr_ram_active,
            'Disk_Prov_GB'      : aggr_disk_prov,
            'FloatIP_Alloc'     : aggr_floatip_alloc,
            'FloatIP_Disassoc'  : aggr_floatip_disassoc,
            'Vols_Prov'         : aggr_persist_vol_count,
            'Vols_Prov_GB'      : aggr_persist_provisioned_vol_value,
            'Snapshot_Prov'      : aggr_persist_snapshot_count,
            'Snapshot_Prov_GB'      : aggr_persist_provisoned_snapshots_value,
            'Object_Containers' : aggr_container_count,
            'Object_Count'      : aggr_object_count,
            'Object_Storage_Used_GB': aggr_object_storage_used,
            'Networks_Prov'         : aggr_networks_prov,
            'Networks_Active'       : aggr_networks_active,
            'Networks_Inactive'     : aggr_networks_inactive,
            'Ports_Prov'            : aggr_ports_prov,
            'Ports_Active'          : aggr_ports_active,
            'Ports_Inactive'        : aggr_ports_inactive,
            'Floating_IPs_Prov'     : aggr_floatingips_prov,
            'Floating_IPs_Usage'    : aggr_floatingips_allocated,
            'Floating_IPs_Available': aggr_floatingips_available,
            'Floating_IPs_Active'   : aggr_floatingips_active,
            'Floating_IPs_Inactive' : aggr_floatingips_inactive,
            'Routers_Prov'          : aggr_routers_prov,
            'Routers_Active'        : aggr_routers_active,
            'Routers_Inactive'      : aggr_routers_inactive,
            'Subnets_Prov'          : aggr_subnets_prov,
            'Snat_external_gateway_Prov': aggr_snat_external_gateway_prov,
            'Lbaas_Vips_Prov'       : aggr_lbaas_vips_prov,
            'Lbaas_Pools_Prov'      : aggr_lbaas_pools_prov
    }

    return d

# --
# Get absolute limits details for a tenant
#
def get_quotas_limit_details():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    global _debug
    if _debug:
        print '[+] Crunching flavor stats for all tenants ...'

    q = {}


    for tenant in tenantlist:

        if tenant.enabled == False:
            t_tenant_name = tenant.name

            q[t_tenant_name] = {
                'm1.tiny'   : 'disabled',
                'm1.small'  : 'disabled',
                'm1.medium' : 'disabled',
                'm1.large'  : 'disabled',
                'm1.xlarge' : 'disabled',
                'm1.2xlarge': 'disabled',
                'm1.4xlarge': 'disabled',
                'm1.8xlarge': 'disabled',
                'custom'    : 'disabled',
            }

        else:

            nova = get_nova_client(tenant.name)
            neutron = get_neutron_client(tenant.name)
            cinder = get_cinder_client(tenant.name)
            t_tenant_name = tenant.name

            #=====================================================================================================
            # Quotas and limits Compute resources
            #=====================================================================================================
            """Retrieves quotas and limits for each of tenant from compute API"""
            q[t_tenant_name] = {'limits_compute': {'tenant_id': tenant.id, 'tenant_name': tenant.name},
                                'quotas_compute': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'quotas_networks': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'limits_cinder': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'quotas_cinder': {'tenant_id': tenant.id,'tenant_name': tenant.name}
                                }

            # Get Nova-absolute limits for tenant
            limits = nova.limits.get(tenant_id=tenant.id).absolute
            for limit in limits:
                if 'ram' in limit.name.lower():
                    limit.value = limit.value #* 1024.0 * 1024.0
                q[t_tenant_name]['limits_compute'][limit.name] = limit.value
            print "Limits of compute resources for all tenants are : %s" % (q[t_tenant_name]['limits_compute'])

            # Nova Quotas for tenant

            quotas = nova.quotas.get(tenant_id=tenant.id)
            for item in ('cores', 'fixed_ips', 'floating_ips', 'instances',
                'key_pairs', 'ram', 'security_groups','security_group_rules', 'server_groups', 'server_group_members'):
                if item == 'ram':
                    setattr(quotas, item, getattr(quotas, item)) #* 1024 * 1024

                q[t_tenant_name]['quotas_compute'][item] = getattr(quotas, item)
            print "Quotas of compute resources are: %s" %( q[t_tenant_name]['quotas_compute'])


            #=====================================================================================================
            # Quotas Networks
            #=====================================================================================================
            """Retrieves tenant quotas from Neutron- Networks API"""
            # get Networks-tenant quotas
            # q[t_tenant_name] = {'quotas_networks': {'tenant_id': tenant.id,'tenant_name': tenant.name}}
            quotas_networks = neutron.show_quota(tenant_id=tenant.id)['quota']
            # for quota_network in quotas_networks:
            # for item in ('floatingip', 'health_monitor' ,'subnetpool',
            #       'member', 'network', 'port', 'router',
            #       'security_group', 'security_group_rule', 'subnet', 'rbac_policy','pool'):
            for item in ('subnet', 'network', 'floatingip', 'subnetpool', 'security_group_rule',
                  'security_group', 'router', 'rbac_policy',  'port'):
                q[t_tenant_name]['quotas_networks'][item] = quotas_networks[item]
                # q[t_tenant_name]['quotas_networks'][item]=getattr(quotas_networks, item)
            print "Quotas of networks are: %s" % (q[t_tenant_name]['quotas_networks'])


            #=====================================================================================================
            # Quotas and limits Cinder
            #=====================================================================================================
            """Retrieves tenant quotas from cinder- Cinder API v2"""
            # q[t_tenant_name] = {
            #     'quotas_cinder': {'tenant_id': tenant.id, "tenant_name": tenant.name},
            #     'limits_cinder': {'tenant_id': tenant.id,'tenant_name': tenant.name}
            #     # 'volume': {'count': 0, 'byte': 0},
            #     # 'volume_snapshots': {'count': 0, 'byte': 0}
            # }

            # Get cinder-absolute limits for tenant
            try:
                limits_cinder = cinder.limits.get().absolute
            except Exception:
                continue
            for limit_cinder in limits_cinder:
                # if 'Giga' in limit_cinder.name:
                #     limit_cinder.value = limit_cinder.value * 1024 * 1024 * 1024
                q[t_tenant_name]['limits_cinder'][limit_cinder.name] = limit_cinder.value
            print "Limits of cinder are: %s "% (q[t_tenant_name]['limits_cinder'])

            # get cinder-tenant quotas
            quotas_cinder = cinder.quotas.get(tenant_id=tenant.id, usage=True)
            for item in ('backup_gigabytes', 'backups', 'gigabytes', 'gigabytes_lvmdriver-1',
                'per_volume_gigabytes', 'snapshots', 'snapshots_lvmdriver-1','volumes', 'volumes_lvmdriver-1'):
                # if 'Giga' in item:
                #     setattr(quotas_cinder, item, getattr(quotas_cinder, item)) * 1024 * 1024 * 1024
                q[t_tenant_name]['quotas_cinder'][item] = getattr(quotas_cinder, item)
                # d[t_tenant_name]['quotas_cinder'][item] = quotas_cinder[item]
            print "Storage Quota- Cinder are : %s" % q[t_tenant_name]['quotas_cinder']

    return q

# --
# convert quota compute to DB format for storing (json format)
#

def get_dbformat_compute_quotas_from_op():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    quotas_compute_list = []
    data = get_quotas_limit_details()

    for tenant in tenantlist:
        quotas_compute = data[tenant.name]['quotas_compute']
        quotas_compute['max_vmem']                 =quotas_compute.pop('ram')
        quotas_compute['max_vcpus']                =quotas_compute.pop('cores')
        quotas_compute['max_server_groups']        =quotas_compute.pop('server_groups')
        quotas_compute['max_server_group_members'] =quotas_compute.pop('server_group_members')
        quotas_compute['max_floating_ips']         =quotas_compute.pop('floating_ips')
        quotas_compute['max_fixed_ips']            =quotas_compute.pop('fixed_ips')
        quotas_compute['max_key_pairs']            =quotas_compute.pop('key_pairs')
        quotas_compute['max_instances']            =quotas_compute.pop('instances')
        quotas_compute['max_security_group_rules'] =quotas_compute.pop('security_group_rules')
        quotas_compute['max_security_groups']      =quotas_compute.pop('security_groups')

        # obj_quotas_compute.append(json.dumps(json_quotas_compute, sort_keys=False).encode('utf-8'))
        quotas_compute_list.append(quotas_compute)
    return quotas_compute_list

# --
# convert limits compute to DB format for storing (json format)
#
def get_dbformat_compute_limits_from_op():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    limits_compute_list = []

    data = get_quotas_limit_details()


    for tenant in tenantlist:
        # dict contains upper letters
        limits_compute_orgi = data[tenant.name]['limits_compute']

        # convert all key of dict to lower letters
        limits_compute = dict((k.lower(), v) for k,v in limits_compute_orgi.iteritems())
        # print " lower dict"
        # print limits_compute

        # vcpus meters
        limits_compute['max_total_vcpus']       =limits_compute.pop('maxtotalcores')
        limits_compute['total_vcpus_used']      =limits_compute.pop('totalcoresused')
        # add two new meters for vcpus
        limits_compute['total_vcpus_available'] = 0  #TODO if this is first time that app comes up --> initially,(no reserved resource exists: total_vcpus_available = max_total_vcpus - total_vcpus_used  OR max_total_vcpus)
        limits_compute['total_vcpus_reserved']  = 0

        # add two new meters for vmem
        limits_compute['max_total_vmem_size']   =limits_compute.pop('maxtotalramsize')
        limits_compute['total_vmem_used']       =limits_compute.pop('totalramused')
        limits_compute['total_vmem_available']  = 0
        limits_compute['total_vmem_reserved']   = 0

        # add two new meters for instances (vapps)
        limits_compute['max_total_instances']       =limits_compute.pop('maxtotalinstances')
        limits_compute['total_instances_used']      =limits_compute.pop('totalinstancesused')
        limits_compute['total_instances_available'] = 0
        limits_compute['total_instances_reserved']  = 0

        # add two new meters for instances (vapps)
        limits_compute['max_total_floatingips']       =limits_compute.pop('maxtotalfloatingips')
        limits_compute['total_floatingips_used']      =limits_compute.pop('totalfloatingipsused')
        limits_compute['total_floatingips_available'] = 0
        limits_compute['total_floatingips_reserved']  = 0

        limits_compute_list.append(limits_compute)
        # print limits_compute_list
    return limits_compute_list


# --
# convert quota networks (neutron) to DB format for storing (json format)
#

def get_dbformat_networks_quotas_from_op():
    keystone = get_keystone_client()
    tenantlist = keystone.tenants.list()

    quotas_networks_list = []
    data = get_quotas_limit_details()

    for tenant in tenantlist:
        quotas_network = data[tenant.name]['quotas_networks']
        quotas_network['max_network']             = quotas_network.pop('network')
        quotas_network['max_router']              = quotas_network.pop('router')
        quotas_network['max_port']                = quotas_network.pop('port')
        quotas_network['max_floatingip']          = quotas_network.pop('floatingip')
        quotas_network['max_subnet']              = quotas_network.pop('subnet')
        quotas_network['max_subnetpool']          = quotas_network.pop('subnetpool')
        quotas_network['max_security_group_rule'] = quotas_network.pop('security_group_rule')
        quotas_network['max_security_group']      = quotas_network.pop('security_group')
        quotas_network['max_rbac_policy']         = quotas_network.pop('rbac_policy')

        # obj_quotas_compute.append(json.dumps(json_quotas_compute, sort_keys=False).encode('utf-8'))
        quotas_networks_list.append(quotas_network)
    return quotas_networks_list


def add_quotas_limits_2_db(mydb, table, data):
    result = mydb.add_row_rs(table, data)
    if result > 0:
        print "Added data to %s table successfully"
    return result


#---------------------------------------------------------------------------------------------------------------------------
#  START --- Get total capacity of compute resources from hyper-visor of compute node #TODO need to take into account multi-compute nodes scenario
#---------------------------------------------------------------------------------------------------------------------------

# --
# get_hypervisor_total_compute_utilization()
# Only admnin user who have administrator permission to query total compute capacity from hyper-visor in a compute node
# Returns details of hyper-visor utilization for a compute node (all tenants-value depend on number of deployed compute node)
#
def get_hypervisor_all_compute_utilization(): #TODO need to modify other related codes when completely moving these functions to here from sh_compute_capacity_poll.py file
    nova = get_nova_client('admin') # Statically set "admin"
    total_cap_compute = nova.hypervisor_stats.statistics()._info
    vcpu_allocation_ratio = 16
    memory_allocation_ratio = 1
    return {
                'servers': [total_cap_compute['count'], total_cap_compute['current_workload']],
                'vdisk_capacity': {
                         #'uuid' : 12, # using UUID for keeps track total compute capacity for each type of resource
                         'disk_total': total_cap_compute['local_gb'],
                         'disk_allocated' : total_cap_compute['local_gb_used'],
                         'disk_available' : total_cap_compute['free_disk_gb'],
                         'disk_reserved' : 0},
                'vmem_capacity': {
                           #'uuid' : 13,
                           'mem_total':  total_cap_compute['memory_mb'],
                           'vmem_total': total_cap_compute['memory_mb'] * memory_allocation_ratio,
                           'vmem_allocated': total_cap_compute['memory_mb_used'],
                           'mem_available': total_cap_compute['free_ram_mb'],
                           'vmem_available': (total_cap_compute['memory_mb'] * memory_allocation_ratio -
                                    total_cap_compute['memory_mb_used']),
                           'vmem_reserved': 0},
                'instances': [total_cap_compute['running_vms']],
                'vcpu_capacity': {
                    #'uuid': 14,
                    'cpu_total': total_cap_compute['vcpus'],
                    'vcpu_total': total_cap_compute['vcpus'] * vcpu_allocation_ratio,
                    'vcpu_allocated': total_cap_compute['vcpus_used'],
                    'cpu_available': total_cap_compute['vcpus'],  # curently nova api returns number of physical cores instead of virtual cores as expected
                    'vcpu_available' : (total_cap_compute['vcpus'] * vcpu_allocation_ratio -
                              total_cap_compute['vcpus_used']),
                    'vcpu_reserved': 0
                }}

# --
# get total capacity for compute: vcpu, vmem, vdisk by invoke get_hypervisor_all_compute_utilization
#
def all_vcpu_cap():
    '''
    this function is to grab vcpus resources from hypervisor with output format as below
    {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    :return: {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    '''
    all_compute_cap = get_hypervisor_all_compute_utilization()
    vcpus_capacity = all_compute_cap['vcpu_capacity']
    return vcpus_capacity

def all_vmem_cap():
    all_compute_cap = get_hypervisor_all_compute_utilization()
    vmem_capactity = all_compute_cap['vmem_capacity']
    return vmem_capactity

def all_vdisk_cap():
    all_compute_cap = get_hypervisor_all_compute_utilization()
    vdisk_capactity = all_compute_cap['vdisk_capacity']
    return vdisk_capactity
#---------------------------------------------------------------------------------------------------------------------------
# END --- Get total capacity of compute resources from hyper-visor of compute node
#---------------------------------------------------------------------------------------------------------------------------



# --
# csv_report()
# Write out the csv formated dict values
#     [d_report]  single level ordered dict that is to be rendered as a table
#     [l_header]  table headers that double up as keys to the d_report dict
#     [file_name] the file that the final csv is to be written into
#
# Note : d_report must be ordered dict for aggregates to be printed last
def csv_report(d_report,l_header,file_name):
    global _debug
    if _debug == True:
        print "[+] Formating report as CSV ..."
        print d_report
        print l_header

    # If file not writable then console
    file_handle = open(file_name,'w') if file_name else sys.stdout

    csv_writer = csv.writer(file_handle)

    # Construct headers to be written to csv first
    # first element intentionally left blank for this function to be generic
    t_tenant_header = []
    t_tenant_header.append("")

    for header in l_header:
        t_tenant_header.append(header)

    csv_writer.writerow(t_tenant_header)

    # Construct each tenant row as a list so that it can be consumed by pycsv
    for k in d_report:
        t_tenant_name = k
        t_tenant_values = d_report[k]

        t_tenant_row = []
        t_tenant_row.append(t_tenant_name)
        for header in l_header:
            t_tenant_row.append(t_tenant_values[header])

        csv_writer.writerow(t_tenant_row)


# def main():
#     parser = argparse.ArgumentParser(description="Command-line interface for generating reports for Openstack clusters")
#
#     group = parser.add_mutually_exclusive_group(required=True)
#     group.add_argument('-f', '--flavorcount', help='Per tenant flavorcount',
#                        action="store_true", default=False)
#     group.add_argument('-u', '--utilization', help='Per tenant utilization',
#                        action="store_true", default=False)
#
#     parser.add_argument('-o', '--output', help='Destination file to store result')
#     parser.add_argument('-d', '--debug', help='Enable Debug',action="store_true")
#     parser.add_argument('--version', action='version', version='1.0')
#
#     cli_opts = parser.parse_args()
#
#     output_file = cli_opts.output
#
#     if cli_opts.debug == True:
#         global _debug
#         _debug = True
#         print "[+] %s" % cli_opts
#
#     if cli_opts.flavorcount == True:
#         # Compute dict of tenantwise flavorcount for all tenants
#         report = get_all_tenant_flavorcount()
#
#         # Prepare report header
#         report_headers = []
#         for flavors in flavorListDefault:
#             report_headers.append(flavors)
#         report_headers.append("custom")
#
#         # Write the report alongwith header to target
#         csv_report(report,report_headers,output_file)
#         return
#
#     if cli_opts.utilization == True:
#         # Compute tenantwise utilization for all tenants
#         report = get_all_tenant_utilization()
#
#         # Prepare report header
#         report_headers = [
#             'Inst_Prov',
#             'Inst_Active',
#             'VCPU_Prov',
#             'VCPU_Active',
#             'RAM_Prov',
#             'RAM_Active',
#             'Disk_Prov_GB',
#             'FloatIP_Alloc',
#             'FloatIP_Disassoc',
#             'Vols_Prov',
#             'Vols_Prov_GB',
#             'Object_Containers',
#             'Object_Count',
#             'Object_Storage_Used_GB'
#         ]
#         # Write header + report to target
#         csv_report(report,report_headers,output_file)


def go_main():
    return 0

if __name__ == "__main__":
    # data = get_all_tenant_utilization()
    # attributes = data['admin']['Networks_Attributes']  #get tenant from tenant table nhe
    # print attributes
    # print attributes[0]#['status']
    #
    # # get_users_per_tenant_details()
    #
    # # print get_hypervisor_all_compute_utilization()
    #

    # data = get_all_tenant_flavorcount()
    # data = get_quotas_limit_details()
    # json_data = data['admin']['limits_compute']
    # print type(json_data)
    # obj_data = json.dumps(json_data, sort_keys=False).encode('utf-8')
    # print obj_data


    # get_dbformat_compute_quotas_from_op()


    # try:
    #     get_dbformat_compute_limits_from_op()
    #     mydb = resource_db.resource_db()
    #     if mydb.connect_db(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
    #         print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
    #         exit(-1)
    #     data_list = get_dbformat_networks_quotas_from_op()
    #     for data in data_list:
    #         add_quotas_limits_2_db(mydb, table='tenants_quota_network_rm', data=data)
    #
    # except (KeyboardInterrupt, SystemExit):
    #     print 'Exiting Resource Management'
    #     exit()


    # check user quota and limits
    # get_quotas_limit_details()

    # check user list
    users_dat= get_users_per_tenant()
    print users_dat