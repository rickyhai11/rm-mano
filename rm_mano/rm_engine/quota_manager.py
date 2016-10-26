'''

author: rickyhai
dcnlab
nguyendinhhai11@gmail.com
Quota Management and Resource Usage are implemented here and they are used by NFVO API or RM API modules

'''

# Quota Manger class imports
# import collections
# import re
# import time
from Queue import Queue
import threading

# from rm_mano.common import consts
# from rm_mano.common import exceptions
# from rm_mano.common.i18n import _LE
# from rm_mano.common.i18n import _LI
from rm_mano.common import endpoint_cache
from rm_mano.drivers.openstack import sdk

# original imports
import datetime

# from rm_mano.rm_monitor.sh_rm_monitoring import *
from rm_mano.common.utils_rm import *
from rm_mano.global_info import *


#
# Resource usage go here
#######################################################################

# Create resource usage (using with reservation operations probably: create reservation...)
def create_resource_usage_by_name(nfvodb, tenant_id, resource, in_use, reserved, until_refresh):
    '''
    Create resource usage for a specific resource in a given tenant/project
    :param nfvodb: db connection object
    :param project_id:
    :param resource: : resource name
    :param in_use: value of in_use corresponding resource;
    :param reserved: value of reserved corresponding resource;
    :param until_refresh: False- not need to refresh resource usage yet
    True: need to refresh resource usage
    :return: resource usage that is created successfully
    '''
    return nfvodb.create_resource_usage_by_name_for_tenant(tenant_id, resource, in_use, reserved,  until_refresh)

# Update resource usage for specific project/tenant
# TODO(rickyhai) consider if this function is needed at here
def update_resource_usage_by_name(nfvodb, tenant_id, resource, in_use, reserved, until_refresh):
    '''
    update resource usage by name of resource for a given tenant/project
    :param nfvodb:
    :param tenant_id:
    :param resource: name of specific resources
    :param in_use: value (int) for resource in_use
    :param reserved: value (int) for resource reserved
    :param util_refresh: True: resource need to be refreshed and sync, otherwise False: no need to refresh and sync
    :return: result
    '''
    # until_refresh is set False by default
    return nfvodb.update_resource_usage_by_name_for_tenant(tenant_id, resource, in_use, reserved, until_refresh)

def get_resource_usage(nfvodb, tenant_id):
    '''
    Get resource usage for a specific tenant/project
    :param nfvodb:
    :param tenant_id:
    :return: resource usage for that project
    '''
    out_resource_usage = {}
    result, resource_usage = nfvodb.get_resource_usage_for_tenant(tenant_id)
    for usage in resource_usage:
        out_usage = build_output_resource_usage(usage)
        out_resource_usage.update(out_usage)

    return out_resource_usage

def get_resource_usage_by_uuid_name(nfvodb, tenant_id, uuid_name):
    '''
    Get resource usage by uuid or name for a given tenant
    :param nfvodb:
    :param tenant_id:
    :param uuid_name: resource name
    :return: resource usage for tenant/project
    '''
    # get resource usage by name
    result, resource_usage = nfvodb.get_resource_usage_by_uuid_name_for_tenant(tenant_id, uuid_name)

    # convert to proper format to response to api request
    out_usage = build_output_resource_usage(resource_usage)

    return out_usage

# delete resource usage for a given project
def delete_resource_usage(nfvodb, tenant_id):
    result = nfvodb.delete_resource_usage_for_tenant(tenant_id)
    return result

