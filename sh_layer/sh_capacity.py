import sys
import json

import todo
from  resource_db import resource_db
from sh_compute_capacity_poll import vcpu_op_stats
from sh_compute_capacity_poll import vdisk_op_stats
from sh_compute_capacity_poll import vmem_op_stats
from sh_compute_capacity_poll import load_flavors_by_id
import sh_network_capacity_poll

global global_config

def check_resource_capacity(mydb, rsv):
    list_capacity_tables = ['vcpu_capacity', 'vmem_capacity', 'vdisk_capacity']
    retrval = True

    reserved_rs = calculate_reserved_compute_rs_by_flavor(rsv)
    # print "Total reserved resources:"
    # print reserved_rs
    for table_name in list_capacity_tables:
        current_rs_capacity, uuid = get_current_available_resource(mydb=mydb, table_name=table_name)
        # print "current_rs_capacity"
        # print current_rs_capacity

        if table_name == 'vcpu_capacity' and reserved_rs['vcpu_reserved'] >= current_rs_capacity['vcpu_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table_name, table_name)
            retrval = False
            break

        elif table_name == 'vmem_capacity' and reserved_rs['vmem_reserved'] >= current_rs_capacity['vmem_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table_name, table_name)
            retrval = False
            break

        elif table_name == 'vdisk_capacity' and reserved_rs['disk_reserved'] >= current_rs_capacity['disk_available']:
            print "Request is rejected due to lack of %s resources. Resources request for %s is not satisfied." %(table_name, table_name)
            retrval = False
            break

        else:
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print " Checked ! Enough resource capacity for reservation. Go ahead for reserved resources in advance"
            print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            #rb_ = resource_db()
            new_rs_capacity = current_rs_capacity

            if table_name == 'vcpu_capacity' and retrval:
                print retrval
                new_rs_capacity['vcpu_available'] = int(current_rs_capacity['vcpu_available']) - int(reserved_rs['vcpu_reserved'])
                new_rs_capacity['vcpu_reserved'] = int(reserved_rs['vcpu_reserved'])
                print "new_rs_capacity da nhay vao trong checked owr vcpu capacity"
                print new_rs_capacity
                mydb.update_row_capacity_by_uuid(table_name=table_name, uuid=uuid, new_values_dict=new_rs_capacity)
                retrval = True

            elif table_name == 'vmem_capacity' and retrval:
                new_rs_capacity['vmem_available'] = int(current_rs_capacity['vmem_available']) - int(reserved_rs['vmem_reserved'])
                new_rs_capacity['vmem_reserved'] = int(reserved_rs['vmem_reserved'])

                mydb.update_row_capacity_by_uuid(table_name=table_name, uuid=uuid, new_values_dict=new_rs_capacity)
                retrval = True

            elif table_name == 'vdisk_capacity' and retrval:
                new_rs_capacity['disk_available'] = int(current_rs_capacity['disk_available']) - int(reserved_rs['disk_reserved'])
                new_rs_capacity['disk_reserved'] = int(reserved_rs['disk_reserved'])
                mydb.update_row_capacity_by_uuid(table_name=table_name, uuid=uuid, new_values_dict=new_rs_capacity)
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
    number_instances = int(rsv['number_instance'])
    flavor_detail = load_flavors_by_id(flavor_id=flavor_id)
    # print flavor_detail
    if number_instances == 1:
        reserved_rs_dict['vcpu_reserved'] = flavor_detail['vcpu']
        reserved_rs_dict['vmem_reserved'] = flavor_detail['vmem']
        reserved_rs_dict['disk_reserved'] = flavor_detail['vdisk']
        print reserved_rs_dict
        return reserved_rs_dict

    elif number_instances > 1:
        #flavor_detail = flavor_detail.update((x,y*int(number_instances)) for x,y in flavor_detail.items())
        for key in flavor_detail:
            flavor_detail[key] *= int(number_instances)
        reserved_rs_dict['vcpu_reserved'] = flavor_detail['vcpu']
        reserved_rs_dict['vmem_reserved'] = flavor_detail['vmem']
        reserved_rs_dict['disk_reserved'] = flavor_detail['vdisk']
        print reserved_rs_dict
        return reserved_rs_dict
    else:
        print "number of instance should be equal or greater than 1 or it is not in correct format"

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
            print "print row at get_current_available_resource function"
            print row
        return current_capacity_data, current_capacity_data['uuid']

def __str2db_format(data):
    '''Convert string data to database format.
    If data is None it returns the 'Null' text,
    otherwise it returns the text surrounded by quotes ensuring internal quotes are escaped.
    '''
    if data==None:
        return 'Null'
    out=str(data)
    if "'" not in out:
        return "'" + out + "'"
    elif '"' not in out:
        return '"' + out + '"'
    else:
        return json.dumps(out)

if __name__ == '__main__':
    check_resource_capacity()

#
# def initialize_compute_rs_capacity_into_db(table_name):
#         print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#         print "%s table is empty. Initializing first available resource values...." % table_name
#         print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#         if table_name == 'vdisk_capacity':
#             init_data = vdisk_op_stats()
#         elif table_name == 'vcpu_capacity':
#             init_data = vcpu_op_stats()
#         elif table_name == 'vmem_capacity':
#             init_data = vmem_op_stats()
#         # if capacity resource table is empty, then call add_row_rs() for initializing first capacity resource values
#         rdb_ = resource_db()
#         result, uuid = rdb_.add_row_rs(table_name=table_name, row_dict=init_data)
#
#         if result > 0:
#             return result ,uuid
#         else:
#             print "failed to initialize %s value into DB" % init_data
#
# def update_compute_rs_capacity_into_db(table_name):
#     print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#     print "compute capacity values are already initialized in DB tables ---> Updating existing available resource values in DB...."
#     print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#     if table_name == 'vdisk_capacity':
#         init_data = vdisk_op_stats()
#     elif table_name == 'vcpu_capacity':
#         init_data = vcpu_op_stats()
#     elif table_name == 'vmem_capacity':
#         init_data = vmem_op_stats()
#     # if capacity resource table is empty, then call add_row_rs() for initializing first capacity resource values
#     rdb_ = resource_db()
#     result = rdb_.update_row_capacity_by_uuid(table_name=table_name)
#
#     if result > 0:
#         return result
#     else:
#         print "failed to initialize %s value into DB" % init_data
#         return result

# def vdisk_capacity_init():
#     init_data = vdisk_op_stats()
#     rdb_ = resource_db()
#     result = rdb_.add_row_rs(table_name='vdisk_capacity', row_dict=init_data)
#
#     if result > 0:
#         return result
#     else:
#         print "failed to initialize vdisk capacity value into DB"

#*********************************************
#   NOVA
#*********************************************

def get_flavor_id(nova_client, flavor_name):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if f.name == flavor_name:
            id = f.id
            break
    return id

def get_flavor_id_by_ram_range(nova_client, min_ram, max_ram):
    flavors = nova_client.flavors.list(detailed=True)
    id = ''
    for f in flavors:
        if min_ram <= f.ram and f.ram <= max_ram:
            id = f.id
            break
    return id

def get_instance_status(nova_client, instance):
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.status
    except Exception, e:
        # print "Error [get_instance_status(nova_client, '%s')]:" % \
        #    str(instance), e
        return None

def get_instances(nova_client):
    try:
        instances = nova_client.servers.list(search_opts={'all_tenants': 1})
        return instances
    except Exception, e:
        print "Error [get_instances(nova_client)]:", e
        return None
