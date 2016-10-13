'''
author: rickyhai
dcnlab
nguyendinhhai11@gmail.com
Implemetation capacity management

Quota Management and Resource Usage are implemented here and they are used by NFVO API or RM API modules
'''

import datetime

from sh_layer.rm_monitor.sh_rm_monitoring import *
from sh_layer.common.utils_rm import *
from sh_layer.global_info import *

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
    return nfvodb.create_resource_usage_by_name_for_tenant(tenant_id, resource, in_use, reserved,  until_refresh=False)

# Update resource usage for specific project/tenant
# TODO(rickyhai) consider if this function is needed at here
def update_resource_usage_by_name(nfvodb, tenant_id, resource, in_use, reserved, until_refresh=False):
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
    return nfvodb.update_resource_usage_by_name_for_tenant(tenant_id, resource, in_use, reserved, until_refresh=False)

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

# resource synchronization RM (NFVO)-VIM
def sync_resource_usage(nfvodb, tenant_id):
    '''
    Sync actual resource usage from vim for recalculate resource usage  that is manually calculated at RM db
    (resource usage table)
    :param nfvodb: ddb connection object
    :param tenant_id:
    :return: None
    '''
    # TODO (ricky) need to take in to account this point: add new records or update existing records ?? prefer to update option

    actual_resource_usage = sync_resource_usage_for_tenant(tenant_id)
    nlog.info('INFO: Starting sync to get actual resource usage from vim')
    for resource in QUOTA_FIELDS:
        result, uuid = nfvodb.new_row(table='resource_usage_rm', INSERT=actual_resource_usage[resource], add_uuid=True,
                                      log=False)
        if result <= 0:
            # debug only
            print "DEBUG: Failed to sync actual resource usage from vim with (resource '%s' and project ID '%s')" \
                  % (resource, tenant_id)
            nlog.error("ERROR: Failed to sync resource usage from VIM to DB ")
    # return result, uuid

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
        result, resource_usage = nfvodb.get_all_quotas_for_tenant(tenant_id=project_id)
        quotas_output = {}
        for usage in resource_usage:
            quotas_out = build_output_quota_limit(db_quotas=usage)
            quotas_output.update(quotas_out)
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


def quota_destroy_all_by_project(nfvodb, tenant_id, only_quotas=False):
    # TODO (rickyhai) implement in next stage
    return

def quota_destroy_by_project(*args, **kwargs):
    # TODO (rickyhai) implement in next stage
    """Destroy all limit quotas associated with a project.
    Leaves usage and reservation quotas intact.
    """
    quota_destroy_all_by_project(only_quotas=True, *args, **kwargs)

# implement quota check, quota calculation,
########################################################

def increase_resource_usage(nfvodb, project_id, values):
    # get  current resource usage ()
    #
    # calculate base on values
    #
    # update to db
    # consider which case for reservation ---> update reserved OR allocated --> in_use
    # by checking values if 'in_use' or 'reserved' is present

    return
def decrease_resource_usage(nfvodb, project_id, values):

    return

# check availability for resource(s) in a given project
def available_resource_check_for_project(nfvodb, values, project_id=None):
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
    un_used_resource = set(quotas.keys()).difference(set(values.keys()))
    print un_used_resource

    # Check for deltas that would go negative
    unders = [r for r, delta in values.items()
              if delta < 0 and delta + rs_usage[r]['in_use'] < 0]

    # check the quotas
    # We're only concerned about positive increments.
    # If a project has gone over quota, we want them to
    # be able to reduce their usage without any problems.
    overs = [r for r, delta in values.items()
             if quotas[r] >= 0 and delta >= 0 and
             quotas[r] <= delta + rs_usage[r]['in_use'] + rs_usage[r]['reserved']]

    if overs:
        flag = False
        nlog.error("ERROR: quotas exceed for the resources '%s'")
        raise exceptions.OverQuota(overs=sorted(overs), quotas=quotas, usages={})
        return flag
    else:
        flag = True
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