# Unused codes
# resource usage synchronization RM from VIM --> NFVO db
# def sync_resource_usage(nfvodb, tenant_id):
#     '''
#     Sync actual resource usage from vim for recalculate resource usage  that is manually calculated at RM db
#     (resource usage table)
#     :param nfvodb: ddb connection object
#     :param tenant_id:
#     :return: None
#     '''
#     # TODO (ricky) need to take in to account this point: add new records
#     # or update existing records ?? prefer to update option
#
#     actual_resource_usage = sync_resource_usage_for_project(tenant_id)
#     nlog.info('INFO: Starting sync to get actual resource usage from vim')
#     for resource in QUOTA_FIELDS:
#         result, uuid = nfvodb.new_row(table='resource_usage_rm', INSERT=actual_resource_usage[resource],
#                                     add_uuid=True, log=False)
#         if result <= 0:
#             # debug only
#             print "DEBUG: Failed to sync actual resource usage from vim with (resource '%s' and project ID '%s')" \
#                   % (resource, tenant_id)
#             nlog.error("ERROR: Failed to sync resource usage from VIM to DB ")
#     # return result, uuid

#
# Quotas go here
#######################################################################

def create_quotas_project(nfvodb, project_id, quotas):

    result = nfvodb.create_all_quotas_for_tenant(
                tenant_id=project_id,
                quotas=quotas)
    return result

def update_quotas_project(nfvodb, project_id, quotas):

    result = nfvodb.update_all_quotas_for_tenant(
                tenant_id=project_id,
                update_quotas=quotas)
    return result

# Tries to update quota limits for a project, if it fails then
# it creates a new entry in DB for that project
# Input data is a dict
def update_create_quotas_for_tenant(nfvodb, tenant_id, quotas):
    '''
    Tries to update quota limits for a project -input data is dict
    f it fails then it creates a new entry in DB for that project
    :param nfvodb: database global parameter
    :param tenant_id: project_id
    :param quotas: (dict) quotas-hard limits
    :return: (dict) quotas_result with format that store in DB
    '''
    try:
        # validate limits
        validate_quota_limits(payload=quotas)

        # Tries to update quota limit in DB first
        nlog.debug('trying to update quotas limit')
        # cv_quotas is converted to db format from input quotas
        result, cv_quotas = nfvodb.update_all_quotas_for_tenant(
            tenant_id=tenant_id, update_quotas=quotas, ) # TODO (rickyhai) replace with update for a specific resource by name (will resolve current issue)
        # print result
        if result <= 0:
            # If update fails due to project/quota not found
            # then create new records for the quota limits
            print "debug: create new record"
            nlog.debug('update failed due to project/quotas not found')
            result = nfvodb.create_all_quotas_for_tenant(
                tenant_id=tenant_id,
                quotas=quotas) # TODO (rickyhai) replace with update for a specific resource by name (will resolve current issue)
            # TODO (rickyhai) modified
        return result
    except exceptions.InvalidInputError:
            nlog.error('ERROR: %s Invalid input for quota limits', HTTP_Not_Found)

def delete_quotas_for_tenant(nfvodb, project_id):
    '''
    Tries to delete quotas for a given project/tenant in DB
    :param nfvodb:
    :param project_id:
    :return: result - nunmber of deleted rows
    '''

    try:
        # Delete quota limit for a given tenant/project in DB
        result = nfvodb.delete_all_quotas_for_project(
            tenant_id=project_id)
        return result
    except exceptions.ProjectQuotaNotFound:
        nlog.error('ERROR: project/tenant ID %s is not found in DB', project_id)

def get_quotas_for_project(nfvodb, project_id):
    '''
    Get resource usage for a given tennant/project
    :param nfvodb:
    :param tenant_id:
    :return:  tuple of each of resource_usage that return from quota DB for a specified tenant/project
    (each element in tuble is quota data for per resource )
    '''

    try:
        # Get quota limit for a given tenant/project in DB
        result, quotas_db = nfvodb.get_all_quotas_for_tenant(tenant_id=project_id)
        quotas_output = {}
        for quota in quotas_db:
            quotas = build_output_quota_limit(db_quotas=quota)
            quotas_output.update(quotas)
        return quotas_output
    except exceptions.ProjectQuotaNotFound:
        nlog.error('ERROR: project/tenant ID %s is not found in DB', project_id)

