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
    def get_stats(self):
        self.nova_client.authenticate()
        data = nova_client.hypervisor_stats.statistics()._info
        vcpu_allocation_ratio =16
        memory_allocation_ratio =1.5
        
        return {
            'servers': [data['count'], data['current_workload']],
            'disk': {'total': data['local_gb'], 
                    'used' : data['local_gb_used'],
                     'free' : data['free_disk_gb'], 
                     'available_least' : data['disk_available_least']},
            'memory': {'total': data['memory_mb'] * memory_allocation_ratio,
                       'phys_total':  data['memory_mb'],
                       'used': data['memory_mb_used'],
                       'phys_free': data['free_ram_mb'],
                       'free': (data['memory_mb'] * memory_allocation_ratio -
                                data['memory_mb_used'])},
            'instances': [data['running_vms']],
            'vcpus': {
                'total': data['vcpus'] * vcpu_allocation_ratio,
                'phys_total': data['vcpus'],
                'used': data['vcpus_used'],
                'phys_free': data['vcpus'],  # curently nova api returns number of physical cores instead of virtual cores as expected
                'free' : (data['vcpus'] * vcpu_allocation_ratio -
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

 
if __name__ == '__main__':
    nova_client = connect(config)
    print nova_client.servers.list()
    print nova_client.flavors.list()
    dat = op_compute_capacity(nova_client)
    print dat
    print dat.get_stats()
    
        
        
        
         