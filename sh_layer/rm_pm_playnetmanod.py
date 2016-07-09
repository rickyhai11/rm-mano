import resource_db
from sh_layer import sh_reservation
# from sh_reservation import end_time_trigger, start_time_trigger
import sh_capacity

import multiprocessing
import sys
import os
import copy_reg
import types
import threading

global global_config
global_config = {'db_host': '116.89.184.43',
                  'db_user': 'root',
                  'db_passwd': '',
                  'db_name': 'mano_db'
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

# def main_loop():
#     # while 1:
#         #run two functions in parallel like two threads
#         # commands = ['start_vnf.start_time_trigger', 'start_vnf.end_time_trigger']
#         # parallelpy.run(commands=commands)
#     sh_ctrl = sh_reservation.sh_control()
#
#     p1 = Process(target=sh_ctrl.start_time_trigger).start()
#     # p1.start()
#     print 'p1 started '
#
#     p2 = Process(target=sh_ctrl.end_time_trigger).start()
#     # p2.start()
#     print 'p2 started'
#
#     p1.join()
#     print 'p1 joined'
#
#     p2.join()
#     print 'p2 joined'
#
# def _reduce_method(m):
#     if m.im_self is None:
#         return getattr, (m.im_class, m.im_func.func_name)
#     else:
#         return getattr, (m.im_self, m.im_func.func_name)
# copy_reg.pickle(types.MethodType, _reduce_method)


if __name__ == "__main__":

    try:
        mydb = resource_db.resource_db()
        print mydb
        if mydb.connect_db(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)
        sh_rsv = sh_reservation.sh_reservation()
        sh_ctrl = sh_reservation.sh_control()
        create_rsv = sh_rsv.create_reservation(mydb, data)

        sh_reservation.global_config = global_config
        sh_capacity.global_config = global_config

        # p1 = multiprocessing.Process(target=process, args=())
        # print p1
        # p1.start()
        # print 'p1 started '
        # p1.join()
        # print 'p1 joined'
        #
        # p2 = multiprocessing.Process(target=sh_reservation.end_time_trigger, args=(mydb,))
        # p2.start()
        # print 'p2 started'
        #
        # p2.join()
        # print 'p2 joined'

        t1 = threading.Thread(target=sh_ctrl.start_time_trigger, args=(mydb,))
        #t2 = threading.Thread(target=end_time_trigger, args=(mydb,))

        # t1.daemon = True
        # t2.daemon = True
        t1.start()
        #t2.start()
    except (KeyboardInterrupt, SystemExit):
            print 'Exiting Recource Management'
            exit()
            # main_loop()
# if __name__ == "__main__":
#
#         # Initialize DB connection
#     try:
#
#         mydb = resource_db.resource_db()
#         if mydb.connect_db(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
#             print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
#             exit(-1)
#         sh_reservation.global_config = global_config
#         sh_capacity.global_config = global_config
#
#         sh_rsv = sh_reservation.sh_reservation()
#         sh_ctrl = sh_reservation.sh_control()
#         create_rsv = sh_rsv.create_reservation(mydb, data)
#
#         sh_ctrl.start_time_trigger(mydb)
#
#         sh_ctrl.end_time_trigger(mydb)
#         # p2.start()
#         # print 'p2 started'
#         #
#         # p2.join()
#         # print 'p2 joined'
#     except KeyboardInterrupt:
#             print >> sys.stderr, '\nExiting by user request.\n'
#             sys.exit(0)
#

# def running_threads(self, mydb):
#     t1 = threading.Thread(target=self.start_time_trigger, args=(mydb,))
#     t2 = threading.Thread(target=self.end_time_trigger, args=(mydb,))
#
#     # t1.daemon = True
#     # t2.daemon = True
#     t1.start()
#     t2.start()
#     self.threads.append(t1)
#     self.threads.append(t2)
#
# def join_threads(threads):
#     for t in threads:
#         while t.isAlive():
#             t.join(5)


