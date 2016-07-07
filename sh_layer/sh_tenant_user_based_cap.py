'''
author: rickyhai
dcnlab
nguyendinhhai11@gmail.com
Implemetation capacity management of users in a given tenant.
'''

import sh_rm_monitoring as rm_monitor
from sh_rm_monitoring import get_nova_client



def check_user_compute_capacity(mydb, rsv):
    list_users_util_cap_tables = ['users_util_compute_rm', 'users_util_network_rm']  # TODO need to add 'users_util_storage_rm' table into this list after finishing implementation
    # flag to identify result of resource check: if true : successfully, otherwise failed
    retrval = True

    reserved_rs = calculate_reserved_compute_rs_by_flavor(rsv)
    # print reserved_rs
    for table in list_users_util_cap_tables:
        current_rs_capacity, uuid = get_current_available_resource(mydb=mydb, table_name=table)
        # print "current_rs_capacity"
        # print current_rs_capacity

        if table == 'vcpu_capacity' and reserved_rs['vcpu_reserved'] >= current_rs_capacity['vcpu_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table, table)
            retrval = False
            break

        elif table == 'vmem_capacity' and reserved_rs['vmem_reserved'] >= current_rs_capacity['vmem_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table, table)
            retrval = False
            break

        elif table == 'vdisk_capacity' and reserved_rs['disk_reserved'] >= current_rs_capacity['disk_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table, table)
            retrval = False
            break

        else:
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print " Checked ! Enough resource capacity for reservation. Go ahead for reserved resources in advance"
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            #rb_ = resource_db()
            new_rs_capacity = current_rs_capacity

            if table == 'vcpu_capacity' and retrval:
                # print retrval
                new_rs_capacity['vcpu_available'] = int(current_rs_capacity['vcpu_available']) - int(reserved_rs['vcpu_reserved'])
                new_rs_capacity['vcpu_reserved'] = int(reserved_rs['vcpu_reserved'])
                # print "new_rs_capacity da nhay vao trong checked owr vcpu capacity"
                print new_rs_capacity
                mydb.update_row_capacity_by_uuid(table_name=table, uuid=uuid, new_values_dict=new_rs_capacity)
                retrval = True

            elif table == 'vmem_capacity' and retrval:
                new_rs_capacity['vmem_available'] = int(current_rs_capacity['vmem_available']) - int(reserved_rs['vmem_reserved'])
                new_rs_capacity['vmem_reserved'] = int(reserved_rs['vmem_reserved'])

                mydb.update_row_capacity_by_uuid(table_name=table, uuid=uuid, new_values_dict=new_rs_capacity)
                retrval = True

            elif table == 'vdisk_capacity' and retrval:
                new_rs_capacity['disk_available'] = int(current_rs_capacity['disk_available']) - int(reserved_rs['disk_reserved'])
                new_rs_capacity['disk_reserved'] = int(reserved_rs['disk_reserved'])
                mydb.update_row_capacity_by_uuid(table_name=table, uuid=uuid, new_values_dict=new_rs_capacity)
                retrval = True
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


def get_current_available_resource(mydb, table_name):
    #print table_name
    #rdb_ = resource_db()

    rows_count, rows = mydb.get_table_capacity(table_name)

    if rows_count == 0:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "%s table is empty. Initializing available resource values by querying the various Controllers (e.g. Nova, Neutron, Cinder)...." % table_name
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        if table_name == 'vdisk_capacity':
            init_data = vdisk_op_stats()
        elif table_name == 'vcpu_capacity':
            init_data = vcpu_op_stats()
        elif table_name == 'vmem_capacity':
            init_data = vmem_op_stats()
        # if capacity resource table is empty, then call add_row_rs() for initializing first capacity resource values
        result, uuid = mydb.add_row_rs(table_name=table_name, row_dict=init_data)

        if result > 0:
            return init_data, uuid  #returned uuid is grabbed from add_row_rs() function
        else:
            print "failed to initialize %s value into DB" % init_data
            return result

    else:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "compute capacity values are already initialized in DB tables ---> Need to calculating and update existing available resources in DB...."
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        # if capacity resource table is not empty, getting uuid from rows_data dict
        # in this case we have override existing db record, hence in capacity tables just have only one record at a moment
        for row in rows: #currently just have only one row record in capacity tables. Hence, rows = row =1
            current_capacity_data = row
            print "Calculated resource usage --> Updating to DB..."
            print row
        return current_capacity_data, current_capacity_data['uuid']