def get_specific_quota_by_project(nfvodb, project_id, resource):
    '''
     get specific quota by project (interface that is invoked by nfvo_api/rm_api)
    :param nfvodb:
    :param resource:
    :return: result and quota(dict)
    '''

    result, quota = nfvodb.get_quota_for_project_by_name_uuid(tenant_id=project_id, resource=resource)
    # convert to output format
    quota_out = build_output_quota_limit(quota)
    return result, quota_out

# def get_project_quotas(nfvodb,resources, project_id, usages=True, parent_project_id=None):
#     """Retrieve quotas for a project.
#
#     Given a list of resources, retrieve the quotas for the given
#     project.
#
#     :param resources: A dictionary of the registered resources.
#     :param project_id: The ID of the project to return quotas for.
#     :param defaults: If True, the quota class value (or the
#                      default value, if there is no value from the
#                      quota class) will be reported if there is no
#                      specific value for the resource.
#     :param usages: If True, the current in_use, reserved and allocated
#                    counts will also be returned.
#     :param parent_project_id: The id of the current project's parent,
#                               if any.
#     """
#     # TODO (ricky) need to be implement when nested quota projects is supported
#     return
#
# def _get_quotas(nfvodb, resources, keys, has_sync, project_id=None,
#                 parent_project_id=None):
#     """A helper method which retrieves the quotas for specific resources.
#
#     This specific resource is identified by keys, and which apply to the
#     current context.
#
#     :param nfvodb: db object
#     :param resources: A dictionary of the registered resources.
#     :param keys: A list of the desired quotas to retrieve.
#     :param has_sync: If True, indicates that the resource must
#                      have a sync attribute; if False, indicates
#                      that the resource must NOT have a sync
#                      attribute.
#     :param project_id: Specify the project_id if current context
#                        is admin and admin wants to impact on
#                        common user's tenant.
#     :param parent_project_id: The id of the current project's parent,
#                               if any.
#     """
#     # TODO (ricky) need to be implement when nested quota projects is supported
#     return

def quota_destroy_all_by_project(nfvodb, tenant_id, only_quotas=False):
    # TODO (rickyhai) implement in next stage
    return

def quota_destroy_by_project(*args, **kwargs):
    # TODO (rickyhai) implement in next stage
    """Destroy all limit quotas associated with a project.
    Leaves usage and reservation quotas intact.
    """
    quota_destroy_all_by_project(only_quotas=True, *args, **kwargs)

