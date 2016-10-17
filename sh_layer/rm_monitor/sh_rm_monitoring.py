#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast
import collections
import os
import re
import sys

import cinderclient.v1.client as cinderclient
import keystoneclient.v2_0.client as keystoneclient
import swiftclient.client as swiftclient
from keystoneauth1 import session
from keystoneauth1.identity import v2
from neutronclient.neutron import client as neutronclient
from novaclient import client as novaclient

from sh_layer.rm_db import resource_db
from sh_layer.common.consts import *

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
                  'db_name': 'rm_mano_v1'
                 }

os_username = 'admin'
os_password = 'fncp2015'
os_auth_url = "http://116.89.184.94:5000/v2.0/"
_debug = False
# new para
os_url = 'http://116.89.184.94:35357/v2.0'


# Static flavors list
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

# --
# get credentials from open-stack services
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
   # d['tenant_name'] = os.environ['OS_TENANT_NAME']
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

def get_nova_client(p_project_id):
    return novaclient.Client(version=2, username= os_username, api_key=os_password, tenant_id=p_project_id, auth_url=os_auth_url, service_type='compute')

def get_neutron_client(p_project_id):
    return neutronclient.Client('2.0', auth_url=os_auth_url, token=get_keystone_client().auth_token, username=os_username, tenant_id=p_project_id, password=os_password, public_network='public')

def get_cinder_client(p_project_id):
    return cinderclient.Client(username=os_username, api_key=os_password, tenant_id=p_project_id, auth_url=os_auth_url)

def get_keystone_client():
    creds = get_keystone_creds()
    return keystoneclient.Client(**creds)

#
# get keystone function which is used in get_users_per_tenant_details() function to call
# "tenants.list_users(tenant.id)"
#
def get_keystone(p_project_id):
    """Returns a Keystone.Client instance."""
    auth = v2.Password(username=os_username, password=os_password,
                       tenant_id=p_project_id, auth_url=os_auth_url)
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
# get_vnfs_details()
# Returns vpcu, vmem, disk, floatingIP for a given tenant
#
def get_vnfs_details(p_nova_client):
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
    summary['vnfs_in_use']             = cnt_instances
    summary['vnfs_active']             = cnt_instances_active
    summary['vcpus_in_use']            = cnt_vcpu
    summary['vcpus_active']            = cnt_vcpu_active

    summary['ram_in_use']             = cnt_ram
    summary['ram_active']             = cnt_ram_active
    summary['disk_in_use']            = cnt_disk + cnt_ephemeral
    # summary['total_ephemeral']      = cnt_ephemeral # TODO (rickyhai) separate later when needed
    summary['floatingip_in_use']      = cnt_floatip # allocated already
    summary['floatingip_disassociate'] = cnt_floatip_disassociated

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
    # t_networks_dict = p_neutron_client.list_networks()['networks']
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
    # t_ports_dict = p_neutron_client.list_ports()['ports']
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
    # {u'external_gateway_info': {u'network_id': u'6b971d7b-f1ad-4b78-977b-44ac5c871c04', u'enable_snat': True,
    # u'external_fixed_ips': [{u'subnet_id': u'9f048ae2-182d-4230-a20d-4367e563ace9', u'ip_address': u'172.24.4.3'},
    # {u'subnet_id': u'a2118904-eaaa-4d2a-b0e7-2e6e61191f3c', u'ip_address': u'2001:db8::3'}]}, u'tenant_id': u'c1bb85f009f647139c767eeaaba3d258',
    # u'id': u'e233f701-2969-4644-bc27-84ad979a5880', u'name': u'test1'}]

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
    t_floatingips_used = len(p_neutron_client.list_floatingips(**kwargs)['floatingips'])
    t_floatingips_available = t_floatingips_total - t_floatingips_used

    t_lbaas_vips_total = 0
    t_lbaas_pools_total = 0

    # filter to get floating id and status of corresponding floating id in a dict format
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

    # counting floating ip which are inactive or active
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

    summary['networks_in_use']                = t_networks_total # in_use = active + inactive
    summary['networks_active']         = t_networks_active
    summary['networks_inactive']       = t_networks_inactive
    summary['networks_attributes']     = t_networks_attributes

    summary['ports_in_use']                   = t_ports_total
    summary['ports_active']            = t_ports_active
    summary['ports_inactive']          = t_ports_inactive
    summary['ports_attributes']        = t_ports_attributes

    summary['floatingips_total']         = t_floatingips_total
    summary['floatingips_in_use']       = t_floatingips_used
    summary['floatingips_available']   = t_floatingips_available
    summary['floatingip_active']       = t_floatingips_active
    summary['floatingip_inactive']     = t_floatingips_inactive
    summary['floatingip_attributes']   = t_floatingips_attributes

    summary['routers_in_use']                 = t_routers_total
    summary['total_routers_active']          = t_routers_active # active router
    summary['total_routers_inactive']        = t_routers_inactive
    summary['total_routers_attributes']      = t_routers_attributes

    summary['subnets_in_use']                 = t_subnets_total
    # summary['total_subnets_active']          = t_subnets_active
    # summary['total_subnets_inactive']        = t_subnets_inactive
    summary['subnets_attributes']      = t_subnets_attributes

    summary['snat_external_gateway']   = t_snat_external_gateway
    summary['lbaas_vips']              = t_lbaas_vips_total
    summary['lbaas_pools']             = t_lbaas_pools_total

    return summary

def _estimate_total_ip(p_neutron_client):
    # global public_network

    total_ip = 0
    subnet_mask = re.compile('[^/]+/(\d{1,2})')
    # subnets_from_public_network = []
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
    # print "total number of floating IP: %d " % total_ip
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
    summary['vols_count'] = len(volumelist)
    summary['vols_size_in_use'] = total_provisioned
    summary['snapshots_count'] = len(snapshotlist)
    summary['snapshots_size_in_use'] = total_volume_snapshots_provisioned
    return summary


