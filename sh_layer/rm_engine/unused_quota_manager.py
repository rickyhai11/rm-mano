import collections
from Queue import Queue
import re
import threading
import time

from oslo_config import cfg
from oslo_log import log as logging

from sh_layer.common import consts
from sh_layer.common import exceptions
from sh_layer.common.i18n import _LI
from sh_layer.common import manager
from sh_layer.common import utils_rm
from sh_layer.drivers.openstack import sdk

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class QuotaManager(manager.Manager):
    """Manages tasks related to quota management"""

    def read_quota_usage(self, project_id, region, usage_queue):
        # Writes usage dict to the Queue in the following format
        # {'region_name': (<nova_usages>, <neutron_usages>, <cinder_usages>)}
        LOG.info(_LI("Reading quota usage for %(project_id)s in %(region)s"),
                 {'project_id': project_id,
                  'region': region}
                 )
        os_client = sdk.OpenStackDriver(region)
        region_usage = os_client.get_resource_usages(project_id)
        total_region_usage = collections.defaultdict(dict)
        # region_usage[0], region_usage[1], region_usage[3] are
        # nova, neutron & cinder usages respectively
        total_region_usage.update(region_usage[0])
        total_region_usage.update(region_usage[1])
        total_region_usage.update(region_usage[2])
        usage_queue.put({region: total_region_usage})

    def get_summation(self, regions_dict):
        # Adds resources usages from different regions
        single_region = {}
        resultant_dict = collections.Counter()
        for current_region in regions_dict:
            single_region[current_region] = collections.Counter(
                regions_dict[current_region])
            resultant_dict += single_region[current_region]
        return resultant_dict

    def _get_playnetmano_rm_project_limit(self, project_id):
        # Returns playnetmano_rm project limit for a project.
        playnetmano_rm_limits_for_project = collections.defaultdict(dict)
        try:
            # checks if there are any quota limit in DB for a project
            limits_from_db = db_api.quota_get_all_by_project(self.context,
                                                             project_id)
        except exceptions.ProjectQuotaNotFound:
            limits_from_db = {}
        for current_resource in CONF.playnetmano_rm_global_limit.iteritems():
            resource = re.sub('quota_', '', current_resource[0])
            # If resource limit in DB, then use it or else use limit
            # from conf file
            if resource in limits_from_db:
                playnetmano_rm_limits_for_project[resource] = limits_from_db[
                    resource]
            else:
                playnetmano_rm_limits_for_project[resource] = current_resource[1]
        return playnetmano_rm_limits_for_project

    def _arrange_quotas_by_service_name(self, region_new_limit):
        # Returns a dict of resources with limits arranged by service name
        resource_with_service = collections.defaultdict(dict)
        resource_with_service['nova'] = collections.defaultdict(dict)
        resource_with_service['cinder'] = collections.defaultdict(dict)
        resource_with_service['neutron'] = collections.defaultdict(dict)
        for limit in region_new_limit:
            if limit in consts.NOVA_QUOTA_FIELDS:
                resource_with_service['nova'].update(
                    {limit: region_new_limit[limit]})
            elif limit in consts.CINDER_QUOTA_FIELDS:
                resource_with_service['cinder'].update(
                    {limit: region_new_limit[limit]})
            elif limit in consts.NEUTRON_QUOTA_FIELDS:
                resource_with_service['neutron'].update(
                    {limit: region_new_limit[limit]})
        return resource_with_service

    def update_quota_limits(self, project_id, region_new_limit,
                            current_region):
        # Updates quota limit for a project with new calculated limit
        os_client = sdk.OpenStackDriver(current_region)
        os_client.write_quota_limits(project_id, region_new_limit)


    def get_tenant_quota_usage_per_region(self, project_id):
        # Return quota usage dict with keys as region name & values as usages.
        # Calculates the usage from each region concurrently using threads.

        # Retrieve regions for the project
        region_lists = sdk.OpenStackDriver().get_all_regions_for_project(
            project_id)
        usage_queue = Queue()
        regions_usage_dict = collections.defaultdict(dict)
        regions_thread_list = []
        for current_region in region_lists:
            thread = threading.Thread(target=self.read_quota_usage,
                                      args=(project_id, current_region,
                                            usage_queue))
            regions_thread_list.append(thread)
            thread.start()
        # Wait for all the threads to finish reading usages
        for current_thread in regions_thread_list:
            current_thread.join()
        # Check If all the regions usages are read
        if len(region_lists) == usage_queue.qsize():
            for i in range(usage_queue.qsize()):
                # Read Queue
                current_region_data = usage_queue.get()
                regions_usage_dict.update(current_region_data)
        return regions_usage_dict

    def get_total_usage_for_tenant(self, project_id):
        # Returns total quota usage for a tenant
        LOG.info(_LI("Get total usage called for project: %s"),
                 project_id)
        try:
            total_usage = dict(self.get_summation(
                self.get_tenant_quota_usage_per_region(project_id)))
            playnetmano_rm_global_limit = self._get_playnetmano_rm_project_limit(
                project_id)
            # Get unused quotas
            unused_quota = set(
                playnetmano_rm_global_limit).difference(set(total_usage.keys()))
            # Create a dict with value as '0' for unused quotas
            unused_quota = dict((quota_name, 0) for quota_name in unused_quota)
            total_usage.update(unused_quota)
            return {'limits': playnetmano_rm_global_limit,
                    'usage': total_usage}
        except exceptions.NotFound:
            raise


if __name__ == "__main__":
    quota_mana= QuotaManager()
    data = quota_mana.get_total_usage_for_tenant('admin')
    print data

