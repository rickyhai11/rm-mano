'''
Created on 2016. 2. 12.

@author: Ricky Hai
'''
from neutronclient.neutron import client as neutron
from datetime import datetime
from time import mktime
from pprint import pformat
import re
config = {
    'VERSION' : '2.0',
    'AUTH_URL': "http://223.194.33.74:5000/v2.0/",
    'USERNAME': "admin",
    'PASSWORD' : "zz",
    'TENANT_ID' : "bd68c380ec274c1ea7187478f7acea0a",
    'TENANT_NAME' : 'admin',
    'public_network' : 'public'
    }

class op_networks_capacity():
    def __init__(self, neutron_client, public_network=None):
        self.neutron_client = neutron_client
        self.last_stats = None
        self.connection_done = None
        self.public_network = public_network

    def check_connection(self, force=False):
        if not self.connection_done or force:
            try:
                # force a connection to the server
                self.connection_done = self.neutron_client.list_ports()
            except Exception as e:
                print"Cannot connect to neutron: %s\n" % e

    def get_stats(self):
        global config
        stats = {}
        self.last_stats = int(mktime(datetime.now().timetuple()))
        kwargs = {'retrieve_all': True, 'fields': 'id'}
        stats['networks'] = [ len(self.neutron_client.list_networks(**kwargs)['networks']) ]
        stats['ports'] = [ len(self.neutron_client.list_ports(**kwargs)["ports"]) ]
        stats['routers'] = [ len(self.neutron_client.list_routers(**kwargs)["routers"]) ]
        stats['floatingips_usage'] = [ len(self.neutron_client.list_floatingips(**kwargs)['floatingips']) ]
        stats['floatingips_available'] = [self._estimate_total_ip() - int(stats['floatingips_usage'][0])]
        if self.public_network:
            total_ip = self._estimate_total_ip()
            stats['floatingips_usage'].append(total_ip)
        if any(e['alias'] == 'lbaas' for e in self.neutron_client.list_extensions()['extensions']):
            stats['lbaas'] = [ len(self.neutron_client.list_vips(**kwargs)["vips"]) ]
            stats['lbaas'].append(len(self.neutron_client.list_pools(**kwargs)["pools"]))
        snat = 0
        for router in self.neutron_client.list_routers()['routers']:
            if router['external_gateway_info'] and router['external_gateway_info']['enable_snat']:
                snat += 1
        stats['snat_external_gateway'] = [ snat ]

        return stats

    def _estimate_total_ip(self):
        total_ip = 0
        subnet_mask = re.compile('[^/]+/(\d{1,2})')
        subnets_from_public_network = [] 
        try:
            subnets_from_public_network = self.neutron_client.list_networks(
                name=self.public_network)['networks'][0]['subnets'] # obtain subnets ID [u'771e1289-7b9c-4d38-8150-5a1170034fe5', u'b7ad90cf-d459-43bb-9f49-359dcaf347f0']
        except Exception as e:
            print "Cannot get subnets associated with %s network: %s" % \
                        (self.public_network, e)
            return None

        for public_subnet_id in subnets_from_public_network:
            net_info = self.neutron_client.list_subnets(
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
        print "total number of floating IP: %d " % total_ip
        return total_ip
    
    
def connect(config):
    # Neutron-client tries to re-authenticate if it gets an unauthorized error
    # https://github.com/openstack/python-neutronclient/blob/752423483304572f00dacfcffce35a268fa3e5d4/neutronclient/client.py#L180
    neutron_client = neutron.Client('2.0',
                                    username=config['USERNAME'],
                                    tenant_id=config['TENANT_ID'],
                                    password=config['PASSWORD'],
                                    auth_url=config['AUTH_URL'])
    kwargs = {'retrieve_all': True, 'fields': 'id'}
    conf = {'neutron_client': neutron_client}
    if config['public_network'] and config['public_network'] != 'none':
        conf['public_network'] = config['public_network']
    config['util'] = op_networks_capacity(**conf)
    config['util'].check_connection(True)
    return neutron_client
    
    
    
if __name__ == '__main__': 
    neutron_client  = connect(config)
    dat = op_networks_capacity(neutron_client,public_network= 'public')
    print dat.get_stats()
    kwargs = {'retrieve_all': True, 'fields': 'id'}
    print neutron_client.list_networks()
    print neutron_client.list_ports()
    print neutron_client.list_routers()
    print neutron_client.list_floatingips()
    print neutron_client.list_extensions()
    #print neutron_client.list_vips()
    print neutron_client.list_pools()
    print neutron_client.list_routers()
    print neutron_client.list_subnets()