# --
# sync_flavor_usage_all_projects()
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
def sync_flavor_usage_all_projects():
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
# sync_resource_usage_all_projects()
# Returns a (k,v) dict where k = tenant name and v is dict of pulled values
#
def sync_resource_usage_all_projects():
    '''
    Get all resource usage for all tenants/projects
    :return: (dict) resource usage included compute, network, storage for all tenants /projects
    '''
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()

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

    for tenant in tenant_list:

        # Skip disabled tenants
        if tenant.enabled == False:
            t_tenant_name                          = tenant.name
            t_users_cnt                            = 'disabled'
            t_users_list                           = 'disabled'
            t_instances                            = 'disabled'
            t_instances_active                     = 'disabled'
            t_vcpu                                 = 'disabled'
            t_vcpu_active                          = 'disabled'
            t_ram                                  = 'disabled'
            t_ram_active                           = 'disabled'
            t_disk_ephemeral                       = 'disabled'
            t_float_allocated                      = 'disabled'
            t_float_disassociated                  = 'disabled'
            t_persist_volcount                     = 'disabled'
            t_persist_provisioned_vol_value        = 'disabled'
            t_persist_snapshot_count               = 'disabled'
            t_persist_provisioned_snapshot_value   = 'disabled'
            t_networks_total                       = 'disabled'
            t_networks_active                      = 'disabled'
            t_networks_inactive                    = 'disabled'
            t_networks_attributes                  = 'disabled'
            t_ports_total                          = 'disabled'
            t_ports_active                         = 'disabled'
            t_ports_inactive                       = 'disabled'
            t_ports_attributes                     = 'disabled'
            t_floatingips_total                    = 'disabled'
            t_floatingips_usage                    = 'disabled'
            t_floatingips_available                = 'disabled'
            t_floatingips_active                   = 'disabled'
            t_floatingips_inactive                 = 'disabled'
            t_floatingips_attributes               = 'disabled'
            t_routers_total                        = 'disabled'
            t_routers_active                       = 'disabled'
            t_routers_inactive                     = 'disabled'
            t_routers_attributes                   = 'disabled'
            t_subnets_total                        = 'disabled'
            t_subnets_attributes                   = 'disabled'
            t_snat_external_gateway                = 'disabled'
            t_lbaas_vips_total                     = 'disabled'
            t_lbaas_pools_total                    = 'disabled'


        else :

            # get keystone client from get_keystone(p_tenant_name) function which have 'power'
            # to fully access keystone functions in lib
            t_keystone = get_keystone(tenant.name)
            t_users_cnt = len(t_keystone.tenants.list_users(tenant.id))
            t_users_list = t_keystone.tenants.list_users(tenant.id)

            nova = get_nova_client(tenant.name)
            cinder = get_cinder_client(tenant.name)
            # swift = get_swift_client(tenant.name)
            neutron = get_neutron_client(tenant.name)

            compute_summary = get_vnfs_details(nova)
            storage_summary = get_volume_details(cinder)
            # object_summary  = get_object_details(swift)
            neutron_summary = get_networks_details(neutron)

            t_tenant_name               = tenant.name
            t_users_cnt                 = t_users_cnt
            t_users_list                = t_users_list
            t_instances                 = compute_summary['total_instances']
            t_instances_active          = compute_summary['total_instances_active']
            t_vcpu                      = compute_summary['total_vcpu']
            t_vcpu_active               = compute_summary['total_vcpu_active']
            t_ram                       = compute_summary['total_ram']  # / 1024
            t_ram_active                = compute_summary['total_ram_active']  # / 1024
            t_disk_ephemeral            = compute_summary['total_disk'] + compute_summary['total_ephemeral']
            t_float_allocated           = compute_summary['total_floatingip_allocated']
            t_float_disassociated       = compute_summary['total_floatingip_disassocated']
            t_persist_volcount          = storage_summary['total_vols_count']
            t_persist_provisioned_vol_value            = storage_summary['total_vols_provisioned_capacity']
            t_persist_snapshot_count                   = storage_summary['total_snapshots_count']
            t_persist_provisioned_snapshot_value       = storage_summary['total_snapshots_provisioned_capacity']
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
            aggr_persist_provisioned_vol_value         = aggr_persist_provisioned_vol_value + t_persist_provisioned_vol_value
            aggr_persist_snapshot_count                = aggr_persist_snapshot_count + t_persist_snapshot_count
            aggr_persist_provisoned_snapshots_value    = aggr_persist_provisoned_snapshots_value + t_persist_provisioned_snapshot_value

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

        # Inst_Prov,Inst_Active,VCPU_Prov,VCPU_Active,RAM_Prov,RAM_Active,Disk_Prov_GB,FloatIP_Alloc,FloatIP_Disassoc,
        # Vols_Prov,Vols_Prov_GB,Object_Containers,Object_Count,Object_Storage_Used_GB"
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
            'Snapshot_Prov'         : aggr_persist_snapshot_count,
            'Snapshot_Prov_GB'      : aggr_persist_provisoned_snapshots_value,
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


# get actual resource usage from VIM with proper DB format
def sync_resource_usage_for_project(project_id):
    '''
    syn function to get actual resource usage from vim
    sync in_use resource only from vim
    :param project_id:
    :return: resource usage (dict)
    '''
    nova = get_nova_client(project_id)
    cinder = get_cinder_client(project_id)
    neutron = get_neutron_client(project_id)

    compute_summary = get_vnfs_details(nova)
    storage_summary = get_volume_details(cinder)
    neutron_summary = get_networks_details(neutron)

    # resource_usage['nova'] = compute_summary
    # resource_usage['cinder'] = storage_summary
    # resource_usage['neutron'] = neutron_summary

    resource_usage = collections.defaultdict(dict)
    # init resource usage to store in DB (sync VIM <-> rm DB)
    for resource in NOVA_QUOTA_FIELDS:
        resource_usage[resource] = collections.defaultdict(dict)
        if resource == 'vcpus':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = compute_summary['vcpus_in_use']
        if resource == 'vnfs':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = compute_summary['vnfs_in_use']
        if resource == 'vmemory':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = compute_summary['ram_in_use']
        if resource == 'floating_ips':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = compute_summary['floatingip_in_use']

    for resource in CINDER_QUOTA_FIELDS:
        resource_usage[resource] = collections.defaultdict(dict)
        if resource == 'volumes':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = storage_summary['vols_size_in_use']
        if resource == 'snapshots':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = storage_summary['snapshots_size_in_use']
        if resource == 'gigabytes':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = compute_summary['disk_in_use']  # pickup from compute resources
                                                                                 # (get_vnfs_detail() function)

    for resource in NEUTRON_QUOTA_FIELDS:
        resource_usage[resource] = collections.defaultdict(dict)
        if resource == 'network':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = neutron_summary['networks_in_use']
        if resource == 'subnet':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = neutron_summary['subnets_in_use']
        if resource == 'port':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = neutron_summary['ports_in_use']
        if resource == 'router':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = neutron_summary['routers_in_use']
        if resource == 'floatingip':
            resource_usage[resource]['project_id'] = project_id
            resource_usage[resource]['resource'] = resource
            resource_usage[resource]['in_use'] = neutron_summary['floatingips_in_use']
    return resource_usage

