import sys

import todo
import resource_db
import sh_compute_capacity_poll
import sh_network_capacity_poll

class capacity():

    def vcpu_capacity_db(self):
        ''' this function is to call to resource_db.get_vcpu_db() to get the latest row with latest timestamp
        for checking_capacity() and calculate_capacity()
        '''
        todo
    def memm_capacity_db(self):
        todo

    def disk_capacity_db(self):
        todo

    def network_capacity_db(self):
        todo

    def check_capacity(self):
        todo # how to implement this function????
        ''' this function is called before any operations like create/update
        return 0 if failed  and 1 if successful
        '''
    def calculate_capacity(self):
        todo # how to implement this function????
        ''' this function is called after any operations like create/update/delete
        return dictionary (need to define dict format for resources capacity included compute and network)
        throw out exception if calculation is failed

        '''