class VimQuotaManager():
    """Manages tasks related to quota management from NFVO to VIM and otherwise VIM to NFVO
       sync quota from NFVO db to vim (NFVO-->VIM)
       sync actual resource usage from vim to nfvo when quota nearly exceeds and need to re-compute (VIM-->NFVO)
    """

    def __init__(self, nfvodb):
        self.endpoints = endpoint_cache.EndpointCache()
        self.nfvodb = nfvodb

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

    # get quota limits for a project then combined with resource usage to return
    # for "Get total usage for a project" api request
    def _get_playnetmano_rm_project_limit(self, nfvodb, project_id):
        # Returns playnetmano_rm project limit for a project.
        # playnetmano_rm_limits_for_project = collections.defaultdict(dict)
        try:
            # checks if there are any quota limit in DB for a project
            # get project quot limit for a project from db (quota table)
            limits_from_db = get_quotas_for_project(nfvodb, project_id)

            # convert to quota names that is visible at vim, this step is required for quota sync (for a project)
            # sync from nfvo --> vim
            limits_visible_at_vim = build_visible_quota_at_vim(limits_from_db)

            return limits_visible_at_vim  # remove this line when below codes undo
        except exceptions.ProjectQuotaNotFound:
            rmlog.error("ERROR: can't get quota limit from db")

        #     limits_from_db = {}
        # for current_resource in config.playnetmano_rm_global_limit.iteritems():
        #     resource = re.sub('quota_', '', current_resource[0])
            # If resource limit in DB, then use it or else use limit
            # from conf file
            # TODO (ricky) implement config file with default quota values for rm_mano then undo
            # if resource in limits_from_db:
            #     playnetmano_rm_limits_for_project[resource] = limits_from_db[resource]
            # else:
            #     playnetmano_rm_limits_for_project[resource] = current_resource[1]
        # return playnetmano_rm_limits_for_project

    # arrange quotas by service (nova, cinder, neutron) to update or delete quota by service --> to vim
    def _arrange_quotas_by_service_name(self, region_new_limit):
        # Returns a dict of resources with limits arranged by service name
        resource_with_service = collections.defaultdict(dict)
        resource_with_service['nova'] = collections.defaultdict(dict)
        resource_with_service['cinder'] = collections.defaultdict(dict)
        resource_with_service['neutron'] = collections.defaultdict(dict)
        for limit in region_new_limit:
            if limit in consts.NOVA_QUOTA_FIELDS_AT_VIM:
                resource_with_service['nova'].update(
                    {limit: region_new_limit[limit]})
            elif limit in consts.CINDER_QUOTA_FIELDS_AT_VIM:
                resource_with_service['cinder'].update(
                    {limit: region_new_limit[limit]})
            elif limit in consts.NEUTRON_QUOTA_FIELDS_AT_VIM:
                resource_with_service['neutron'].update(
                    {limit: region_new_limit[limit]})
        return resource_with_service

    def update_quota_limits(self, project_id, region_new_limit,
                            current_region):
        # Updates quota limit for a project with new calculated limit
        os_client = sdk.OpenStackDriver(current_region)
        os_client.write_quota_limits(project_id, region_new_limit)

    # sync quotas for a given project  from nfvo to vim
    def quota_sync_for_project(self, nfvodb, project_id):
        # Support multi regions and multi vims:
        # Sync quota limits for the project according to below formula
        # Global remaining limit = Playnetmano_rm global limit - Summation of usages
        #                          in all the regions
        # New quota limit = Global remaining limit + usage in that region

        # Notice: this formula will work effectively with multi regions/vims and also work well with only one region
        # with only one region, quota is kept as user set previously in  request or db
        # example: user set quota= {'vcpus': 10} --> after sync (go through above formula),
        # quota for that region is still {'vcpus' : 10}

        rmlog.info("INFO: Quota sync Called for Project: %s", project_id)
        regions_thread_list = []
        # Retrieve regions for the project
        region_lists = sdk.OpenStackDriver().get_all_regions_for_project(
            project_id)
        regions_usage_dict = self.get_tenant_quota_usage_per_region(project_id)
        if not regions_usage_dict:
            # Skip syncing for the project if not able to read regions usage
            rmlog.error("ERROR: Error reading regions usage for the Project: '%s'. "
                      "Aborting, continue with next project.", project_id)
            return
        total_project_usages = dict(self.get_summation(regions_usage_dict))
        playnetmano_rm_global_limit = self._get_playnetmano_rm_project_limit(nfvodb, project_id)
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

    def get_total_usage_for_tenant(self, nfvodb, project_id):
        # Returns total quota usage for a tenant
        rmlog.info("INFO: Get total usage called for project: %s", project_id)
        try:
            total_usage = dict(self.get_summation(
                self.get_tenant_quota_usage_per_region(project_id)))
            playnetmano_rm_global_limit = self._get_playnetmano_rm_project_limit(nfvodb, project_id)
            # Get unused quotas
            unused_quota = set(playnetmano_rm_global_limit).difference(set(total_usage.keys()))
            # Create a dict with value as '0' for unused quotas
            unused_quota = dict((quota_name, 0) for quota_name in unused_quota)
            total_usage.update(unused_quota)
            return {'limits': playnetmano_rm_global_limit,
                    'usage': total_usage}
        except exceptions.NotFound:
            raise

    def sync_total_usage_for_tenant_vim_2_db(self, nfvodb, project_id):
        # update total actual resource usage for a project to nfvo db (synchronize between nfvo and vim)
        rmlog.info("INFO: resource usage is out of sync, sync total actual resource usage from vim to nfvo db "
                   "for project: %s", project_id)
        try:
            total_actual_usage = self.get_total_usage_for_tenant(nfvodb, project_id)
            usage_nfvo_db = build_visible_resources_at_nfvo(total_actual_usage['usage'])
            for resource, value in usage_nfvo_db.items():
                result = allocated_resource_update(nfvodb, project_id, resource, value, action='SYNC')
                if not result[0]:
                    rmlog.error("ERROR: Failure when updating synced usage from vim to nfvo db")

        except exceptions.SyncFailure:
            raise


