'''
author: rickyhai
dcnlab
nguyendinhhai11@gmail.com
Implemetation capacity management
'''

import datetime

from sh_layer.rm_monitor.sh_rm_monitoring import *
from sh_layer.rm_db.utils_db import utils_db
from utils import todo
from sh_layer.global_info import *


def resource_limit_check_for_tenant(resource, tenant_id):
    return

def quota_reserve(context, resources, quotas, deltas, expire,
                  until_refresh, max_age, project_id=None):
    return

def quota_usage_get(context, project_id, resource):
    # TODO (rm api interface)
    return _get_quota_usages_by_resource(context, project_id, resource)

def _get_quota_usages_by_resource(context, project_id, resource):
    # TODO(rickyhai), add user_id as part of the filter
    return


def quota_usage_get_all_by_project(context, project_id):
    # TODO (rm api interface)
    return

def _quota_usage_create(tenant_id, user_id):
    return

def __update_quota_usage_for_tenant(tenant_id, user_id):
    return

def quota_destroy_all_by_project(context, project_id, only_quotas=False):
    # TODO (rm api interface)
    # TODO (rickyhai) admin context require
    """Destroy all quotas associated with a project.

    This includes limit quotas, usage quotas and reservation quotas.
    Optionally can only remove limit quotas and leave other types as they are.

    :param context: The request context, for access checks.
    :param project_id: The ID of the project being deleted.
    :param only_quotas: Only delete limit quotas, leave other types intact.
    """
def quota_destroy_by_project(*args, **kwargs):
    # TODO (rm api interface)
    """Destroy all limit quotas associated with a project.

    Leaves usage and reservation quotas intact.
    """
    quota_destroy_all_by_project(only_quotas=True, *args, **kwargs)


def quota_resource_usage_sync_for_tenant(nfvodb, tenant_id):
    all_usage = get_resource_usage_tenant(tenant_id)
    nlog.debug(all_usage)
    for resource_usage in QUOTA_FIELDS:
        result, uuid = nfvodb.new_row(table='resource_usage_rm', INSERT=all_usage[resource_usage], add_uuid=True, log=False)
        if result <= 0:
            nlog.error("ERROR: added/updated resource usage from VIM to DB ")
    return result, uuid













# store  actual resource usage to DB
########################################################

def add_resource_2_db(mydb, table, data):
    result = mydb.add_row_rs(table, data)
    if result > 0:
        print "Added data to %s table successfully"
    return result

def __init_resource_usage_compute_all_users_2_db(mydb, table, rsv):
    # polling compute openstack service for getting updated compute resource usage.
    # when compute resource value of user is not initiated (empty with that user_id and tenant_id in DB)
    # Above specification is to identify exactly which user from particular tenant, compute resources would be initiated into DB table
    data_list = get_resource_usage_compute_for_all_users_in_all_tenants()
    for data in data_list:
        if data['user_id'] == rsv['user_id'] and data['tenant_id'] == rsv['tenant_id'] and data['user_name'] != 'admin': # need to exclude admin user as admin-ids are same in all tenants
            print " initating resource usage-compute for user-id: %s and tenant-id: %s in %s DB table" % (data['user_id'], data['tenant_id'], table)
            result, added_uuid = mydb.add_row_rs(table, data)
            print type(data)
            return data, result, added_uuid # at the first meet matched user-id, loop will be broken. save memory than put return out of loop

def init_resource_usage_compute_all_users_2_db(mydb, table, rsv):
    init_data, result, added_uuid = __init_resource_usage_compute_all_users_2_db(mydb, table, rsv)
    print type(init_data)
    if result > 0 and init_data is not None:
        print "Initiated dat for %s table successfully"
        return init_data, result, added_uuid
    elif result == 0 and init_data is None: # if we see this error TypeError: 'NoneType' object is not iterable, that means code jumps to here
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print " FAILED to initiate data into DB table %s because user-id=%s and tenant-id=%s from RESERVATION request CAN NOT be found in DB table %s " \
              "--> init_data is empty" % (table,rsv['user_id'], rsv['tenant_id'], table)
        print "==========================================================================================================================="
        print "WARNING !!! user-id: %s and tenant-id: %s from RESERVATION request are NOT EXISTING in DB and VIM OR user-id: %s is admin user." \
              " Please sign up !!! Thanks." % (rsv['user_id'], rsv['tenant_id'], rsv['user_id'])
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return result