def get_project_quotas(nfvodb,resources, project_id, usages=True, parent_project_id=None):
    """Retrieve quotas for a project.

    Given a list of resources, retrieve the quotas for the given
    project.

    :param resources: A dictionary of the registered resources.
    :param project_id: The ID of the project to return quotas for.
    :param defaults: If True, the quota class value (or the
                     default value, if there is no value from the
                     quota class) will be reported if there is no
                     specific value for the resource.
    :param usages: If True, the current in_use, reserved and allocated
                   counts will also be returned.
    :param parent_project_id: The id of the current project's parent,
                              if any.
    """
    # TODO (ricky) need to be implement when nested quota projects is supported
    return

def _get_quotas(nfvodb, resources, keys, has_sync, project_id=None,
                parent_project_id=None):
    """A helper method which retrieves the quotas for specific resources.

    This specific resource is identified by keys, and which apply to the
    current context.

    :param nfvodb: db object
    :param resources: A dictionary of the registered resources.
    :param keys: A list of the desired quotas to retrieve.
    :param has_sync: If True, indicates that the resource must
                     have a sync attribute; if False, indicates
                     that the resource must NOT have a sync
                     attribute.
    :param project_id: Specify the project_id if current context
                       is admin and admin wants to impact on
                       common user's tenant.
    :param parent_project_id: The id of the current project's parent,
                              if any.
    """
    # TODO (ricky) need to be implement when nested quota projects is supported
    return


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




def quota_reserve(nfvodb, resources, quotas, deltas, expire,
                  until_refresh, max_age, project_id=None):
    elevated = context.elevated()
    with context.session.begin():
        if project_id is None:
            project_id = context.project_id

        # Get the current usages
        usages = _get_quota_usages(context, context.session, project_id)

        # Handle usage refresh
        refresh = False
        work = set(deltas.keys())
        while work:
            resource = work.pop()

            # Do we need to refresh the usage?
            if resource not in usages:
                usages[resource] = re_quota_usage_create(elevated,
                                                       project_id,
                                                       resource,
                                                       0, 0,
                                                       until_refresh or None,
                                                       session=context.session)
                refresh = True
            elif usages[resource].in_use < 0:
                # Negative in_use count indicates a desync, so try to
                # heal from that...
                refresh = True
            elif usages[resource].until_refresh is not None:
                usages[resource].until_refresh -= 1
                if usages[resource].until_refresh <= 0:
                    refresh = True
            elif max_age and usages[resource].updated_at is not None and (
                (usages[resource].updated_at -
                    timeutils.utcnow()).seconds >= max_age):
                refresh = True

            if refresh:
                # no actual usage refresh here

                # refresh from the bottom pod
                usages[resource].until_refresh = until_refresh or None

                # Because more than one resource may be refreshed
                # by the call to the sync routine, and we don't
                # want to double-sync, we make sure all refreshed
                # resources are dropped from the work set.
                work.discard(resource)

                # NOTE: We make the assumption that the sync
                #            routine actually refreshes the
                #            resources that it is the sync routine
                #            for.  We don't check, because this is
                #            a best-effort mechanism.

        # Check for deltas that would go negative
        unders = [r for r, delta in deltas.items()
                  if delta < 0 and delta + usages[r].in_use < 0]

        # Now, let's check the quotas
        # NOTE: We're only concerned about positive increments.
        #            If a project has gone over quota, we want them to
        #            be able to reduce their usage without any
        #            problems.
        overs = [r for r, delta in deltas.items()
                 if quotas[r] >= 0 and delta >= 0 and
                 quotas[r] < delta + usages[r].in_use + usages[r].reserved]

        # NOTE: The quota check needs to be in the transaction,
        #            but the transaction doesn't fail just because
        #            we're over quota, so the OverQuota raise is
        #            outside the transaction.  If we did the raise
        #            here, our usage updates would be discarded, but
        #            they're not invalidated by being over-quota.

        # Create the reservations
        if not overs:
            reservations = []
            for resource, delta in deltas.items():
                reservation = _reservation_create(elevated,
                                                  str(uuid.uuid4()),
                                                  usages[resource],
                                                  project_id,
                                                  resource, delta, expire,
                                                  session=context.session)
                reservations.append(reservation.uuid)

                # Also update the reserved quantity
                # NOTE: Again, we are only concerned here about
                #            positive increments.  Here, though, we're
                #            worried about the following scenario:
                #
                #            1) User initiates resize down.
                #            2) User allocates a new instance.
                #            3) Resize down fails or is reverted.
                #            4) User is now over quota.
                #
                #            To prevent this, we only update the
                #            reserved value if the delta is positive.
                if delta > 0:
                    usages[resource].reserved += delta

    if unders:
        LOG.warning(_LW("Change will make usage less than 0 for the following "
                        "resources: %s"), unders)
    if overs:
        usages = {k: dict(in_use=v['in_use'], reserved=v['reserved'])
                  for k, v in usages.items()}
        raise exceptions.OverQuota(overs=sorted(overs), quotas=quotas,
                                   usages=usages)

    return reservations


