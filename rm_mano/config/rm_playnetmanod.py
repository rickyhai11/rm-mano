from rm_mano.rm_engine.quota_manager import *
from rm_mano.rm_db.resource_db import *

global global_config
global_config = {'db_host': '116.89.184.43',
                  'db_user': 'root',
                  'db_passwd': '',
                  'db_name': 'rm_mano_v1'
                 }
global data
data = {}  # TODO (ricky) data dictionary shoul follow below format

'''
Table: reservation
Columns:
reservation_id int(36) AI PK
uuid varchar(36)
usage_id varchar(36)
label varchar(100)
region_id varchar(36)
user_id varchar(36)
project_id varchar(36)
resource varchar(36)
delta int(20)
start_time datetime
end_time datetime
expire datetime
status enum('ACTIVE','INACTIVE','BUILD','ERROR')
created_at datetime
updated_at datetime
deleted_at datetime
summary varchar(300)
'''

if __name__ == "__main__":

    try:
        nfvodb = Resource_db.resource_db()
        if nfvodb.connect(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)
        quotas = {'vcpus': 8, 'vnfs' : 11, 'vmemory': 11, 'network': 11, 'port': 11 }
        # quotas_result = create_quotas_project(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3', quotas=quotas)
        # print quotas_result

        # VimQuotaManager class test
        # region_new_limit = {'nova':{"cores": 80,"ram": 102400, "metadata_items": 800,"key_pairs": 800},'cinder':{"volumes": 80,"snapshots": 80, "gigabytes": 800,"backups": 800},'neutron':{"network":80,"port": 80,"router": 80}}
        quota_manager = VimQuotaManager(nfvodb)
        # quota_manager.quota_sync_for_project(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')

        # delete_quotas_for_tenant(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # quota_manager.update_quota_limits(project_id='f4211c8eee044bfb9dea2050fef2ace5', region_new_limit=region_new_limit, current_region='RegionOne')
        # quota_manager.get_region_for_project('f4211c8eee044bfb9dea2050fef2ace5')

        # test get actual usage resources from vim
        actual_usage = quota_manager.get_total_usage_for_tenant(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        print actual_usage


        # # test validate function
        # name = 'vcpu'
        # validate_resource_by_name(resource=name)

        # quotas_result = update_create_quotas_for_tenant(nfvodb, tenant_id='25970fbcfb0a4c2fb42ccc18f1bccde3', quotas=quotas)
        # print quotas_result

        # quotas_result= get_quotas_for_project(nfvodb, tenant_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # print quotas_result[0]

        # quotas_result = delete_quotas_for_tenant(nfvodb, tenant_id='25970fbcfb0a4c2fb42ccc18f1bccde3')

        # update ={'in_use': 3}
        # update_resource_usage_by_name(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5', resource='vnfs', actual_usage= update)
        # r_u = get_resource_usage(nfvodb, tenant_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # o_u = get_resource_usage_by_uuid_name(nfvodb, tenant_id='25970fbcfb0a4c2fb42ccc18f1bccde3', uuid_name='vcpus')
        # print o_u['vcpus']['reserved']
        # delete_resource_usage(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5')
        # sync_resource_usage(nfvodb, tenant_id='f4211c8eee044bfb9dea2050fef2ace5')

        # quotas_db = {'uuid': '1234dsd', 'project_id': 'af10gh', 'resource': 'vcpus', 'hard_limit': 10}
        # quotas =build_output_quota_limit(quotas_db)

        # test get quota project function that return converted format to api request
        # out_quotas= get_quotas_for_project(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # out_quotas= get_specific_quota_by_project(nfvodb, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3', resource='vcpus')
        # print out_quotas

        # test limit_check() and available_check() functions
        # values = {'vcpus': 10, 'vnfs' : 10, 'memory': 11, 'network': 10,}
        # limit_check(nfvodb, values, project_id ='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # re= available_resource_check_for_project(nfvodb, values, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
        # print re

        # test covert resource usage function
        # db_usage = {'deleted_at': None, 'resource': 'port', 'uuid': '8b36d48f-903d-11e6-b184-0050568b49a9',
        #             'user_id': None, 'created_at': None, 'in_use': 0L, 'updated_at': datetime.datetime(2016, 10, 12, 14, 13, 14),
        #             'until_refresh': 0, 'reserved': 0L, 'project_id': '25970fbcfb0a4c2fb42ccc18f1bccde3'}
        # out_usage = build_output_resource_usage(db_usage)
        # print out_usage

    except (KeyboardInterrupt, SystemExit):
            print 'Exiting Recource Management'
            exit()

# def multi_processing_reservations():
#
#     sh_rsv = Reservation.Reservation()
#     sh_ctrl = Reservation.sh_control()
#     create_rsv = sh_rsv.create_reservation(nfvodb, data)
#
#     Reservation.global_config = global_config
#     sh_total_quota_manager.global_config = global_config
#
#     p1 = multiprocessing.Process(target=process, args=())
#     print p1
#     p1.start()
#     print 'p1 started '
#     p1.join()
#     print 'p1 joined'
#
#     p2 = multiprocessing.Process(target=Reservation.end_time_trigger, args=(nfvodb,))
#     p2.start()
#     print 'p2 started'
#
#     p2.join()
#     print 'p2 joined'
#
#     t1 = threading.Thread(target=sh_ctrl.start_time_trigger, args=(nfvodb,))
#     t2 = threading.Thread(target=end_time_trigger, args=(nfvodb,))
#
#     t1.daemon = True
#     t2.daemon = True
#     t1.start()
#     t2.start()
#
#     return
