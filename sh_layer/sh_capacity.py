import sys

import todo
import resource_db
import sh_compute_capacity_poll
import sh_network_capacity_poll
import sh_reservation

class capacity():

    def initiate_polling_vcpu_2_db(self):
        ''' this function is to call to resource_db.get_vcpu_db() to get the latest row with latest timestamp
        for checking_capacity() and calculate_capacity()
        '''
        invoke poll function from Op

        call to add_newrow to write new values to DB with timestamp


        todo
    def memm_capacity_db(self):
        todo

    def disk_capacity_db(self
        todo

    def network_capacity_db(self):
        todo

    def check_capacity(self):
        todo # how to implement this function????
        ''' this function is called before any operations like create/update
        return 0 if failed  and 1 if successful
        '''

    def calculate_capacity_vcpu(self):
        todo # how to implement this function????
        ''' this function is called after any operations like create/update/delete
        return dictionary (need to define dict format for resources capacity included compute and network)
        throw out exception if calculation is failed

        '''