def check_user_compute_capacity(mydb, rsv):
    list_users_util_cap_tables = ['users_util_compute_rm'] # ,'users_util_network_rm', 'users_util_storage_rm']  # TODO need to add 'users_util_storage_rm' table into this list after finishing implementation
    # flag to identify result of resource check: if true : successfully, otherwise failed
    retrval = True
    reserved_rs = calculate_reserved_compute_rs_by_flavor(rsv)
    print reserved_rs
    for table in list_users_util_cap_tables:
        current_rs_capacity, uuid = get_current_available_resource(mydb=mydb, table_name=table, rsv=rsv)
        print " print out current_rs_capacity dict"
        print current_rs_capacity

        # if table == 'users_util_compute_rm':
        if table == 'users_util_compute_rm' and int(reserved_rs['reserved_vcpus']) >= int(current_rs_capacity['available_vcpus']):
            print "Request is rejected due to lack of VCPUs. Resources request from user-id : %s in tenant-id: %s for VCPUs is not satisfied. Debug-DB table %s" % (rsv['user_id'], rsv['tenant_id'], table)
            retrval = False
            break

        elif table == 'users_util_compute_rm' and int(reserved_rs['reserved_vmem']) >= int(current_rs_capacity['available_vmem']):
            print "Request is rejected due to lack of VMEM. Resources request from user-id : %s in tenant-id: %s for VMEM is not satisfied. Debug-DB table %s" % (rsv['user_id'], rsv['tenant_id'], table)
            retrval = False
            break

        elif table == 'users_util_compute_rm' and int(rsv['number_vnfs']) >= int(current_rs_capacity['available_vnfs']):
            print "Request is rejected, requested number vnfs from user-id : %s in tenant-id: %s is over limitation. Please adjust quota for addtional resources. Debug-DB table %s" % (rsv['user_id'], rsv['tenant_id'], table)
            retrval = False
            break

        else:
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print " Checked ! Enough compute resources for reservation. Go ahead for reserving resources in advance."
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print " Recalculating resources and Updating to %s DB table" % table
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            new_rs_capacity = current_rs_capacity
            if retrval:
                print "Print out retrval flag : %s " %retrval

                new_rs_capacity['available_vcpus'] = int(current_rs_capacity['available_vcpus']) - int(reserved_rs['reserved_vcpus'])
                new_rs_capacity['reserved_vcpus'] = int(reserved_rs['reserved_vcpus'])
                new_rs_capacity['available_vmem'] = int(current_rs_capacity['available_vmem']) - int(reserved_rs['reserved_vmem'])
                new_rs_capacity['reserved_vmem'] = int(reserved_rs['reserved_vmem'])
                new_rs_capacity['available_vnfs'] = int(current_rs_capacity['available_vnfs']) - int(reserved_rs['reserved_vnfs'])
                new_rs_capacity['reserved_vnfs'] = int(reserved_rs['reserved_vnfs'])
                new_rs_capacity['created_at'] = datetime.datetime.now()
                print new_rs_capacity
                # mydb.add_row_rs(table_name=table, row_dict=new_rs_capacity)
                mydb.replace_row_by_uuid_composite(table_name=table, uuid=new_rs_capacity['uuid'], new_values_dict=new_rs_capacity)
    return retrval

