from sh_layer.rm_engine.sh_quota_manager import *
from sh_layer.common.utils_rm import *


global global_config
global_config = {'db_host': '116.89.184.43',
                  'db_user': 'root',
                  'db_passwd': '',
                  'db_name': 'rm_mano_v1'
                 }
global data
data = {'reservation_id': '5555',
        'label': 'test4',
        'host_id': "cfcb18eef55b4b03bb075ea106fe771f",
        'host_name': 'hai_compute',
        'user_id': 'ffbc3c72aa9f44769f3430093c59c457',
        'user_name': 'demo',
        'tenant_id': '4a766494021447c7905b81adae050a97',
        'tenant_name': 'demo',
        'start_time': '2016-07-09 18:04:00',
        'end_time': '2016-07-09 18:09:00',
        'flavor_id': 1,
        'image_id': '68e9fa2a-afa2-4e32-8598-35cea0f704fa',
        'network_id': '2d54f36a-8569-4a71-806c-f563a9aa6367',
        'number_vnfs': '1',
        'ns_id': 'cfcb18eef55b4b03bb075ea106fe771f',
        'status': 'ACTIVE',
        'summary': 'reservation testing'
        }


if __name__ == "__main__":

    try:
        nfvodb = resource_db.resource_db()
        if nfvodb.connect(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)
        # quotas = {'vcpus': 11, 'vnfs' : 11, 'memory': 11, 'network': 11, 'port': 11 }

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
        values = {'vcpus': 10, 'vnfs' : 10, 'memory': 11, 'network': 10,}
        # limit_check(nfvodb, values, project_id ='25970fbcfb0a4c2fb42ccc18f1bccde3')
        re= available_resource_check_for_project(nfvodb, values, project_id='25970fbcfb0a4c2fb42ccc18f1bccde3')
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
#     sh_rsv = sh_reservation.sh_reservation()
#     sh_ctrl = sh_reservation.sh_control()
#     create_rsv = sh_rsv.create_reservation(nfvodb, data)
#
#     sh_reservation.global_config = global_config
#     sh_total_quota_manager.global_config = global_config
#
#     p1 = multiprocessing.Process(target=process, args=())
#     print p1
#     p1.start()
#     print 'p1 started '
#     p1.join()
#     print 'p1 joined'
#
#     p2 = multiprocessing.Process(target=sh_reservation.end_time_trigger, args=(nfvodb,))
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