# --
# Sync absolute limits and actual 'in_use' details for a given project from VIM to NFVO
#
def sync_hard_limits(project_id):

    nova = get_nova_client(project_id)
    cinder = get_cinder_client(project_id)
    neutron = get_neutron_client(project_id)

    """Retrieves quotas limit only for a given project"""
    sync_quota_from_vim = collections.defaultdict(dict)
    sync_quota_from_vim['nova'] = collections.defaultdict(dict)
    sync_quota_from_vim['cinder'] = collections.defaultdict(dict)
    sync_quota_from_vim['neutron'] = collections.defaultdict(dict)

    # Nova Quotas for a project
    # using nova quota-show --tenant $tenant command to see output format
    quotas_nova = nova.quotas.get(tenant_id=project_id)
    for item in ('cores', 'fixed_ips', 'floating_ips', 'instances',
        'key_pairs', 'ram', 'security_groups','security_group_rules', 'server_groups', 'server_group_members'):
        if item == 'ram':
            setattr(quotas_nova, item, getattr(quotas_nova, item)) #* 1024 * 1024
        sync_quota_from_vim['nova'][item] = getattr(quotas_nova, item)

    #=====================================================================================================
    # Quotas Networks
    #=====================================================================================================
    """Retrieves tenant quotas from Neutron- Networks API"""
    # get Networks-tenant quotas
    quotas_networks = neutron.show_quota(tenant_id=project_id)['quota']
    for item in ('subnet', 'network', 'floatingip', 'subnetpool', 'security_group_rule',
          'security_group', 'router', 'rbac_policy',  'port'):
        sync_quota_from_vim['neutron'][item] = quotas_networks[item]

    #=====================================================================================================
    # Quotas and limits Cinder
    #=====================================================================================================
    """Retrieves tenant quotas from cinder- Cinder API v2"""
    # get cinder-tenant quotas
    # quotas_cinder: {'per_volume_gigabytes': {u'limit': -1, u'reserved': 0, u'in_use': 0}}
    quotas_cinder = cinder.quotas.get(tenant_id=project_id, usage=True)
    for item in ('backup_gigabytes', 'backups', 'gigabytes', 'gigabytes_lvmdriver-1',
        'per_volume_gigabytes', 'snapshots', 'snapshots_lvmdriver-1','volumes', 'volumes_lvmdriver-1'):
        sync_quota_from_vim['cinder'][item] = quotas_cinder[item]['limit']
        # sync_quota_from_vim['cinder'][item] = getattr(quotas_cinder, item)

    return sync_quota_from_vim

# --
# Get absolute limits details for all tenants
#
def sync_hard_limits_all_projects():
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


            """Retrieves quotas and limits for each of tenant from compute API"""
            q[t_tenant_name] = {'limits_compute': {'tenant_id': tenant.id, 'tenant_name': tenant.name},
                                'quotas_compute': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'quotas_networks': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'limits_cinder': {'tenant_id': tenant.id,'tenant_name': tenant.name},
                                'quotas_cinder': {'tenant_id': tenant.id,'tenant_name': tenant.name}
                                }
            #=====================================================================================================
            # Quotas and limits Compute resources
            #=====================================================================================================
            # Get Nova-absolute limits for tenant
            limits = nova.limits.get(tenant_id=tenant.id).absolute
            for limit in limits:
                if 'ram' in limit.name.lower():
                    limit.value = limit.value #* 1024.0 * 1024.0
                q[t_tenant_name]['limits_compute'][limit.name] = limit.value
            # print "Limits of compute resources for all tenants are : %s" % (q[t_tenant_name]['limits_compute'])
            limits = nova.limits.get(tenant_id='f4211c8eee044bfb9dea2050fef2ace5').to_dict()
            resource_usage = collections.defaultdict(dict)
            resource_usage['ram'] = limits['absolute']['totalRAMUsed']
            resource_usage['cores'] = limits['absolute']['totalCoresUsed']
            resource_usage['instances'] = \
                limits['absolute']['totalInstancesUsed']
            print resource_usage

            # Nova Quotas for tenant

            quotas = nova.quotas.get(tenant_id=tenant.id)
            for item in ('cores', 'fixed_ips', 'floating_ips', 'instances',
                'key_pairs', 'ram', 'security_groups','security_group_rules', 'server_groups', 'server_group_members'):
                if item == 'ram':
                    setattr(quotas, item, getattr(quotas, item)) #* 1024 * 1024

                q[t_tenant_name]['quotas_compute'][item] = getattr(quotas, item)
            # print "Quotas of compute resources are: %s" %( q[t_tenant_name]['quotas_compute'])


            #=====================================================================================================
            # Quotas Networks
            #=====================================================================================================
            """Retrieves tenant quotas from Neutron- Networks API"""
            # get Networks-tenant quotas
            # q[t_tenant_name] = {'quotas_networks': {'tenant_id': tenant.id,'tenant_name': tenant.name}}
            quotas_networks = neutron.show_quota(tenant_id=tenant.id)['quota']
            for item in ('subnet', 'network', 'floatingip', 'subnetpool', 'security_group_rule',
                  'security_group', 'router', 'rbac_policy',  'port'):
                q[t_tenant_name]['quotas_networks'][item] = quotas_networks[item]
                # q[t_tenant_name]['quotas_networks'][item]=getattr(quotas_networks, item)
            # print "Quotas of networks are: %s" % (q[t_tenant_name]['quotas_networks'])


            #=====================================================================================================
            # Quotas and limits Cinder
            #=====================================================================================================
            """Retrieves tenant quotas from cinder- Cinder API v2"""

            # Get cinder-absolute limits for tenant
            try:
                limits_cinder = cinder.limits.get().absolute
            except Exception:
                continue
            for limit_cinder in limits_cinder:
                # if 'Giga' in limit_cinder.name:
                #     limit_cinder.value = limit_cinder.value * 1024 * 1024 * 1024
                q[t_tenant_name]['limits_cinder'][limit_cinder.name] = limit_cinder.value
            # print "Limits of cinder are: %s "% (q[t_tenant_name]['limits_cinder'])

            # get cinder-tenant quotas
            quotas_cinder = cinder.quotas.get(tenant_id=tenant.id, usage=True)
            for item in ('backup_gigabytes', 'backups', 'gigabytes', 'gigabytes_lvmdriver-1',
                'per_volume_gigabytes', 'snapshots', 'snapshots_lvmdriver-1','volumes', 'volumes_lvmdriver-1'):
                # if 'Giga' in item:
                #     setattr(quotas_cinder, item, getattr(quotas_cinder, item)) * 1024 * 1024 * 1024
                q[t_tenant_name]['quotas_cinder'][item] = getattr(quotas_cinder, item)
                # d[t_tenant_name]['quotas_cinder'][item] = quotas_cinder[item]
            # print "Storage Quota- Cinder are : %s" % q[t_tenant_name]['quotas_cinder']

    return q