def reserve(nfvodb, resources, deltas, expire=None,
            project_id=None):
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
    return db_api.quota_reserve(context, resources, quotas, deltas,
                                expire, CONF.quota.until_refresh,
                                CONF.quota.max_age,
                                project_id=project_id)

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

def load_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id):

    # get flavour info from flavour_info table
    result, content = nfvodb.get_table_by_uuid_name("flavour_info", vnfd_flavor_id, error_item_text=None, allow_serveral=False)
    if result <= 0:
        nlog.error("Error : Can't get flavour_info table")
        return False
    else:
        resources = collections.defaultdict(dict)
        resources['vcpus'] = content['numVirCpu']
        resources['memmory'] = content['vMemory']
        resources['gigabytes'] = content['storageSize']
        return resources

# get number of vnfs in a reservation dict
# return a dict of reserved quota  after calculating with below formula:
# reserved = number of vnfs * flavor_detail
def quota_reserved(nfvodb, vnfd_flavor_id, number_vnfs):
    '''
    get reserved resource for instantiating reservation
    :param vnfd_flavor_id: flavour id
    :param number_vnfs: number of vnfs in a reservation
    :return: reserved resources (dict)
    '''

    # get flavour info from flavour_info table
    resources = load_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id)
    if number_vnfs > 0:
        for key, val in resources.items():
            val *= int(number_vnfs)
            reserved[key] = val
        nlog.info("SUCCESS: Loading reserved based on flavour id '%s',  reserved = %s", vnfd_flavor_id, reserved)
        return reserved
    else:
        nlog.error("ERROR: number of vnfs is not defined yet :[number of vnfs = '%s']", number_vnfs)
        return False

def quota_allocated(nfvodb, vnfd_flavor_id):
    '''
    get allocated resources that required when NVFNO send resource allocation message to VIM
    :param nfvodb:
    :param vnfd_flavor_id: flavour id which is used when NVFNO send resource allocation message to VIM
    :return: allocated dict: resource allocation
    '''

    # get flavour info from flavour_info table
    allocated = load_flavour_from_flavour_info_table(nfvodb, vnfd_flavor_id )

    return allocated

def go_main():
    return 0

if __name__ == "__main__":

    data = {'reservation_id': '22222',
            'label': 'test4',
            'host_id': "12212817268DJKHSAJD",
            'host_name': 'hai_compute',
            'user_id': 'ffbc3c72aa9f44769f3430093c59c457',
            'user_name': 'admin',
            'tenant_id': '4a766494021447c7905b81adae050a97',
            'tenant_name': 'demo',
            'start_time': '2016-05-23 18:04:00',
            'end_time': '2016-05-23 18:09:00',
            'flavor_id': 1,
            'image_id': 'bf9d2214-4032-4b0a-8588-0fb73fc7d57c',
            'network_id': 'f61491df-3ad8-4ac4-9974-6b6ea27bf5f0',
            'number_vnfs': 2,
            'ns_id': 'ffbc3c72aa9f44769f3430093c59c457',
            'status': 'ACTIVE',
            'summary': 'reservation testing'
            }

    flavor_details = {'vcpus': 1, 'memory': 512, 'gigabytes': 1}
    # test get reserved quota from flavour
    reserved = quota_reserved_by_flavor_vnfcount(data)
    print reserved


    #
    # try:
    #     nfvodb = resource_db()
    #     if nfvodb.connect(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
    #         print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
    #         exit(-1)
    #     # get_quotas_for_project(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5')
    #     # update ={'in_use': 3}
    #     # update_resource_usage_by_name(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5', resource='vnfs', actual_usage= 3)
    #
    # except (KeyboardInterrupt, SystemExit):
    #     print 'Exiting Resource Management'
