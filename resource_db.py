import MySQLdb.cursors
import MySQLdb as rmdb
import json
import sys
from threading import Thread
from collections import defaultdict

import todo
from sh_layer import sh_total_compute_capacity_util_poll_op as sh_compute
global global_config
global_config = {'db_host': 'localhost',
                  'db_user': 'root',
                  'db_passwd': 'S@igon0011',
                  'db_name': 'rm_db'
                 }
# global data
# data = {'reservation_id': '6789',
#         'label': 'test2',
#         'host_id': "12212817268DJKHSAJD",
#         'host_name': 'hai_compute',
#         'user_id': '48c70b9e59c240768bb2b88ffb1eb66c',
#         'user_name': 'admin',
#         'tenant_id': 'cfcb18eef55b4b03bb075ea106fe771f',
#         'tenant_name': 'admin',
#         'start_time': '2016-04-21 12:11:11',
#         'end_time': '2016-04-21 12:22:22',
#         'flavor_id': '1',
#         'image_id': '3d356f2b-79da-468e-8e31-ec0c861190e1',
#         'network_id': 'f61491df-3ad8-4ac4-9974-6b6ea27bf5f0',
#         'number_instance': '1',
#         'instance_id': 'null',   # this attribute need to be updated after instance is created (start_time arrived)
#         'ns_id': 'SJDHS765327SDHJSG8236BSD826734',
#         'status': 'ACTIVE',
#         'summary': 'reservation testing'
#         }
'''
Should consider to user array for status field
'''

vmem_capa= {'uuid': 3,"mem_total": 12, "vmem_total": 12, "vmem_used": 5, "mem_available": 5, "vmem_available": 6}

vcpu={'uuid': 13,"cpu_total": 15, "vcpu_total" : 20, "vcpu_allocated": 10, "cpu_available": 8, "vcpu_available": 65, 'vcpu_reserved' : 0}
            #"created_at": '2016-04-13 12:30:20', "modified_at": '2016-04-13 12:30:59' }
flavor_dict = {'flavor_id': 2, 'name': 'm.medium', 'ram': 1024, 'disk': 2, 'vcpu': 2}

image_dict = {'image_id': '19f7025b-b78a-4bf0-bc37-0cba68e16b10', 'name': 'ubuntu_01'}