# get default quota for a given tenant in case quota for that tenant is not set and  store in DB
def sync_default_quota_(project_id):
    # TODO (rickyhai) implement sync function to get default quota from vim to rm db
    return


# --
# convert quota compute to DB format for storing (json format) - for tenant quota-compute table
#

def build_dbformat_hard_limit_compute_all_projects():
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()

    quotas_compute_list = []
    data = sync_hard_limits_all_projects()

    for tenant in tenant_list:
        quotas_compute                             = data[tenant.name]['quotas_compute']

        quotas_compute['max_vmem']                 =quotas_compute.pop('ram')
        quotas_compute['max_vcpus']                =quotas_compute.pop('cores')
        quotas_compute['max_vnfs']                 =quotas_compute.pop('instances')
        quotas_compute['max_server_groups']        =quotas_compute.pop('server_groups')
        quotas_compute['max_server_group_members'] =quotas_compute.pop('server_group_members')
        quotas_compute['max_floating_ips']         =quotas_compute.pop('floating_ips')
        quotas_compute['max_fixed_ips']            =quotas_compute.pop('fixed_ips')
        quotas_compute['max_key_pairs']            =quotas_compute.pop('key_pairs')
        quotas_compute['max_security_group_rules'] =quotas_compute.pop('security_group_rules')
        quotas_compute['max_security_groups']      =quotas_compute.pop('security_groups')

        # obj_quotas_compute.append(json.dumps(json_quotas_compute, sort_keys=False).encode('utf-8'))
        quotas_compute_list.append(quotas_compute)
    return quotas_compute_list  # TODO (ricky) implement function to add synced quotas from vim to db

# --
# convert limits compute to DB format for storing (json format)
#
def build_dbformat_resource_usage_compute_all_projects():
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()

    # Initiate list of usage compute records that will be stored into DB
    limits_compute_list = []

    data = sync_hard_limits_all_projects()
    # resource utilization metrics for all tenants
    data_tenant_utilization = sync_resource_usage_all_projects()

    for tenant in tenant_list:
        # dict contains upper letters
        limits_compute_orgi = data[tenant.name]['limits_compute']

        # convert all key of dict to lower letters
        limits_compute = dict((k.lower(), v) for k, v in limits_compute_orgi.iteritems())

        # combine data from tenant utilization function to get needed format with full fields to store in DB
        tenant_compute_util = data_tenant_utilization[tenant.name]

        limits_compute['max_total_vcpus']                                 = limits_compute.pop('maxtotalcores')
        # total number of vcpu are allocated to users in a given tenant
        # limits_compute['total_vcpus_allocated']                         = 0
        limits_compute['total_vcpus_used']                                = limits_compute.pop('totalcoresused')
        limits_compute['total_vcpus_active']                              = tenant_compute_util['VCPU_Active']  #  total number of vcpus are assigned to instance already

        limits_compute['max_total_vmem_size']                             = limits_compute.pop('maxtotalramsize')
        # limits_compute['total_vmem_allocated']                            = 0
        limits_compute['total_vmem_used']                                 = limits_compute.pop('totalramused')
        limits_compute['total_vmem_active']                               = tenant_compute_util['RAM_Active']

        limits_compute['max_total_vnfs']                                  = limits_compute.pop('maxtotalinstances')
        # limits_compute['total_vnfs_allocated']                          = 0
        limits_compute['total_vnfs_used']                                 = limits_compute.pop('totalinstancesused')
        limits_compute['total_vnfs_active']                               = tenant_compute_util['Inst_Active']

        limits_compute['max_total_floatingips']                           = limits_compute.pop('maxtotalfloatingips')
        # limits_compute['total_floatingips_allocated']                   = 0
        limits_compute['total_floatingips_used']                          = limits_compute.pop('totalfloatingipsused')
        limits_compute['total_floatingips_disassociated']                 = tenant_compute_util['FloatIP_Disassoc']

        limits_compute_list.append(limits_compute)
        print limits_compute_list
    return limits_compute_list   # TODO (ricky) implement function to add synced quotas from vim to db


# --
# convert quota networks (neutron) to DB format for storing (json format)
#

