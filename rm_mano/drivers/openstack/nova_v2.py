
import collections

from oslo_log import log

from rm_mano.common import consts
from rm_mano.common import exceptions
from rm_mano.drivers import base

from novaclient import client
# from keystoneauth1 import session

LOG = log.getLogger(__name__)
API_VERSION = '2.1'

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

class NovaClient(base.DriverBase):
    '''Nova V2.1 driver.'''
    def __init__(self, region, disabled_quotas, session):
        try:
            self.nova_client = client.Client(API_VERSION,
                                             session=session,
                                             region_name=region)
            self.enabled_quotas = list(set(consts.NOVA_QUOTA_FIELDS) -
                                       set(disabled_quotas))
            self.no_neutron = True if 'floatingips' in self.enabled_quotas \
                or 'fixedips' in self.enabled_quotas else False
        except exceptions.ServiceUnavailable:
            raise

    def get_resource_usages(self, project_id):
        """Collects resource usages for a given project

        :params: project_id
        :return: dictionary of corresponding resources with its usage
        """
        try:
            # The API call does not give usage for keypair, fixed ips &
            # metadata items. Have raised a bug for that.
            limits = self.nova_client.limits.get(
                tenant_id=project_id).to_dict()
            print limits
            resource_usage = collections.defaultdict(dict)
            resource_usage['ram'] = limits['absolute']['totalRAMUsed']
            resource_usage['cores'] = limits['absolute']['totalCoresUsed']
            resource_usage['instances'] = \
                limits['absolute']['totalInstancesUsed']
            # If neutron is not enabled, calculate below resources from nova
            if self.no_neutron:
                resource_usage['security_groups'] = \
                    limits['absolute']['totalSecurityGroupsUsed']
                resource_usage['floating_ips'] = \
                    limits['absolute']['totalFloatingIpsUsed']
            # For time being, keypair is calculated in below manner.
            resource_usage['key_pairs'] = \
                len(self.nova_client.keypairs.list())
            return resource_usage
        except exceptions.InternalError:
            raise

    def update_quota_limits(self, project_id, **new_quota):
        """Updates quota limits for a given project

        :params: project_id, dictionary with the quota limits to update
        :return: Nothing
        """
        try:
            if not self.no_neutron:
                if 'floating_ips' in new_quota:
                    del new_quota['floating_ips']
                if 'fixed_ips' in new_quota:
                    del new_quota['fixed_ips']
                if 'security_groups' in new_quota:
                    del new_quota['security_groups']
            return self.nova_client.quotas.update(project_id,
                                                  **new_quota)
        except exceptions.InternalError:
            raise

    def delete_quota_limits(self, project_id):
        """Delete/Reset quota limits for a given project

        :params: project_id
        :return: Nothing
        """
        try:
            return self.nova_client.quotas.delete(project_id)
        except exceptions.InternalError:
            raise

    # integrate sh_monitor function

    # --
    # get_flavor_count()
    # Returns a flavor:count for a given tenant
    #

    def get_flavor_count(self, project_id):

        instanceList = self.nova_client.servers.list(search_opts={'all_tenants': 1, 'tenant_id': project_id})
        cnt_inst_flavor_distribution = {}
        cnt_inst_flavor_distribution['custom'] = 0

        global flavorListDefault
        for fname in flavorListDefault:
            cnt_inst_flavor_distribution[fname] = 0

        for inst in instanceList:
            t_inst_flav = inst.flavor['id']
            flavor = self.nova_client.flavors.get(t_inst_flav)

            if cnt_inst_flavor_distribution.has_key(flavor.name):
                cnt_inst_flavor_distribution[flavor.name] = cnt_inst_flavor_distribution[flavor.name] + 1
            else:
                cnt_inst_flavor_distribution['custom'] = cnt_inst_flavor_distribution['custom'] + 1

        return cnt_inst_flavor_distribution