# implement quota check, quota calculation
########################################################


def available_resource_check_for_project(nfvodb, values, project_id=None):
    # check availability for resource(s) in a given project
    '''
        checking availability for resource(s) in a given project based on assigned quota
        :param nfvodb: db object
        :param values: (dict) keys/values of resource(s) that are used for check
        :param project_id:  specific a given project
        :return:
        '''
    # get applicable quota for a project
    quotas = get_quotas_for_project(nfvodb, project_id)

    # get applicable resource usage for a project
    rs_usage = get_resource_usage(nfvodb, project_id)

    # set flog for quota enforcement
    flag = False

    # Get unused quotas
    # un_used_resource = set(quotas.keys()).difference(set(values.keys()))
    # print un_used_resource

    # Check for deltas that would go negative
    unders = [r for r, val in values.items()
              if val < 0 and val + rs_usage[r]['in_use'] < 0]
    if unders:
        rmlog.error("Change will make usage less than 0 for the following resources: %s", unders)

    # check the quotas
    # We're only concerned about positive increments.
    # If a project has gone over quota, we want them to
    # be able to reduce their usage without any problems.
    overs = [r for r, val in values.items()
             if quotas[r] >= 0 and val >= 0 and
             quotas[r] <= val + rs_usage[r]['in_use'] + rs_usage[r]['reserved']]

    if overs:
        flag = False
        rmlog.error("ERROR: quotas exceed for the resources '%s'", overs)
        print exceptions.OverQuota(overs=sorted(overs), quotas=quotas, usages={})
        return flag
    else:
        flag = True
        rmlog.info("INFO: Resources: '%s' is sufficient", overs)
        return flag


def available_check_specific_resource_for_project(nfvodb, resource, project_id=None):
    # TODO (rickyhai) need to implement
    return


def limit_check(nfvodb, values, project_id=None):
    """Check simple quota limits.

    For limits--those quotas for which there is no usage
    synchronization function--this method checks that a set of
    proposed values are permitted by the limit restriction.

    This method will raise a QuotaResourceUnknown exception if a
    given resource is unknown or if it is not a simple limit
    resource.

    If any of the proposed values is over the defined quota, an
    OverQuota exception will be raised with the sorted list of the
    resources which are too high.  Otherwise, the method returns
    nothing.

    :param values: A dictionary of the resources/values to check against the
                   quota.
    :param project_id: Specify the project_id if current context
                       is admin and admin wants to impact on
                       common user's tenant.
    """

    # Ensure no value is less than zero
    unders = [key for key, val in values.items() if val < 0]
    if unders:
        nlog.error("ERROR: sh_quota_manager.limit_check() invalid input data: '%s'", unders)
        raise exceptions.InvalidInputError()

    # If project_id is None, then we use the project_id in context
    # if project_id is None:
    #     project_id = context.project_id

    # Get the applicable quotas
    quotas = get_quotas_for_project(nfvodb, project_id)

    # Check the quotas and construct a list of the resources that
    # would be put over limit by the desired values
    overs = [key for key, val in values.items()
             if quotas[key] >= 0 and quotas[key] < val]
    if overs:
        nlog.error("ERROR: quotas exceed for the resources '%s'", overs)
        raise exceptions.OverQuota(overs=sorted(overs), quotas=quotas, usages={})