def build_dbformat_resource_usage_networks_all_projects():
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()

    # Initiate list of usage networks records that will be stored into DB
    quotas_networks_list = []
    # Quotas and limits for all tenants - compute + networks + storage resources
    data_quotas_limits = sync_hard_limits_all_projects()
    # Tenant utilization metrics for all tenants
    data_projects_utilization = sync_resource_usage_all_projects()

    for tenant in tenant_list:
        quotas_network_utilization = data_quotas_limits[tenant.name]['quotas_networks']
        # combine data from tenant utilization function to get needed format with full fields to store in DB
        tenant_networks_util = data_projects_utilization[tenant.name]
        print tenant_networks_util['Networks_Prov']
        print quotas_network_utilization['network']

        # quotas_network_utilization['tenant_name']                         = tenant.name
        # quotas_network_utilization['tenant_id']                           = tenant.id
        quotas_network_utilization['max_network']                         = quotas_network_utilization.pop('network')
        # TODO(ricky) hierarchy projects/users support
        # quotas_network_utilization['total_network_allocated']             = 0
        quotas_network_utilization['total_network_used']                  = tenant_networks_util['Networks_Prov']
        quotas_network_utilization['total_network_active']                = tenant_networks_util['Networks_Active']
        quotas_network_utilization['total_network_inactive']              = tenant_networks_util['Networks_Inactive']

        quotas_network_utilization['max_router']                          = quotas_network_utilization.pop('router')
        # quotas_network_utilization['total_router_allocated']              = 0
        quotas_network_utilization['total_router_used']                   = tenant_networks_util['Routers_Prov']
        quotas_network_utilization['total_router_active']                 = tenant_networks_util['Routers_Active']
        quotas_network_utilization['total_router_inactive']               = tenant_networks_util['Routers_Inactive']

        quotas_network_utilization['max_port']                            = quotas_network_utilization.pop('port')
        # quotas_network_utilization['total_port_allocated']                = 0
        quotas_network_utilization['total_port_used']                     = tenant_networks_util['Ports_Prov']
        quotas_network_utilization['total_port_active']                   = tenant_networks_util['Ports_Active']
        quotas_network_utilization['total_port_inactive']                 = tenant_networks_util['Ports_Inactive']

        quotas_network_utilization['max_floatingip']                      = quotas_network_utilization.pop('floatingip')
        # quotas_network_utilization['total_floatingip_allocated']          = 0
        quotas_network_utilization['total_floatingip_used']               = tenant_networks_util['Floating_IPs_Usage']
        quotas_network_utilization['total_floatingip_available']          = tenant_networks_util['Floating_IPs_Available']
        quotas_network_utilization['total_floatingip_active']             = tenant_networks_util['Floating_IPs_Active']
        quotas_network_utilization['total_floatingip_inactive']           = tenant_networks_util['Floating_IPs_Inactive']

        quotas_network_utilization['max_subnet']                          = quotas_network_utilization.pop('subnet')
        # quotas_network_utilization['total_subnet_allocated']              = 0
        quotas_network_utilization['total_subnet_used']                   = tenant_networks_util['Subnets_Prov']

        quotas_network_utilization['max_subnetpool']                      = quotas_network_utilization.pop('subnetpool')
        quotas_network_utilization['max_security_group_rule']             = quotas_network_utilization.pop('security_group_rule')
        quotas_network_utilization['max_security_group']                  = quotas_network_utilization.pop('security_group')
        quotas_network_utilization['max_rbac_policy']                     = quotas_network_utilization.pop('rbac_policy')

        # obj_quotas_compute.append(json.dumps(json_quotas_compute, sort_keys=False).encode('utf-8'))
        quotas_networks_list.append(quotas_network_utilization)
    return quotas_networks_list

# --
# combine tenant limits and tenant utilization  that related to storage resource to store into DB with proper format
#
def build_dbformat_resource_usage_storage_all_projects():
    '''
    Out put data - quota and limit storage format from sync_hard_limits_all_projects() function
    	'quotas_cinder':
		{'per_volume_gigabytes': {u'limit': -1, u'reserved': 0, u'in_use': 0}, 'snapshots_lvmdriver-1': {u'limit': -1, u'reserved': 0, u'in_use': 0},
		'gigabytes': {u'limit': 1000, u'reserved': 0, u'in_use': 0}, 'tenant_id': u'24104f8dd8074d5aae884f25a583e3d4',
		'backup_gigabytes': {u'limit': 1000, u'reserved': 0, u'in_use': 0}, 'snapshots': {u'limit': 10, u'reserved': 0, u'in_use': 0},
		'gigabytes_lvmdriver-1': {u'limit': -1, u'reserved': 0, u'in_use': 0}, 'volumes': {u'limit': 10, u'reserved': 0, u'in_use': 0},
		'tenant_name': u'admin', 'volumes_lvmdriver-1': {u'limit': -1, u'reserved': 0, u'in_use': 0}, 'backups': {u'limit': 10, u'reserved': 0, u'in_use': 0}},

		'limits_cinder':
		{u'totalSnapshotsUsed': 0, u'maxTotalBackups': 10, u'maxTotalVolumeGigabytes': 1000, u'maxTotalSnapshots': 10, u'maxTotalBackupGigabytes': 1000,
		'tenant_id': u'24104f8dd8074d5aae884f25a583e3d4', u'totalBackupGigabytesUsed': 0, u'maxTotalVolumes': 10, u'totalVolumesUsed': 0,
		'tenant_name': u'admin', u'totalBackupsUsed': 0, u'totalGigabytesUsed': 0}},

    :return:
    '''
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()

    # Initiate list of usage storage records that will be stored into DB
    quotas_storage_list = []
    tenant_storage_util = {}

    # get quota and limit quota data
    data = sync_hard_limits_all_projects()

    #  resource utilization metrics for all tenants
    # data_tenant_utilization = sync_resource_usage_all_projects()

    for tenant in tenant_list:
        # limits storage dict contains upper letters that need to be convert to lower letter
        # when storing in DB if it is used

        # usage quota storage for a given tenant
        tenant_quotas_storage_util = data[tenant.name]['quotas_cinder']
        print tenant_quotas_storage_util

        # data from tenant utilization function to get needed format with full fields to store in DB

        tenant_storage_util['tenant_name']                              = tenant.name
        tenant_storage_util['tenant_id']                                = tenant.id

        tenant_storage_util['max_total_gigabytes']                      = tenant_quotas_storage_util['gigabytes']['limit']
        # tenant_storage_util['total_gigabytes_allocated']                = 0
        tenant_storage_util['total_gigabytes_used']                     = tenant_quotas_storage_util['gigabytes']['in_use']

        # tenant_storage_util['max_total_gigabytes_lvmdriver-1']          = tenant_quotas_storage_util['gigabytes_lvmdriver-1']['limit']
        # tenant_storage_util['total_gigabytes_lvmdriver-1_allocated']    = 0 # total number of gigabytes are allocated to users in a given tenant
        # tenant_storage_util['total_gigabytes_lvmdriver-1_used']         = tenant_quotas_storage_util['gigabytes_lvmdriver-1']['in_use']

        tenant_storage_util['max_total_backup_gigabytes']               = tenant_quotas_storage_util['backup_gigabytes']['limit']
        # tenant_storage_util['total_backup_gigabytes_allocated']         = 0
        tenant_storage_util['total_backup_gigabytes_used']              = tenant_quotas_storage_util['backup_gigabytes']['in_use']

        tenant_storage_util['max_total_backup']                      = tenant_quotas_storage_util['backups']['limit']
        # tenant_storage_util['total_backup_allocated']                = 0
        tenant_storage_util['total_backup_used']                     = tenant_quotas_storage_util['backups']['in_use']

        tenant_storage_util['max_total_snapshots']                   = tenant_quotas_storage_util['snapshots']['limit']
        # tenant_storage_util['total_snapshots_allocated']             = 0
        tenant_storage_util['total_snapshots_used']                  = tenant_quotas_storage_util['snapshots']['in_use']

        # tenant_storage_util['max_total_snapshots_lvmdriver-1']           = tenant_quotas_storage_util['snapshots_lvmdriver-1']['limit']
        # tenant_storage_util['total_snapshots_lvmdriver-1_allocated']     = 0
        #  get data from sync_resource_usage_all_projects() function: 'Snapshot_Prov_GB' : t_persist_provisioned_snapshot_value,
        # tenant_storage_util['total_snapshots_lvmdriver-1_used']          = tenant_quotas_storage_util['snapshots_lvmdriver-1']['in_use']


        tenant_storage_util['max_total_volumes']           = tenant_quotas_storage_util['volumes']['limit']
        # tenant_storage_util['total_volumes_allocated']     = 0
        tenant_storage_util['total_volumes_used']          = tenant_quotas_storage_util['volumes']['in_use']

        # tenant_storage_util['max_total_volumes_lvmdriver-1']           = tenant_quotas_storage_util['volumes_lvmdriver-1']['limit']
        # tenant_storage_util['total_volumes_lvmdriver-1_allocated']     = 0
        # get data from sync_resource_usage_all_projects() function: 'Snapshot_Prov_GB' : t_persist_provisioned_snapshot_value,
        # tenant_storage_util['total_volumes_lvmdriver-1_used']          = tenant_quotas_storage_util['volumes_lvmdriver-1']['in_use']

        quotas_storage_list.append(tenant_storage_util)
        # print limits_compute_list
    return quotas_storage_list


