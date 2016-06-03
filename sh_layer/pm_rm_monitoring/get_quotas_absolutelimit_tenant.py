from novaclient.client import Client as NovaClient
from novaclient import exceptions

import collectd
import traceback

import base

class NovaPlugin(base.Base):

    def __init__(self):
        base.Base.__init__(self)
        self.prefix = 'openstack-nova'

    def get_stats(self):
        """Retrieves stats from nova"""
        keystone = self.get_keystone()

        tenant_list = keystone.tenants.list()

        data = { self.prefix: { 'cluster': { 'config': {} }, } }
        client = NovaClient('2', self.username, self.password, self.tenant, self.auth_url)
        for tenant in tenant_list:
            # FIX: nasty but works for now (tenant.id not being taken below :()
            client.tenant_id = tenant.id
            data[self.prefix]["tenant-%s" % tenant.name] = { 'limits': {}, 'quotas': {} }
            data_tenant = data[self.prefix]["tenant-%s" % tenant.name]

            # Get absolute limits for tenant
            limits = client.limits.get(tenant_id=tenant.id).absolute
            for limit in limits:
                if 'ram' in limit.name.lower():
                    limit.value = limit.value * 1024.0 * 1024.0
                data_tenant['limits'][limit.name] = limit.value

            # Quotas for tenant
            quotas = client.quotas.get(tenant.id)
            for item in ('cores', 'fixed_ips', 'floating_ips', 'instances',
                'key_pairs', 'ram', 'security_groups'):
                if item == 'ram':
                    setattr(quotas, item, getattr(quotas, item) * 1024 * 1024)
                data_tenant['quotas'][item] = getattr(quotas, item)

        # Cluster allocation / reserved values
        for item in ('AllocationRatioCores', 'AllocationRatioRam',
                'ReservedNodeCores', 'ReservedNodeRamMB',
                'ReservedCores', 'ReservedRamMB'):
            data[self.prefix]['cluster']['config'][item] = getattr(self, item)

        # Hypervisor information
        hypervisors = client.hypervisors.list()
        for hypervisor in hypervisors:
            name = "hypervisor-%s" % hypervisor.hypervisor_hostname
            data[self.prefix][name] = {}
            for item in ('current_workload', 'free_disk_gb', 'free_ram_mb',
                    'hypervisor_version', 'memory_mb', 'memory_mb_used',
                    'running_vms', 'vcpus', 'vcpus_used'):
                data[self.prefix][name][item] = getattr(hypervisor, item)
            data[self.prefix][name]['memory_mb_overcommit'] = \
                data[self.prefix][name]['memory_mb'] * data[self.prefix]['cluster']['config']['AllocationRatioRam']
            data[self.prefix][name]['memory_mb_overcommit_withreserve'] = \
                data[self.prefix][name]['memory_mb_overcommit'] - data[self.prefix]['cluster']['config']['ReservedNodeRamMB']
            data[self.prefix][name]['vcpus_overcommit'] = \
                data[self.prefix][name]['vcpus'] * data[self.prefix]['cluster']['config']['AllocationRatioCores']
            data[self.prefix][name]['vcpus_overcommit_withreserve'] = \
                data[self.prefix][name]['vcpus_overcommit'] - data[self.prefix]['cluster']['config']['ReservedNodeCores']

        return data

try:
    plugin = NovaPlugin()
except Exception as exc:
    collectd.error("openstack-nova: failed to initialize nova plugin :: %s :: %s"
            % (exc, traceback.format_exc()))

def configure_callback(conf):
    """Received configuration information"""
    plugin.config_callback(conf)

def read_callback():
    """Callback triggerred by collectd on read"""
    plugin.read_callback()

collectd.register_config(configure_callback)
collectd.register_read(read_callback, plugin.interval)



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