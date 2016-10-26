
'''
OpenStack Driver
'''
import collections

from oslo_log import log
from oslo_utils import timeutils

from rm_mano.common import consts
from rm_mano.common import endpoint_cache
from rm_mano.common import exceptions
from rm_mano.common.i18n import _
from rm_mano.common.i18n import _LE
from rm_mano.common.i18n import _LI

from rm_mano.drivers.openstack.cinder_v2 import CinderClient
from rm_mano.drivers.openstack.keystone_v3 import KeystoneClient
from rm_mano.drivers.openstack.neutron_v2 import NeutronClient
from rm_mano.drivers.openstack.nova_v2 import NovaClient



LOG = log.getLogger(__name__)


class OpenStackDriver(object):

    os_clients_dict = collections.defaultdict(dict)

    def __init__(self, region_name=None):
        # Check if objects are cached and try to use those
        self.region_name = region_name
        if 'keystone' in OpenStackDriver.os_clients_dict and \
                self._is_token_valid():
            self.keystone_client = OpenStackDriver.os_clients_dict['keystone']
        else:
            self.keystone_client = KeystoneClient()
            OpenStackDriver.os_clients_dict['keystone'] = self.keystone_client
        self.disabled_quotas = self._get_disabled_quotas(region_name)
        if region_name in OpenStackDriver.os_clients_dict and \
                self._is_token_valid():
            LOG.info(_LI('Using cached OS client objects'))
            self.nova_client = OpenStackDriver.os_clients_dict[
                region_name]['nova']
            self.cinder_client = OpenStackDriver.os_clients_dict[
                region_name]['cinder']
            self.neutron_client = OpenStackDriver.os_clients_dict[
                region_name]['neutron']
        else:
            # Create new objects and cache them
            LOG.info(_("Creating fresh OS Clients objects"))
            self.neutron_client = NeutronClient(region_name,
                                                self.disabled_quotas,
                                                self.keystone_client.session)
            self.nova_client = NovaClient(region_name,
                                          self.disabled_quotas,
                                          self.keystone_client.session)
            self.cinder_client = CinderClient(region_name,
                                              self.disabled_quotas,
                                              self.keystone_client.session)
            OpenStackDriver.os_clients_dict[
                region_name] = collections.defaultdict(dict)
            OpenStackDriver.os_clients_dict[region_name][
                'nova'] = self.nova_client
            OpenStackDriver.os_clients_dict[region_name][
                'cinder'] = self.cinder_client
            OpenStackDriver.os_clients_dict[region_name][
                'neutron'] = self.neutron_client

    def get_enabled_projects(self):
        try:
            return self.keystone_client.get_enabled_projects()
        except Exception as exception:
            LOG.error(_LE('Error Occurred: %s'), exception.message)

    def get_resource_usages(self, project_id):
        try:
            nova_usages = self.nova_client.get_resource_usages(project_id)
            neutron_usages = self.neutron_client.get_resource_usages(
                project_id)
            cinder_usages = self.cinder_client.get_resource_usages(project_id)
            return nova_usages, neutron_usages, cinder_usages
        except (exceptions.ConnectionRefused, exceptions.NotAuthorized,
                exceptions.TimeOut):
            # Delete the cached objects for that region
            del OpenStackDriver.os_clients_dict[self.region_name]
        except Exception as exception:
            LOG.error(_LE('Error Occurred: %s'), exception.message)

    def write_quota_limits(self, project_id, limits_to_write):
        try:
            self.nova_client.update_quota_limits(project_id,
                                                 **limits_to_write['nova'])
            self.cinder_client.update_quota_limits(project_id,
                                                   **limits_to_write['cinder'])
            self.neutron_client.update_quota_limits(project_id,
                                                    limits_to_write['neutron'])
        except (exceptions.ConnectionRefused, exceptions.NotAuthorized,
                exceptions.TimeOut):
            # Delete the cached objects for that region
            del OpenStackDriver.os_clients_dict[self.region_name]
        except Exception as exception:
            LOG.error(_LE('Error Occurred: %s'), exception.message)

    def delete_quota_limits(self, project_id):
        try:
            self.nova_client.delete_quota_limits(project_id)
            self.neutron_client.delete_quota_limits(project_id)
            self.cinder_client.delete_quota_limits(project_id)
        except (exceptions.ConnectionRefused, exceptions.NotAuthorized,
                exceptions.TimeOut):
            # Delete the cached objects for that region
            del OpenStackDriver.os_clients_dict[self.region_name]
        except Exception as exception:
            LOG.error(_LE('Error Occurred: %s'), exception.message)

    def _get_disabled_quotas(self, region):
        disabled_quotas = []
        if not self.keystone_client.is_service_enabled('volume') and \
                not self.keystone_client.is_service_enabled('volumev2'):
            disabled_quotas.extend(consts.CINDER_QUOTA_FIELDS)
        # Neutron
        if not self.keystone_client.is_service_enabled('network'):
            disabled_quotas.extend(consts.NEUTRON_QUOTA_FIELDS)
        else:
            disabled_quotas.extend(['floating_ips', 'fixed_ips'])
            disabled_quotas.extend(['security_groups',
                                    'security_group_rules'])
        return disabled_quotas

    def get_all_regions_for_project(self, project_id):
        try:
            # Retrieve regions based on endpoint filter for the project.
            region_lists = self._get_filtered_regions(project_id)
            if not region_lists:
                # If endpoint filter is not used for the project, then
                # return all regions
                region_lists = endpoint_cache.EndpointCache().get_all_regions()
            return region_lists
        except Exception as exception:
            LOG.error(_LE('Error Occurred: %s'), exception.message)
            raise

    def _get_filtered_regions(self, project_id):
        return self.keystone_client.get_filtered_region(project_id)

    def _is_token_valid(self):
        keystone = self.os_clients_dict['keystone'].keystone_client
        token = keystone.tokens.validate(keystone.session.get_token())
        expiry_time = timeutils.normalize_time(timeutils.parse_isotime(
            token['expires_at']))
        current_time = timeutils.utcnow()
        if expiry_time > current_time:
            return True
        else:
            LOG.info(_("The cached keystone token has expired"))
            # Reset the cached dictionary
            OpenStackDriver.os_clients_dict = collections.defaultdict(dict)
            return False

    # integrate sh_monitor functions
    ###################################

    def get_flavors_usage(self, project_id):
        return self.nova_client.get_flavor_count(project_id)

    def sync_flavor_usage_all_projects(self):
        project_id_list = self.keystone_client.get_enabled_projects()

        flavors_all_projects = collections.defaultdict(dict)
        for project_id in project_id_list:
            t_flavor_details = self.nova_client.get_flavor_count(project_id)

            flavors_all_projects[project_id] = {
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

        return flavors_all_projects

    def load_flavors_from_vim(self, flavor_id):
        '''
        loading flavor details directly from vim (openstack)
        :param flavor_id:
        :return: a dict - all details about required resources for that flavor
        '''
        return self.nova_client.load_flavors_from_vim(flavor_id)


if __name__ == "__main__":
    nova_client = OpenStackDriver()
    # fl_cnt= nova_client.get_flavors_usage('f4211c8eee044bfb9dea2050fef2ace5')
    all = nova_client.sync_flavor_usage_all_projects()
    print all