# --
# get_users_per_tenant_details()
# Returns number of users and list users for a given tenant, to get correctly keystone client for counting list users
# need to call get_keystone(p_tenant_name) instead of get_keystone_client() as usual
#
def _get_list_users_per_project():
    """Retrieves list of user per tenant"""
    # get keystone client from get_keystone(p_tenant_name) function which have 'power'
    # to fully access keystone functions in lib
    # Count number of users in a tenant

    # get_keystone_client() is called
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()
    print "print out tenant list"
    print tenant_list

    # initiate users_dict
    users_data = {}
    for tenant in tenant_list:

        # invoke another function to get new keystone client for getting users list per tenant
        t_keystone = get_keystone(tenant.id)

        # t_users_cnt = len(t_keystone.tenants.list_users(tenant.id))
        t_users_list = t_keystone.tenants.list_users(tenant.id)
        users_data[tenant.name] = t_users_list

    return users_data, keystone

def _convert_user_str_2_dict(data):
    '''
    this function is to convert data format from _get_list_users_per_project function : string format to dictionary
    format for each of user in a given tenant
    :param data: is string format including user info in a  given tenant
    :return: dict format of a user in a given tenant
    '''
    # notice keep a space behind "<User " in below code line to avoid the issue when using literal_eval() function
    data = str(data).lstrip('<User ')
    t_user_str = (data.rstrip('>'))
    t_user_dict= ast.literal_eval(t_user_str)
    # print t_user_dict

    return t_user_dict

def get_list_users_per_project():
    '''
    This function is to get list of users in given tenant with proper format (list of user_dict info) to store into DB
    :return:
    '''
    users_data, keystone = _get_list_users_per_project()
    tenantlist = keystone.tenants.list()
    t_users_list = []
    for tenant in tenantlist:
        t_users_data= users_data[tenant.name]

        for t_user in t_users_data:
            t_user_dict = _convert_user_str_2_dict(t_user)
            # insert tenant name and tenant id into t_user_dict to identify exactly which tenant that user is belong to
            # easier to keep track when storing in DB
            t_user_dict['tenant_name'] = tenant.name
            t_user_dict['tenant_id'] = tenant.id
            t_users_list.append(t_user_dict)

    return t_users_list


