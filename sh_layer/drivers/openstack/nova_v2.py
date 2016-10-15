
import collections

from oslo_log import log

from sh_layer.common import consts
from sh_layer.common import exceptions
from sh_layer.drivers import base

from novaclient import client
from keystoneauth1 import session

LOG = log.getLogger(__name__)
API_VERSION = '2.1'


class NovaClient(base.DriverBase):
    # '''Nova V2.1 driver.'''
    # def __init__(self, region, disabled_quotas, session):
    #     try:
    #         self.nova_client = client.Client(
    #                      version=config['VERSION'],
    #                      username=config['USERNAME'],
    #                      api_key=config['PASSWORD'],
    #                      tenant_id=config['TENANT_ID'],
    #                      auth_url=config['AUTH_URL'],
    #                      service_type = config['SERVICE_TYPE']
    #                      )

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



