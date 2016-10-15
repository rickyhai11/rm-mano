import collections
from Queue import Queue
import re
import threading
import time

from sh_layer.common import consts
from sh_layer.common import endpoint_cache
from sh_layer.common import exceptions
from sh_layer.common.i18n import _LE
from sh_layer.common.i18n import _LI
from sh_layer.drivers.openstack import sdk


class QuotaManager():
    """Manages tasks related to quota management"""

    def __init__(self, *args, **kwargs):
        self.endpoints = endpoint_cache.EndpointCache()

    def read_quota_usage(self, project_id, region, usage_queue):
        # Writes usage dict to the Queue in the following format
        # {'region_name': (<nova_usages>, <neutron_usages>, <cinder_usages>)}

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

    def quota_sync_for_project(self, project_id):
        # Sync quota limits for the project according to below formula
        # Global remaining limit = Playnetmano_rm global limit - Summation of usages
        #                          in all the regions
        # New quota limit = Global remaining limit + usage in that region
        LOG.info(_LI("Quota sync Called for Project: %s"),
                 project_id)
        regions_thread_list = []
        # Retrieve regions for the project
        region_lists = sdk.OpenStackDriver().get_all_regions_for_project(
            project_id)
        regions_usage_dict = self.get_tenant_quota_usage_per_region(project_id)
        if not regions_usage_dict:
            # Skip syncing for the project if not able to read regions usage
            LOG.error(_LE("Error reading regions usage for the Project: '%s'. "
                      "Aborting, continue with next project."), project_id)
            return
        total_project_usages = dict(self.get_summation(regions_usage_dict))
        playnetmano_rm_global_limit = self._get_playnetmano_rm_project_limit(project_id)
        global_remaining_limit = collections.Counter(
            playnetmano_rm_global_limit) - collections.Counter(total_project_usages)

        for current_region in region_lists:
            region_new_limit = dict(
                global_remaining_limit + collections.Counter(
                    regions_usage_dict[current_region]))
            region_new_limit = self._arrange_quotas_by_service_name(
                region_new_limit)
            thread = threading.Thread(target=self.update_quota_limits,
                                      args=(project_id, region_new_limit,
                                            current_region,))
            regions_thread_list.append(thread)
            thread.start()

        # Wait for all the threads to update quota
        for current_thread in regions_thread_list:
            current_thread.join()

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
    def get_region_for_project(self, project_id):
        # Retrieve regions for the project
        region_lists = sdk.OpenStackDriver().get_all_regions_for_project(project_id)
        print region_lists

if __name__ == "__main__":
    region_new_limit = {'nova':{"cores": 80,"ram": 102400, "metadata_items": 800,"key_pairs": 800},'cinder':{"volumes": 80,"snapshots": 80, "gigabytes": 800,"backups": 800},'neutron':{"network":80,"port": 80,"router": 80}}
    quota_manager = QuotaManager()
    quota_manager.update_quota_limits(project_id='f4211c8eee044bfb9dea2050fef2ace5', region_new_limit=region_new_limit, current_region='RegionOne')
    # quota_manager.get_region_for_project('f4211c8eee044bfb9dea2050fef2ace5')