'''
Created on 2016. 2. 1.

@author: Ricky Hai
'''
from novaclient.client import Client
from datetime import datetime
from time import mktime

global config 
config = {
    'VERSION': '2',
    'AUTH_URL': "http://116.89.184.94:5000/v2.0/",
    'USERNAME': "admin",
    'PASSWORD': "fncp2015",
    'TENANT_ID': "1975c8ee1c7c4229bdd909ad662fcbe6",
    'TENANT_NAME': "admin",
    'SERVICE_TYPE': 'compute'}

class polling_op_compute_capacity():
    
    def __init__(self, nova_client):
        self.nova_client = nova_client
        self.last_stats = None
    def get_stats(self,nova_client):
        self.nova_client.authenticate()
        data = nova_client.hypervisor_stats.statistics()._info
        vcpu_allocation_ratio = 1
        memory_allocation_ratio = 1
        # print data
        return {
            'servers': [data['count'], data['current_workload']],
            'vdisk_capacity': {
                     #'uuid' : 9999999999999,
                     'disk_total': data['local_gb'],
                     'disk_allocated' : data['local_gb_used'],
                     'disk_available' : data['free_disk_gb'],
                     'disk_reserved' : 0},
            'vmem_capacity': {
                       #'uuid' : 8888888888888,
                       'mem_total':  data['memory_mb'],
                       'vmem_total': data['memory_mb'] * memory_allocation_ratio,
                       'vmem_allocated': data['memory_mb_used'],
                       'mem_available': data['free_ram_mb'],
                       'vmem_available': (data['memory_mb'] * memory_allocation_ratio -
                                data['memory_mb_used']),
                       'vmem_reserved': 0},
            'instances': [data['running_vms']],
            'vcpu_capacity': {
                #'uuid': 22222222222,
                'cpu_total': data['vcpus'],
                'vcpu_total': data['vcpus'] * vcpu_allocation_ratio,
                'vcpu_allocated': data['vcpus_used'],
                'cpu_available': data['vcpus'],  # curently nova api returns number of physical cores instead of virtual cores as expected
                'vcpu_available' : (data['vcpus'] * vcpu_allocation_ratio -
                          data['vcpus_used']),
                'vcpu_reserved': 0
            }}

def connect(config):
    try:
        nova_client = Client(
                         version=config['VERSION'],
                         username=config['USERNAME'],
                         api_key=config['PASSWORD'],
                         tenant_id=config['TENANT_ID'],
                         auth_url=config['AUTH_URL'],
                         service_type = config['SERVICE_TYPE']
                         )
    
        nova_client.authenticate()
    except Exception as e:
        print "Connection failed: %s" % e
    return nova_client

def poll_compute_op(config):
    '''
    this function is gating function that all operations according to getting input data resources : vcpus, vmem,vdisk
    should invoke instead of other ones in this file.
    (dict format for using to store in DB or check_capacity() or calculate_capacity())

    :param config: dict format where open-stack config should be defined based on user's system for authentication
    :return:
    '''
    #get credential to access nova api
    nova_client = connect(config)
    #print nova_client.servers.list()

    #getting compute resource data from hypervisor
    dat = polling_op_compute_capacity(nova_client)
    rs_data = dat.get_stats(nova_client)

    return rs_data

def vcpu_op_stats():
    '''
    this function is to grab vcpus resources from hypervisor with output format as below
    {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    :return: {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    '''
    rs_data = poll_compute_op(config)
    vcpus_capacity = rs_data['vcpu_capacity']

    return vcpus_capacity

def vmem_op_stats():
    rs_data = poll_compute_op(config)
    vmem_capactity = rs_data['vmem_capacity']

    return vmem_capactity

def vdisk_op_stats():
    rs_data = poll_compute_op(config)
    vdisk_capactity = rs_data['vdisk_capacity']

    return vdisk_capactity

# Reference function using json request and response
# def load_flavors_list():
#     l = []
#     for project in projects.keys():
#         headers['X-Auth-Token'] = get_token(project)
#         r = requests.get('%s/flavors/detail' % auth_cache[project]['nova_admin_url'], headers=headers)
#         for f in r.json()['flavors']:
#             l.append({
#                 'id': f['id'],
#                 'name': f['name'],
#                 'ram': f['ram'],
#                 'vcpus': f['vcpus'],
#                 'disk': f['disk']
#             })
#     return l

def load_flavors_by_id(flavor_id):
    nova_client = connect(config)
    flavor_list = nova_client.flavors.list(detailed=True)
    flavor_detail = {}
    for flavor in flavor_list:
        print flavor.id
        if int(flavor.id) == int(flavor_id):
            flavor_detail['name'] = flavor.name
            flavor_detail['vcpu'] = flavor.vcpus
            flavor_detail['vmem'] = flavor.ram
            flavor_detail['vdisk'] = flavor.disk
            print flavor_detail
            return flavor_detail

        else:
            print("-"*35)
            print "flavor %s is not existing in VIM (Openstack)" %flavor_id
            print("-"*35)
            return 0
    # print flavor_detail


if __name__ == '__main__':
    print vdisk_op_stats()
    print vcpu_op_stats()
    print vdisk_op_stats()
    # load_flavors_by_id(flavor_id=1)


        
        
         