'''
Created on 2016. 2. 1.

@author: Ricky Hai
'''
from novaclient.client import Client
from datetime import datetime
from time import mktime

global config 
config = {
    'VERSION' : '2',
    'AUTH_URL': "http://223.194.33.74:5000/v2.0/",
    'USERNAME': "admin",
    'PASSWORD' : "zz",
    'TENANT_ID' : "bd68c380ec274c1ea7187478f7acea0a",
    'TENANT_NAME' : "admin",
    'SERVICE_TYPE' : 'compute'}

class op_compute_capacity():
    
    def __init__(self, nova_client):
        self.nova_client = nova_client
        self.last_stats = None
    def get_stats(self,nova_client):
        self.nova_client.authenticate()
        data = nova_client.hypervisor_stats.statistics()._info
        vcpu_allocation_ratio =16
        memory_allocation_ratio =1.5
        print data
        return {
            'servers': [data['count'], data['current_workload']],
            'vdisk_capacity': {
                     'disk_total': data['local_gb'],
                     'disk_used' : data['local_gb_used'],
                     'disk_available' : data['free_disk_gb']},
            'vmem_capacity': {
                       'mem_total':  data['memory_mb'],
                       'vmem_total': data['memory_mb'] * memory_allocation_ratio,
                       'vmem_used': data['memory_mb_used'],
                       'mem_available': data['free_ram_mb'],
                       'vmem_available': (data['memory_mb'] * memory_allocation_ratio -
                                data['memory_mb_used'])},
            'instances': [data['running_vms']],
            'vcpu_capacity': {
                'cpu_total': data['vcpus'],
                'vcpu_total': data['vcpus'] * vcpu_allocation_ratio,
                'vcpu_used': data['vcpus_used'],
                'cpu_available': data['vcpus'],  # curently nova api returns number of physical cores instead of virtual cores as expected
                'vcpu_available' : (data['vcpus'] * vcpu_allocation_ratio -
                          data['vcpus_used']) 
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
    #print nova_client.flavors.list()

    #getting compute resource data from hypervisor
    dat = op_compute_capacity(nova_client)
    rs_data= dat.get_stats(nova_client)

    return rs_data

def vcpu_op_stats():
    '''
    this function is to grab vcpus resources from hypervisor with output format as below
    {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    :return: {'vcpu_total': 32, 'vcpu_available': 32, 'cpu_total': 2, 'vcpu_used': 0, 'cpu_available': 2}
    '''
    rs_data=poll_compute_op(config)
    vcpus_capacity= rs_data['vcpu_capacity']

    return vcpus_capacity

def vmem_op_stats():
    rs_data=poll_compute_op(config)
    vmem_capactity= rs_data['vmem_capacity']

    return vmem_capactity

def vdisk_op_stats():
    rs_data=poll_compute_op(config)
    vdisk_capactity= rs_data['vdisk_capacity']

    return vdisk_capactity
 
if __name__ == '__main__':
    print vcpu_op_stats()


        
        
         