def allocated_resource_update(nfvodb, project_id, resource, allocated, action):
    '''
    when resource allocation change is made, then we need to update 'in_use' value for a specific resource
    in resource usage table against action = (ADD, UPDATE, DELETE)
    if action == ADD or UPDATE --> increase in_use
    if action == DELETE --> decrease in_use
    :param nfvodb: db object
    :param tenant_id:
    :param resource: name
    :param in_use: value
    :param action: (ADD, UPDATE, DELETE) --> to decide whether in_use (allocated) resource is increased or decreased
    :return:
    '''

    return nfvodb.in_use_record_update(project_id=project_id, resource=resource, in_use=allocated, action=action)


def reserved_resource_update(nfvodb, project_id, resource, reserved, action):
    '''
    when resource reservation change is made, then we need to update 'reserved' value for a specific resource
    in resource usage table against action = (ADD, UPDATE, DELETE)
    if action == ADD or UPDATE --> increase reserved
    if action == DELETE --> decrease reserved
    :param nfvodb: db object
    :param tenant_id:
    :param resource: name
    :param reserved: value
    :param action: (ADD, UPDATE, DELETE) --> to decide whether reserved resource is increased or decreased
    :return:
    '''

    return nfvodb.reserved_record_update(project_id=project_id, resource=resource, reserved=reserved, action=action)


def get_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id):

    # get flavour info from flavour_info table
    result, content = nfvodb.get_table_by_uuid_name("flavour_info", vnfd_flavor_id, error_item_text=None, allow_serveral=False)
    if result <= 0:
        nlog.error("Error : Can't get flavour_info table")
        return False
    else:
        resources = collections.defaultdict(dict)
        resources['vcpus'] = content['numVirCpu']
        resources['vmemmory'] = content['vMemory']
        resources['gigabytes'] = content['storageSize']
        return resources


def loading_reserved_quota_by_flavour_id(nfvodb, vnfd_flavor_id, number_vnfs):
    # get number of vnfs in a reservation dict
    # return a dict of reserved quota  after calculating with below formula:
    # reserved = number of vnfs * flavor_detail
    '''
        get reserved resource for instantiating reservation
        :param vnfd_flavor_id: flavour id
        :param number_vnfs: number of vnfs in a reservation
        :return: reserved resources (dict)
        '''

    # get flavour info from flavour_info table
    resources = get_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id)
    if number_vnfs > 0:
        for key, val in resources.items():
            val *= int(number_vnfs)
            reserved[key] = val
        nlog.info("SUCCESS: Loading reserved based on flavour id '%s',  reserved = %s", vnfd_flavor_id, reserved)
        return reserved
    else:
        nlog.error("ERROR: number of vnfs is not defined yet :[number of vnfs = '%s']", number_vnfs)
        return False


def loading_allocated_quota_by_flavour_id(nfvodb, vnfd_flavor_id):
    '''
    get allocated resources that required when NFVO send resource allocation message to VIM
    :param nfvodb:
    :param vnfd_flavor_id: flavour id which is used when NVFNO send resource allocation message to VIM
    :return: allocated dict: resource allocation
    '''

    # get flavour info from flavour_info table
    allocated = get_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id)

    return allocated


def get_vnfdUsingCnt_for_project(nfvodb, vnfd_id, action):
    '''
    Get number of current using vnfs in a project
    :param vnfd_id:
    :param action: ADD --> vnfd_using_cnt ++
    DELETE --> vnfd_using_cnt --
    :return:
    '''
    # get vnfd_using_cnt from vnfd_using_info table
    result, vnfd_using_cnt = nfvodb.update_vnf_using_info_table(vnfd_id, action)
    return result, vnfd_using_cnt

#
#
# wish-list in the future- IGNORE THESE CODES BELOW PLS !
#########################################################
#