class resource_db():

    ####################################################################################################################
    #connect and disconnect DB
    ####################################################################################################################
    def __init__(self):
        print "============================================================================"

    def connect_db(self, host=None, user=None, passwd=None, database=None):
        '''
        :param host:
        :param user:
        :param passwd:
        :param database:
        :return:
        Connect to specific database. valid host, user, passwd and database must be provided
        '''
        try:
            if host is not None: self.host = host
            if user is not None: self.user = user
            if passwd is not None: self.passwd = passwd
            if database is not None: self.database = database
            # if cursorclass is not None: self.cursorclass = cursorclass

            self.con =rmdb.connect(self.host, self.user, self.passwd, self.database)
            print "DB: connected to %s@%s ---> %s" %(self.user, self.host, self.database)
            return 0
        except rmdb.Error, e:
            print "cannot connect to %s@%s ---> %s Error %d:%s" % (self.user, self.host, self.database, e.args[0],
                                                                   e.args[1])
            return -1

    def disconnect(self):
        '''disconnect from specific data base'''
        try:
            self.con.close()
            del self.con
        except rmdb.Error, e:
            print "Error disconnecting from DB: Error %d: %s" % (e.args[0], e.args[1])
            return -1
        except AttributeError, e: #self.con not defined
            if e[0][-5:] == "'con'": return -1, "Database internal error, no connection."
            else: raise

    # def reload_connect_db(self):
    #     self.con = self.connect_db(host="localhost", user="root", passwd="S@igon0011", database="rm_db")
    #     if self.con is not None:
    #         return self.con


    ####################################################################################################################
    #CRUD DB operations for reservation
    ####################################################################################################################

    # common adding data to DB table function
    def add_row_rs(self, table_name, row_dict):
        ''' add_row_resources could be used like global adding function for adding any data with dict/json format to DB
        for example:
            if Add a new reservation to reservation table
            input parameters:
                table_name: name of table in mySQL DB
                rowdict: dictionary for reservation attributes as below structure
                    data = {'reservation_id': '12345',
                    'label': 'test1',
                    'host': "hai_compute",
                    'user': 'ricky',
                    'project': 'admin',
                    'start_time': '2016-04-13 12:19:20',
                    'end_time': '2016-04-13 12:30:20',
                    'flavor_id': '1',
                    'image_id': 'asddsds',
                    'instance_id': "sjdgsjhdgsjh"
                    'summary': 'reservation testing',
                    'status': 'ACTIVE'
                    }
                    XXX tablename not sanitized
                    XXX test for allowed keys is case-sensitive
                    filter out keys that are not column names'''

        #self.con = self.reload_connect_db()

        self.con
        self.cursor=self.con.cursor()
        self.cursor.execute("describe %s" % table_name)
        self.allowed_keys = set(row[0] for row in self.cursor.fetchall())
        #print self.allowed_keys
        self.keys = self.allowed_keys.intersection(row_dict)
        #print "print keys"
        #print self.keys

        if len(row_dict) > len(self.keys):
            unknown_keys = set(row_dict) - self.allowed_keys
            print >> sys.stderr, "skipping keys:", ", ".join(unknown_keys)

        columns = ", ".join(self.keys)
        values_template = ", ".join(["%s"] * len(self.keys))
        try:
            sql = "insert into %s (%s) values (%s)" % (
                table_name, columns, values_template)
            values = tuple(row_dict[key] for key in self.keys)
            print sql
            print values
            self.cursor.execute(sql, values)
            added = self.cursor.rowcount
            #get last added id in a table
            added_id = self.cursor.lastrowid  #Returns the value generated for an AUTO_INCREMENT column TODO
            print added_id
            self.con.commit()
            if added > 0:

                print "Inserted new row successfully"
                return added, added_id
            else:
                print "Failed to add a new row into database table: %s" % table_name
                return added

        except (rmdb.Error, AttributeError), e:
            print "resource_db.add_row_rs DB Exception %d : %s" % (e.args[0], e.args[1])
            self.con.rollback()


    def delete_row_by_rsv_id(self, table_name, reservation_id):
        '''
        Delete a reservation from database with reservation ID from reservation table
        :param table:
        :return:
        '''
        # for retry_ in range(0,2):
        #self.con = self.reload_connect_db()

        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "DELETE FROM %s WHERE reservation_id = '%s'" % (table_name, reservation_id)
                print sql
                self.cur.execute(sql)
                deleted = self.cur.rowcount
                print "Delete successfully a reservation: %s " % deleted
            return deleted
        except (rmdb.Error, AttributeError), e:
                print "resource_db.delete_row DB Exception %d : %s" % (e.argrs[0], e.args[1])

    def update_row_timestamp_by_rsv_id(self, table_name, reservation_id, start_time, end_time):
        '''
        this function is to update start_time and end_time of a reservation from reservation table
        :param self:
        :param reservation_id:
        :param start_time:
        :param end_time:
        :return:
        '''

        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "UPDATE %s SET start_time='%s',end_time='%s' WHERE reservation_id = '%s'" % (table_name,
                                                                            start_time, end_time, reservation_id)
                print sql
                self.cur.execute(sql)
                updated = self.cur.rowcount
                print "Update successfully a reservation: %s " % updated
            return updated
        except (rmdb.Error, AttributeError), e:
            print "resource_db.update_row DB Exception %d : %s" % (e.args[0], e.args[1])


    def update_row_rsv(self, table_name, reservation_id, new_values_dict):
        '''
        Removes the old (based on reservation_id) and adds a new reservation with new values (new reservation is created as well)
        Attribute
        :param table_name: table where to insert
        :param old_reservation:
        :param new_values_dict: is a dictionary with format as below
        :return: (delete, new_reservation_id)
        '''
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "DELETE FROM %s WHERE reservation_id= '%s'" % (table_name, reservation_id)
                print sql
                self.cur.execute(sql)
                deleted = self.cur.rowcount
                #print deleted
                if deleted > 0 and new_values_dict:
                    print "Deleted successfully next step --> adding a new reservation for new values"
                    self.add_row_rs(table_name, new_values_dict)
                    print "Updated new values into %s table successfully" % table_name
                    new_reservation_id = new_values_dict['reservation_id']

                    return deleted, new_reservation_id

                else:
                    print "Failed to delete previous values in db ######'%s row has been deleted'###### OR " \
                          "###### 'reservation_id': %s was not existing " \
                          "in %s table ######" % (deleted, reservation_id, table_name)

        except (rmdb.Error, AttributeError), e:
            print "resource_db.update_row_capacity_by_uuid DB Exception %d : %s" % (e.args[0], e.args[1])

    def update_row_vapp_id_by_rsv_id(self, table_name, reservation_id, vapp_id):
        '''
        this function is to update values for a reservation

        :param talble_name:
        :param reservation_id: esxting reservation in DB
        :param vapp_id = instance_id in this case this field need to be updated after starting time has been triggered
        and instance has been created
        :return:
        '''
        #self.con = self.reload_connect_db()
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "UPDATE %s SET instance_id='%s' WHERE reservation_id = '%s'" % (table_name,
                                                                            vapp_id, reservation_id)
                print sql
                self.cur.execute(sql)
                updated = self.cur.rowcount
                print "Updated vapp_id: %s successfully for %s reservation" % (vapp_id, updated)
            return updated
        except (rmdb.Error, AttributeError), e:
            print "resource_db.update_row DB Exception %d : %s" % (e.args[0], e.args[1])


    def get_rsv_by_id(self, table_name, reservation_id):
        '''
        this function is to list a reservation from DB table with reservation_id
        :param table_name:
        :param reservation_id:
        :return:
        '''
        try:
            with self.con:
                self.cur= self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM %s WHERE reservation_id= '%s'" % (table_name, reservation_id)
                self.cur.execute(sql)
                rows = self.cur.fetchone()
                listed = self.cur.rowcount
                print "query reservation with id %s successfully" % reservation_id
                #print listed
                print rows['reservation_id']
                return listed, rows
        except(rmdb.Error, AttributeError), e:
            print "resource_db.get_rsv_by_id DB exception %d: %s" % (e.args[0], e.args[1])

    # common function- shared function for get values of a column in a table
    def get_column_from_table(self, table_name, column):
        '''
        this function is to get values of a column in a table
        :param table_name:
        :param column: name of column
        :return: list of values for that coresponding column
        '''
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "SELECT %s FROM %s" % (column, table_name)
                print sql
                self.cur.execute(sql)
                rows = self.cur.fetchall()
                print rows
                #for row in rows:
                    #print row[0]
                return rows
        except(rmdb.Error, AttributeError), e:
            print "resource_db.get_column_from_table DB exception %d: %s" % (e.args[0], e.args[1])

    def get_rsv_by_status(self, status):
        #self.con = self.reload_connect_db()
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM reservation WHERE status= '%s'" % status
                self.cur.execute(sql)
                list_rsv = self.cur.fetchall()
                listed = self.cur.rowcount
                #self.cur.close()
                print "There are %s reservations with '%s' status." % (listed, status)
                #print list_rsv
                return list_rsv
        except(rmdb.Error, AttributeError), e:
            print "resource_db.get_rsv_by_status DB exception %d: %s" % (e.args[0], e.args[1])




    ####################################################################################################################
    # CRUD DB operations which are related to compute and network resources
    ####################################################################################################################
    '''
    # re-use common adding data to db function for adding new row into db table
    def add_row_rs(self, table_name, row_dict)
    '''
    def update_row_capacity_by_uuid(self, table_name, uuid, new_values_dict):
        '''
        Removes the old (based on uuid) and adds the new values for resource capacity tables (vcpu, vmem,vdisk, network etc...)
        Attribute
        :param table_name: table where to insert
        :param uuid: input uuid that using to del
        :param new_values_dict: is a dictionary with format as below (included new 'uuid' field)
            vcpu={'uuid': 13,"cpu_total": 15, "vcpu_total" : 20,"vcpu_used": 10, "cpu_available": 8, "vcpu_available":65}
        :return: (delete, new_uuid)
        '''
        #self.con = self.reload_connect_db()
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "DELETE FROM %s WHERE uuid= '%s'" % (table_name, uuid)
                print sql
                self.cur.execute(sql)
                deleted = self.cur.rowcount
                #print deleted
                if deleted > 0 and new_values_dict:
                    print "Deleted successfully next step --> adding new values"
                    self.add_row_rs(table_name, new_values_dict)
                    print "Updated new values into %s table successfully" % table_name
                    #new_uuid = new_values_dict['uuid']

                    return deleted #new_uuid

                else:
                    print "Failed to delete previous values in db ######'%s row has been deleted'###### OR " \
                          "###### 'uuid': %s was not existing " \
                          "in %s table ######" % (deleted, uuid, table_name)

        except (rmdb.Error, AttributeError), e:
            print "resource_db.update_row_capacity_by_uuid DB Exception %d : %s" % (e.args[0], e.args[1])

    def delete_row_capacity_by_uuid(self, table_name, uuid):
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "DELETE FROM %s WHERE uuid= '%s'" % (table_name, uuid)
                print sql
                self.cur.execute(sql)
                deleted = self.cur.rowcount
                #print deleted
                if deleted > 0:
                    print "Deleted successfully next step --> adding new values"
                    return deleted

                else:
                    print "Failed to delete"
                    print "###### %s row has been deleted ######" % deleted
                    print "###### 'uuid': %s was not existing in %s table ######" % (uuid, table_name)

        except (rmdb.Error, AttributeError), e:
            print "resource_db.update_row_capacity_by_uuid DB Exception %d : %s" % (e.args[0], e.args[1])

    def get_row_capacity_by_uuid(self, table_name, uuid):
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM %s WHERE uuid = '%s'" % (table_name, uuid)
                self.cur.execute(sql)
                rows = self.cur.fetchone()
                listed = self.cur.rowcount
                print " Query capacity with uuid %s successfully" % uuid
                print listed
                print rows
                return listed, rows
        except(rmdb.Error, AttributeError), e:
            print "resource_db.get_row_capacity_by_uuid DB exception %d: %s" % (e.args[0], e.args[1])

    def get_table_capacity(self, table_name):
        #self.con = self.reload_connect_db()
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM %s" % table_name
                self.cur.execute(sql)
                rows = self.cur.fetchall()
                listed = self.cur.rowcount
                # for row in rows:   # for debug
                #     print row
                print " query all of %s table successfully" % table_name
                return listed, rows
        except(rmdb.Error, AttributeError), e:
            print "resource_db.get_table_capacity DB exception %d: %s" % (e.args[0], e.args[1])


    ####################################################################################################################
    #unused functions so far (before intergration with playnetMANO v2)
    ####################################################################################################################

    def __str2db_format(self, data):
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

    def __tuple2db_format_set(self, data):
        '''Compose the needed text for a SQL SET, parameter 'data' is a pair tuple (A,B),
        and it returns the text 'A="B"', where A is a field of a table and B is the value
        If B is None it returns the 'A=Null' text, without surrounding Null by quotes
        If B is not None it returns the text "A='B'" or 'A="B"' where B is surrounded by quotes,
        and it ensures internal quotes of B are escaped.
        '''
        if data[1]==None:
            return str(data[0]) + "=Null"
        out=str(data[1])
        if "'" not in out:
            return str(data[0]) + "='" + out + "'"
        elif '"' not in out:
            return str(data[0]) + '="' + out + '"'
        else:
            return str(data[0]) + '=' + json.dumps(out)

    def __tuple2db_format_where(self, data):
        '''Compose the needed text for a SQL WHERE, parameter 'data' is a pair tuple (A,B),
        and it returns the text 'A="B"', where A is a field of a table and B is the value
        If B is None it returns the 'A is Null' text, without surrounding Null by quotes
        If B is not None it returns the text "A='B'" or 'A="B"' where B is surrounded by quotes,
        and it ensures internal quotes of B are escaped.
        '''
        if data[1]==None:
            return str(data[0]) + " is Null"
        out=str(data[1])
        if "'" not in out:
            return str(data[0]) + "='" + out + "'"
        elif '"' not in out:
            return str(data[0]) + '="' + out + '"'
        else:
            return str(data[0]) + '=' + json.dumps(out)

    def __tuple2db_format_where_not(self, data):
        '''Compose the needed text for a SQL WHERE(not). parameter 'data' is a pair tuple (A,B),
        and it returns the text 'A<>"B"', where A is a field of a table and B is the value
        If B is None it returns the 'A is not Null' text, without surrounding Null by quotes
        If B is not None it returns the text "A<>'B'" or 'A<>"B"' where B is surrounded by quotes,
        and it ensures internal quotes of B are escaped.
        '''
        if data[1]==None:
            return str(data[0]) + " is not Null"
        out=str(data[1])
        if "'" not in out:
            return str(data[0]) + "<>'" + out + "'"
        elif '"' not in out:
            return str(data[0]) + '<>"' + out + '"'
        else:
            return str(data[0]) + '<>' + json.dumps(out)

    def __remove_quotes(self, data):
        '''remove single quotes ' of any string content of data dictionary'''
        for k,v in data.items():
            if type(v) == str:
                if "'" in v:
                    data[k] = data[k].replace("'","_")


    ####################################################################################################################
    # main function for testing above code
    ####################################################################################################################

if __name__ == '__main__':
    db = resource_db()
    #a = db.connect_db(host="localhost", user="root", passwd="S@igon0011", database="rm_db")
    #cursor = db.con.cursor()
    #cursor = db.con.cursor(MySQLdb.cursors.DictCursor)
    #db.add_row_rs('reservation', data) #sh_compute.vmem_op_stats())
    #db.add_row_rs('vcpu_capacity', vcpu) #sh_compute.vmem_op_stats())

    #db.delete_row_by_rsv_id(table_name,'12345')
    # db.update_row_timestamp_by_rsv_id(table_name,'12345','2016-04-14 11:11:11','2016-04-15 22:22:22')
    #db.get_rsv_by_id('reservation','12345')
    #db.update_row_capacity_by_uuid('vmem_capacity', 2, vmem_capa)
    dat_table = db.get_table_capacity('vdisk_capacity')
    #print dat_table
    # list_rsv = db.get_rsv_by_status('ACTIVE')
    # for rsv in list_rsv:
    #     print rsv
    #     start_time = rsv['start_time']
    #     print start_time