def get_resource_usage_compute_for_all_users_in_all_projects():
    '''
    this function is to get users quota in a given tenant for compute, networks and storage
    :return: user quotas for each kind of resources such as : compute, network or storage
    notice that user quota-storage is currently not supported yet.
    '''
    # get keystone client for listing out all of tenants
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()
    # print tenant_list
    per_tenant_users_util_compute_list = []
    # all_tenants_users_util_compute_list = []

    for tenant in tenant_list:
        # print " in tenant"
        # print tenant.name
        # invoke another function to get new keystone client for getting users list per tenant
        t_keystone = get_keystone(tenant.id)
        novaclient = get_nova_client(tenant.id)
        # using that above keystone client for list out users in given tenant
        t_users_list = t_keystone.tenants.list_users(tenant.id)
        # print t_users_list
        for user in t_users_list:
            users_util_compute = {}
            # print "in user"
            # print user

            """Retrieves quotas for each of user in given tenant """
            #=====================================================================================================
            # User Quota- Compute resources
            #=====================================================================================================

            user_quota_compute = novaclient.quotas.get(tenant_id=tenant.id, user_id=user.id)
            print user_quota_compute.ram

            users_util_compute['tenant_name']                     = tenant.name
            users_util_compute['tenant_id']                       = tenant.id
            users_util_compute['user_name']                       = user.name
            users_util_compute['user_id']                         = user.id
            # vcpus meters
            users_util_compute['max_vcpus']                       = user_quota_compute.cores
            users_util_compute['used_vcpus']                      = 0
            users_util_compute['reserved_vcpus']                  = 0
            users_util_compute['available_vcpus']                 = users_util_compute['max_vcpus'] - (users_util_compute['used_vcpus'] + users_util_compute['reserved_vcpus'])
            users_util_compute['percentage_vcpus_used']           = ((users_util_compute['used_vcpus']) / (users_util_compute['max_vcpus']))*100
            users_util_compute['percentage_vcpus_reserved']       = ((users_util_compute['reserved_vcpus']) / (users_util_compute['max_vcpus']))*100
            # including used + reserved resources
            users_util_compute['percentage_total_vcpus_usage']    = ((users_util_compute['reserved_vcpus'] + users_util_compute['used_vcpus']) /
                                                                        (users_util_compute['max_vcpus']))*100
            # vmem meters
            users_util_compute['max_vmem']                        = user_quota_compute.ram
            users_util_compute['used_vmem']                       = 0
            users_util_compute['reserved_vmem']                   = 0
            users_util_compute['available_vmem']                  = users_util_compute['max_vmem'] - (users_util_compute['used_vmem'] + users_util_compute['reserved_vmem'])
            users_util_compute['percentage_vmem_used']            = ((users_util_compute['used_vmem']) / (users_util_compute['max_vmem']))*100
            users_util_compute['percentage_vmem_reserved']        = ((users_util_compute['reserved_vmem']) / (users_util_compute['max_vmem']))*100
            # including used + reserved resources
            users_util_compute['percentage_total_vmem_usage']      = ((users_util_compute['reserved_vmem'] + users_util_compute['used_vmem']) /
                                                                      (users_util_compute['max_vmem']))*100
            # server groups meters
            # users_quota_compute['max_server_groups']            = user_quota_compute.server_groups
            # users_quota_compute['max_server_group_members']     = user_quota_compute.server_group_members
            # instance count meters
            users_util_compute['max_vnfs']                        = user_quota_compute.instances
            users_util_compute['used_vnfs']                       = 0
            users_util_compute['reserved_vnfs']                   = 0
            users_util_compute['available_vnfs']                  = users_util_compute['max_vnfs'] - (users_util_compute['used_vnfs'] + users_util_compute['reserved_vnfs'])
            users_util_compute['percentage_vnfs_used']            = ((users_util_compute['used_vnfs']) / (users_util_compute['max_vnfs']))*100
            users_util_compute['percentage_vnfs_reserved']        = ((users_util_compute['reserved_vnfs']) / (users_util_compute['max_vnfs']))*100
            # including used + reserved resources
            users_util_compute['percentage_total_vnfs_usage']     = ((users_util_compute['reserved_vnfs'] + users_util_compute['used_vnfs']) /
                                                                 (users_util_compute['max_vnfs']))*100
            # Floating up meters
            users_util_compute['max_floating_ips']                = user_quota_compute.floating_ips
            users_util_compute['used_floating_ips']               = 0
            users_util_compute['reserved_floating_ips']           = 0
            users_util_compute['available_floating_ips']          = users_util_compute['max_floating_ips'] - (users_util_compute['used_floating_ips'] + users_util_compute['reserved_floating_ips'])
            users_util_compute['percentage_floating_ips_used']    = ((users_util_compute['used_floating_ips']) / (users_util_compute['max_floating_ips']))*100
            users_util_compute['percentage_floating_ips_reserved']= ((users_util_compute['reserved_floating_ips']) / (users_util_compute['max_floating_ips']))*100
            # including used + reserved resources
            users_util_compute['percentage_total_floating_ips_usage'] = ((users_util_compute['reserved_floating_ips'] + users_util_compute['used_floating_ips']) /
                                                                         (users_util_compute['max_floating_ips']))*100
            # fixed ip and key pairs meters
            users_util_compute['max_fixed_ips']                   = user_quota_compute.fixed_ips
            users_util_compute['max_key_pairs']                   = user_quota_compute.key_pairs
            # Other meters
            users_util_compute['max_security_group_rules']        = user_quota_compute.security_group_rules
            users_util_compute['max_security_groups']             = user_quota_compute.security_groups
            users_util_compute['max_injected_file_content_bytes'] = user_quota_compute.injected_file_content_bytes
            users_util_compute['max_injected_file_path_bytes']    = user_quota_compute.injected_file_path_bytes

            # Append dict "users_quota_compute" to list "users_quota_compute_list" it makes us easier when storing in DB
            # print users_util_compute
            per_tenant_users_util_compute_list.append(users_util_compute)

    print per_tenant_users_util_compute_list
    return per_tenant_users_util_compute_list