class DbQuotaDriver(object):
    """Driver to perform check to enforcement of quotas.

    Also allows to obtain quota information.
    The default driver utilizes the local database.
    """

    def commit(self, reservations, project_id=None):
        """Commit reservations.

        :param context: The request context, for access checks.
        :param reservations: A list of the reservation UUIDs, as
                             returned by the reserve() method.
        :param project_id: Specify the project_id if current context
                           is admin and admin wants to impact on
                           common user's tenant.
        """
        # If project_id is None, then we use the project_id in context
        if project_id is None:
            project_id = context.project_id

        db_api.reservation_commit(context, reservations, project_id=project_id)

    def rollback(self, reservations, project_id=None):
        """Roll back reservations.

        :param context: The request context, for access checks.
        :param reservations: A list of the reservation UUIDs, as
                             returned by the reserve() method.
        :param project_id: Specify the project_id if current context
                           is admin and admin wants to impact on
                           common user's tenant.
        """
        # If project_id is None, then we use the project_id in context
        if project_id is None:
            project_id = context.project_id

        db_api.reservation_rollback(context, reservations,
                                    project_id=project_id)

    def expire(self, context):
        """Expire reservations.

        Explores all currently existing reservations and rolls back
        any that have expired.

        :param context: The request context, for access checks.
        """

        db_api.reservation_expire(context)




def reserve(nfvodb, resources, deltas, expire=None,
            project_id=None):
    # reserve() will invoke reservation_create() to reserve resources and make reservations
    """Check quotas and reserve resources.

    For counting quotas--those quotas for which there is a usage
    synchronization function--this method checks quotas against
    current usage and the desired deltas.

    This method will raise a QuotaResourceUnknown exception if a
    given resource is unknown or if it does not have a usage
    synchronization function.

    If any of the proposed values is over the defined quota, an
    OverQuota exception will be raised with the sorted list of the
    resources which are too high.  Otherwise, the method returns a
    list of reservation UUIDs which were created.

    :param resources: A dictionary of the registered resources.
    :param deltas: A dictionary of the proposed delta changes.
    :param expire: An optional parameter specifying an expiration
                   time for the reservations.  If it is a simple
                   number, it is interpreted as a number of
                   seconds and added to the current time; if it is
                   a datetime.timedelta object, it will also be
                   added to the current time.  A datetime.datetime
                   object will be interpreted as the absolute
                   expiration time.  If None is specified, the
                   default expiration time set by
                   --default-reservation-expire will be used (this
                   value will be treated as a number of seconds).
    :param project_id: Specify the project_id if current context
                       is admin and admin wants to impact on
                       common user's tenant.
    """

    # Set up the reservation expiration
    if expire is None:
        expire = CONF.quota.reservation_expire
    if isinstance(expire, six.integer_types):
        expire = datetime.timedelta(seconds=expire)
    if isinstance(expire, datetime.timedelta):
        expire = timeutils.utcnow() + expire
    if not isinstance(expire, datetime.datetime):
        raise t_exceptions.InvalidReservationExpiration(expire=expire)

    # If project_id is None, then we use the project_id in context
    if project_id is None:
        project_id = context.project_id

    # Get the applicable quotas.
    # NOTE: We're not worried about races at this point.
    #            Yes, the admin may be in the process of reducing
    #            quotas, but that's a pretty rare thing.

    # NOTE(ricky): in rm-mano, no embedded sync function here,
    # so set has_sync=False.
    quotas = self._get_quotas(context, resources, deltas.keys(),
                              has_sync=False, project_id=project_id)

    # NOTE: Most of the work here has to be done in the DB
    #            API, because we have to do it in a transaction,
    #            which means access to the session.  Since the
    #            session isn't available outside the DBAPI, we
    #            have to do the work there.
    return db_api.reservation_create(context, resources, quotas, deltas,
                                     expire, CONF.quota.until_refresh,
                                     CONF.quota.max_age,
                                     project_id=project_id)


