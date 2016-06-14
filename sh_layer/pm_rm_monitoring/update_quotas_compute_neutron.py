#!/usr/bin/python

import logging
import os
from neutronclient.neutron import client as neutronc
from novaclient import client as novac
from optparse import OptionParser
import inspect
#logging.basicConfig(level=logging.INFO)

def parse_args():
        parser = OptionParser()
        parser.add_option("-p", "--project", dest="project_id",
                  help="project ID which needs quota modifications")
        (options, args) = parser.parse_args()
        return options, args

def init_openstack():
        global neutron, nova
        neutron = neutronc.Client('2.0', auth_url=os.environ['OS_AUTH_URL'],
                                tenant_name=os.environ['OS_TENANT_NAME'],
                                username=os.environ['OS_USERNAME'],
                                password=os.environ['OS_PASSWORD'],
                                region_name=os.environ['OS_REGION_NAME'])
        nova = novac.Client('2', auth_url=os.environ['OS_AUTH_URL'],
                                tenant_id=os.environ['OS_TENANT_ID'],
                                username=os.environ['OS_USERNAME'],
                                api_key=os.environ['OS_PASSWORD'],
                                region_name=os.environ['OS_REGION_NAME'])
        neutron.format = 'json'
        nova.format='json'
        return

def get_quota_info(project_id):
        '''gets quota info from the user'''
        # need to find a way to validate the tenant id...

        #print project_id
        nova_qs = nova.quotas.get(project_id)
        #print nova_qs
        neutron_qs = neutron.show_quota(project_id)
        #print neutron_qs
        #neutron_qs = neutron.get_quotas_tenant(project_id)

        instances = raw_input('Enter number of VMs (instances) ['+str(nova_qs.instances)+']:')
        if not instances:
                instances = nova_qs.instances
        else:
                instances = int(instances)
        if instances < 2 or instances > 8:
                print 'Instances outside valid range (2-8)'
                exit(1)
        vcpus = raw_input('Enter total number of CPUs (cores) ['+str(nova_qs.cores)+']:')
        if not vcpus:
                vcpus = nova_qs.cores
        else:
                vcpus = int(vcpus)
        if vcpus < 2 or vcpus > 10:
                print 'vCPUs outside valid range (2-10)'
                exit(1)
        ram = raw_input('Enter total RAM (in MB) ['+str(nova_qs.ram)+']:')
        if not ram:
                ram = nova_qs.ram
        else:
                ram = int(ram)
        if ram < 4096 or ram > 10240:
                print 'RAM outside valid range (4096-10240)'
                exit(1)
        print 'Skipping disk configuration for now...'
        #harddisk = raw_input('Enter total harddisk (in GB):')
        #if hardisk < 50 or harddisk > 100:
        #       print 'Hardidsk outside valid range (50-100)'
        #       exit(1)
        public_ips = raw_input('Enter total public IPs [(nova),'+str(nova_qs.floating_ips)+', (neutron) '+str(neutron_qs['quota']['floatingip'])+']:')
        if not public_ips:
                public_ips = neutron_qs['quota']['floatingip']
        else:
                public_ips = int(public_ips)
        if public_ips < 0 or public_ips > 4:
                print 'Public IPs outside valid range (1-4)'
                exit(1)
        ret_val = {'instances': instances, 'cores': vcpus, 'ram': ram, 'public_ips': public_ips }
        return ret_val

def update_quotas(project_id, q_info):
        print
        print 'Updating quotas for user '+project_id
        nova_qs = nova.quotas.get(project_id)
        neutron_qs = neutron.show_quota(project_id)
        #print 'nova - instances(), cores (), floatingips()'
        nova_qs = nova.quotas.update(project_id, instances=q_info['instances'], cores=q_info['cores'], floating_ips=q_info['public_ips'])
        #print 'neutron - floatingips()'
        neutron_qs = neutron.update_quota(project_id, {'quota': {'floatingip': q_info['public_ips'] }})

        print
        print 'Quotas updated...'
        print
        nova_qs = nova.quotas.get(project_id).to_dict()
        print 'Nova quota for project '+project_id
        for k,v in nova_qs.iteritems():
                print '   '+str(k)+': '+str(v)
        neutron_qs = neutron.show_quota(project_id)
        print
        print 'Neutron quota for project '+project_id
        for k,v in neutron_qs['quota'].iteritems():
                print '   '+str(k)+': '+str(v)

def get_project_id():
        tenant_id = raw_input( 'Enter project id:')
        #no validation right now...
        return tenant_id

def main():
        '''main function'''
        opts, args = parse_args()
        if opts.project_id is None:
                project_id = get_project_id()
        else:
                project_id = opts.project_id
        print "Updating quotas for project_id "+project_id
        init_openstack()
        q_info = get_quota_info(project_id)
        update_quotas(project_id, q_info)

main()