def get_resource_usage_network_for_all_users_in_all_projects():
    '''
    this function is to get users quota in a given tenant for compute, networks and storage
    :return: user quotas for each kind of resources such as : compute, network or storage
    notice that user quota-storage is currently not supported yet.
    '''
    # get keystone client for listing out all of tenants
    keystone = get_keystone_client()
    tenant_list = keystone.tenants.list()
    # Initiate dicts and list for user quotas
    users_util_networks_list = []

    for tenant in tenant_list:
        # invoke another function to get new keystone client for getting users list per tenant
        t_keystone = get_keystone(tenant.id)
        neutron = get_neutron_client(tenant.id)

        # using that above keystone client for list out users in given tenant
        t_users_list = t_keystone.tenants.list_users(tenant.id)
        for user in t_users_list:
            # declare new dict for each of user.
            users_util_networks = {}

            """Retrieves quotas for each of user in given tenant"""
            #=====================================================================================================
            # User Quotas - network resources
            #=====================================================================================================
            user_quota_networks = neutron.show_quota(tenant_id=tenant.id, user_id= user.id)['quota']
            # print user_quota_networks['subnet']
            # print user_quota_networks
            users_util_networks['tenant_name']                       = tenant.name
            users_util_networks['tenant_id']                         = tenant.id
            users_util_networks['user_name']                         = user.name
            users_util_networks['user_id']                           = user.id
            # subnet meters
            users_util_networks['max_subnet']                        = user_quota_networks['subnet']
            users_util_networks['used_subnet']                       = 0
            users_util_networks['reserved_subnet']                   = 0
            users_util_networks['available_subnet']                  = users_util_networks['max_subnet'] - (users_util_networks['used_subnet'] + users_util_networks['reserved_subnet'] )
            users_util_networks['percentage_subnet_used']            = ((users_util_networks['used_subnet']) / (users_util_networks['max_subnet']))*100
            users_util_networks['percentage_subnet_reserved']        = ((users_util_networks['reserved_subnet']) / (users_util_networks['max_subnet']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_subnet_usage']     = ((users_util_networks['reserved_subnet'] + users_util_networks['used_subnet']) /
                                                                      (users_util_networks['max_subnet']))*100
            # networks meters
            users_util_networks['max_network']                       = user_quota_networks['network']
            users_util_networks['used_network']                      = 0
            users_util_networks['reserved_network']                  = 0
            users_util_networks['available_network']                 = users_util_networks['max_network'] - (users_util_networks['used_network'] + users_util_networks['reserved_network'])
            users_util_networks['percentage_network_used']           = ((users_util_networks['used_network']) / (users_util_networks['max_network']))*100
            users_util_networks['percentage_network_reserved']       = ((users_util_networks['reserved_network']) / (users_util_networks['max_network']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_network_usage']    = ((users_util_networks['reserved_network'] + users_util_networks['used_network']) /
                                                                      (users_util_networks['max_network']))*100
            # floating ip meters
            users_util_networks['max_floatingip']                    = user_quota_networks['floatingip']
            users_util_networks['used_floatingip']                   = 0
            users_util_networks['reserved_floatingip']               = 0
            users_util_networks['available_floatingip']              = users_util_networks['max_floatingip'] - (users_util_networks['used_floatingip'] + users_util_networks['reserved_floatingip'])
            users_util_networks['percentage_floatingip_used']        = ((users_util_networks['used_floatingip']) / (users_util_networks['max_floatingip']))*100
            users_util_networks['percentage_floatingip_reserved']    = ((users_util_networks['reserved_floatingip']) / (users_util_networks['max_floatingip']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_floatingip_usage'] = ((users_util_networks['reserved_floatingip'] + users_util_networks['used_floatingip']) /
                                                                      (users_util_networks['max_floatingip']))*100
            # router meters
            users_util_networks['max_router']                        = user_quota_networks['router']
            users_util_networks['used_router']                       = 0
            users_util_networks['reserved_router']                   = 0
            users_util_networks['available_router']                  = users_util_networks['max_router'] - (users_util_networks['used_router'] + users_util_networks['reserved_router'])
            users_util_networks['percentage_router_used']            = ((users_util_networks['used_router']) / (users_util_networks['max_router']))*100
            users_util_networks['percentage_router_reserved']        = ((users_util_networks['reserved_router']) / (users_util_networks['max_router']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_router_usage']     = ((users_util_networks['reserved_router'] + users_util_networks['used_router']) /
                                                                      (users_util_networks['max_router']))*100
            # port meters
            users_util_networks['max_port']                          = user_quota_networks['port']
            users_util_networks['used_port']                         = 0
            users_util_networks['reserved_port']                     = 0
            users_util_networks['available_port']                    = users_util_networks['max_port'] -  (users_util_networks['used_port'] + users_util_networks['reserved_port'])
            users_util_networks['percentage_port_used']              = ((users_util_networks['used_port']) / (users_util_networks['max_port']))*100
            users_util_networks['percentage_port_reserved']          = ((users_util_networks['reserved_port']) / (users_util_networks['max_port']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_port_usage']       = ((users_util_networks['reserved_port'] + users_util_networks['used_port']) /
                                                                      (users_util_networks['max_port']))*100
            # subnet-pools meters
            users_util_networks['max_subnetpool']                    = user_quota_networks['subnetpool']
            users_util_networks['used_subnetpool']                   = 0
            users_util_networks['reserved_subnetpool']               = 0
            users_util_networks['available_subnetpool']              = users_util_networks['max_subnetpool'] - (users_util_networks['used_subnetpool'] + users_util_networks['reserved_subnetpool'])
            users_util_networks['percentage_subnetpool_used']        = ((users_util_networks['used_subnetpool']) / (users_util_networks['max_subnetpool']))*100
            users_util_networks['percentage_subnetpool_reserved']    = ((users_util_networks['reserved_subnetpool']) / (users_util_networks['max_subnetpool']))*100
            # including used + reserved resources
            users_util_networks['percentage_total_subnetpool_usage'] = ((users_util_networks['reserved_subnetpool'] + users_util_networks['used_subnetpool']) /
                                                                      (users_util_networks['max_subnetpool']))*100
            # other meters
            users_util_networks['max_security_group']                = user_quota_networks['security_group']
            users_util_networks['max_security_group_rule']           = user_quota_networks['security_group_rule']
            users_util_networks['max_rbac_policy']                   = user_quota_networks['rbac_policy']

            # Append dict "users_quota_networks" to list "users_quota_networks_list" it makes us easier when storing in DB
            users_util_networks_list.append(users_util_networks)

            """Retrieves quotas for each of user in given tenant"""
            #=====================================================================================================
            # User Quotas - storage resources. CURRENTLY CINDER NOT SUPPORT USER QUOTA OR LIMITS AS WELL
            #=====================================================================================================
            # users_limit_storage = cinder.limits.get()
            # users_quota_storage = cinder.quotas.get(user_id=user.id)
            # TODO NEED TO IMPLEMENT THIS PART WHEN USER QUOTA IS FULLY SUPPORTED IN CINDER-OPENSTACK

    return users_util_networks_list


def get_resource_usage_storage_for_all_users_in_all_projects():
    '''
    user storage quota is not supported yet at this phase
    (https://blueprints.launchpad.net/cinder/+spec/per-project-user-quotas-support)
    :return:
    '''
    return 0


def go_main():
    return 0

if __name__ == "__main__":

    try:
        mydb = resource_db.resource_db()
        if mydb.connect(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)
        # data_list = get_resource_usage_compute_for_all_users_in_all_projects()
        # # data_list = get_resource_usage_network_for_all_users_in_all_projects()
        # for data in data_list:
        #     add_resource_2_db(mydb, table='users_util_compute_rm', data=data)
        d= sync_resource_usage_for_project('25970fbcfb0a4c2fb42ccc18f1bccde3')
        print d

    except (KeyboardInterrupt, SystemExit):
        print 'Exiting Resource Management'
        exit()