class AllQuotaEngine(QuotaEngine):
    """Represent the set of all quotas."""

    @property
    def resources(self):
        """Fetches all possible quota resources."""

        result = {}

        # Global quotas.
        # Set sync_func to None for no sync function in Tricircle
        reservable_argses = [

            ('instances', None, 'quota_instances'),
            ('cores', None, 'quota_cores'),
            ('ram', None, 'quota_ram'),
            ('security_groups', None, 'quota_security_groups'),
            ('floating_ips', None, 'quota_floating_ips'),
            ('fixed_ips', None, 'quota_fixed_ips'),
            ('server_groups', None, 'quota_server_groups'),


            ('volumes', None, 'quota_volumes'),
            ('per_volume_gigabytes', None, 'per_volume_size_limit'),
            ('snapshots', None, 'quota_snapshots'),
            ('gigabytes', None, 'quota_gigabytes'),
            ('backups', None, 'quota_backups'),
            ('backup_gigabytes', None, 'quota_backup_gigabytes'),
            ('consistencygroups', None, 'quota_consistencygroups')
        ]

        absolute_argses = [
            ('metadata_items', 'quota_metadata_items'),
            ('injected_files', 'quota_injected_files'),
            ('injected_file_content_bytes',
             'quota_injected_file_content_bytes'),
            ('injected_file_path_bytes',
             'quota_injected_file_path_length'),
        ]

        # TODO(joehuang), for countable, the count should be the
        # value in the db but not 0 here
        countable_argses = [
            ('security_group_rules', None, 'quota_security_group_rules'),
            ('key_pairs', None, 'quota_key_pairs'),
            ('server_group_members', None, 'quota_server_group_members'),
        ]

        for args in reservable_argses:
            resource = ReservableResource(*args)
            result[resource.name] = resource

        for args in absolute_argses:
            resource = AbsoluteResource(*args)
            result[resource.name] = resource

        for args in countable_argses:
            resource = CountableResource(*args)
            result[resource.name] = resource

        return result

    def register_resource(self, resource):
        raise NotImplementedError(_("Cannot register resource"))

    def register_resources(self, resources):
        raise NotImplementedError(_("Cannot register resources"))

# get all defined resources
QUOTAS = AllQuotaEngine()


# get number of vnfs in a reservation dict
# return a dict of reserved quota  after calculating with below formula:
# reserved = number of vnfs * flavor_detail
# def quota_reserved_by_flavor_vnfcount(content):
#     '''
#     get reserved resource for instantiating reservation
#     reservation content should be provided that included needed info such as:flavor_id, number_vnfs...
#     :param content: (dict) dict-reservation content (like in db form)
#     :return: reserved resources (dict)
#     '''
#
#     # get flavour id and number of vnfs from rsv content
#     flavor_id = content['flavor_id']
#     number_vnfs = int(content['number_vnfs'])
#
#     # flavor_details = {'vcpus': 1, 'memory': 512, 'gigabytes': 1}
#     # loading based on flavour id
#     flavor_details = load_flavors_from_vim(flavor_id)
#
#     # initiate reserved dict
#     reserved = collections.defaultdict(dict)
#     if number_vnfs > 0:
#         for key, val in flavor_details.items():
#             val *= int(number_vnfs)
#             reserved[key] = val
#         nlog.info("SUCCESS: Loading reserved based on flavour id '%s', reserved = %s", flavor_id, reserved)
#         return reserved
#     else:
#         nlog.error("ERROR: number of vnfs is not defined yet :[number of vnfs = '%s']", number_vnfs)


def go_main():
    return 0

if __name__ == "__main__":

    # VimQuotaManager class test
    region_new_limit = {'nova':{"cores": 80,"ram": 102400, "metadata_items": 800,"key_pairs": 800},'cinder':{"volumes": 80,"snapshots": 80, "gigabytes": 800,"backups": 800},'neutron':{"network":80,"port": 80,"router": 80}}
    quota_manager = VimQuotaManager()
    quota_manager.update_quota_limits(project_id='f4211c8eee044bfb9dea2050fef2ace5', region_new_limit=region_new_limit, current_region='RegionOne')
