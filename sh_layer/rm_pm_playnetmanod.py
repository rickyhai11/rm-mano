import resource_db
import sh_reservation
import sh_capacity

from multiprocessing import Process

global global_config
global_config = {'db_host': 'localhost',
                  'db_user': 'root',
                  'db_password': 'S@igon0011',
                  'db_name': 'rm_db'
                 }

def main_loop():
    # while 1:
        #run two functions in parallel like two threads
        # commands = ['start_vnf.start_time_trigger', 'start_vnf.end_time_trigger']
        # parallelpy.run(commands=commands)
    sh_ctrl = sh_reservation.sh_control()

    p1 = Process(target=sh_ctrl.start_time_trigger)
    p1.start()
    print 'p1 started '

    p2 = Process(target=sh_ctrl.end_time_trigger)
    p2.start()
    print 'p2 started'

    p1.join()
    print 'p1 joined'

    p2.join()
    print 'p2 joined'

if __name__ == "__main__":
    try:
        # Initialize DB connection
        mydb = resource_db.resource_db();
        if mydb.connect_db(global_config['db_host'], global_config['db_user'], global_config['db_passwd'], global_config['db_name']) == -1:
            print "Error connecting to database", global_config['db_name'], "at", global_config['db_user'], "@", global_config['db_host']
            exit(-1)

        sh_reservation.global_config = global_config
        sh_capacity.global_config = global_config

        sh_rsv = sh_reservation.sh_reservation()
        create_rsv = sh_rsv.create_reservation(mydb, data) #TODO need to define inpout parameters right here: nfvo or sh layer will give "data" dict
        main_loop()

    except (KeyboardInterrupt, SystemExit):
        print 'Exiting playnetmanod'
        exit()