def calculate_reserved_compute_rs_by_flavor(rsv):
    ''' this function is called after any operations like create/update/delete reservation
    return dictionary (need to define dict format for reserved resources included compute only)
    throw out exception if calculation is failed
    TODO: How to calculate reserved network resource ????
    '''
    # get number of instances in reservation dict and check how many instance in a rsv
    # return a dict of reserved resources after calculating
    # reserved resources = number of instances * flavor_detail
    reserved_rs_dict = {}
    flavor_id = rsv['flavor_id']
    number_vnfs = int(rsv['number_vnfs'])
    flavor_details = load_flavors_by_id(flavor_id=flavor_id)
    # print flavor_detail
    if number_vnfs == 1:
        reserved_rs_dict['reserved_vcpus'] = flavor_details['vcpu']
        reserved_rs_dict['reserved_vmem'] = flavor_details['vmem']
        reserved_rs_dict['reserved_vnfs'] = rsv['number_vnfs']
        reserved_rs_dict['reserved_vdisk'] = flavor_details['vdisk'] # TODO: this field should be moved to cinder-storage due to recent change between nova and cinder related to "vdisk"

        print " Detected that number of vnfs within reservation is: 1 , Reserved COMPUTE resources accordingly is: %s" % reserved_rs_dict
        # print reserved_rs_dict
        return reserved_rs_dict

    elif number_vnfs > 1:
        #flavor_detail = flavor_detail.update((x,y*int(number_instances)) for x,y in flavor_detail.items())
        for key in flavor_details:
            flavor_details[key] *= int(number_vnfs)
        reserved_rs_dict['reserved_vcpus'] = flavor_details['vcpu']
        reserved_rs_dict['reserved_vmem'] = flavor_details['vmem']
        reserved_rs_dict['reserved_vdisk'] = flavor_details['vdisk']

        print " Detected that number of vnfs within reservation is greater than 1 (number of vnfs = %s), " \
              "Reserved COMPUTE resources accordingly is: %s" % (number_vnfs, reserved_rs_dict)
        # print reserved_rs_dict
        return reserved_rs_dict
    else:
        print "Number of vnfs should be equal or greater than 1 or it is not in correct format."


def load_flavors_by_id(flavor_id):
    '''
    loading flavor template based on flavor_id and get all details about required resources for that flavor
    :param flavor_id:
    :return: a dict - all details about required resources for that flavor
    '''
    nova_client = get_nova_client('admin')
    flavor_list = nova_client.flavors.list(detailed=True)
    flavor_details = {}
    for flavor in flavor_list:
        print flavor.id
        if int(flavor.id) == int(flavor_id):
            flavor_details['flavor_name'] = flavor.name
            flavor_details['vcpu'] = flavor.vcpus
            flavor_details['vmem'] = flavor.ram
            flavor_details['vdisk'] = flavor.disk
            print flavor_details
            return flavor_details

        else:
            print("-"*35)
            print "flavor %s is not existing in VIM (Openstack)" % flavor_id
            print("-"*35)
            return 0


def get_current_available_resource(mydb, table_name, rsv):

    rows_count, row = mydb.get_newest_row_by_timestamp_userid_tenantid(table_name, rsv)

    if rows_count == 0:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "%s table is empty. Initializing available resource values by querying the various Controllers (e.g. Nova, Neutron, Cinder)...." % table_name
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        if table_name == 'users_util_compute_rm':
            init_data_current_user, result, added_uuid = init_resource_usage_compute_all_users_2_db(mydb=mydb, table=table_name, rsv=rsv)
            return init_data_current_user, added_uuid

        elif table_name == 'users_util_network_rm':
            todo
        elif table_name == 'users_util_storage_rm':
            todo

    elif rows_count > 0:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print " users resource usage values were already initialized in DB tables %s ---> Need to calculating and update existing resource values in %s table...." \
              % (table_name, table_name)
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        # if capacity resource table is not empty, getting uuid from rows_data dict
        # in this case we have override existing db record, hence in capacity tables just have only one record at a moment
        current_capacity_data = row
        print "Calculated resource usage --> Updating to DB..."
        print row
        return current_capacity_data[0], (current_capacity_data[0])['uuid']


def go_main():
    return 0

if __name__ == "__main__":

    try:
        nfvodb = utils_db()
        if nfvodb.connect(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)
        r, u = quota_resource_usage_sync_for_tenant(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5')

    except (KeyboardInterrupt, SystemExit):
        print 'Exiting Resource Management'
