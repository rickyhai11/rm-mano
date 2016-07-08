import MySQLdb.cursors
import MySQLdb as mdb
import uuid as myUuid
import json
import sys
import yaml
from collections import OrderedDict
import requests
from jsonschema import validate as js_v, exceptions as js_e


global global_config
global_config = {'db_host': 'localhost',
                  'db_user': 'root',
                  'db_passwd': 'S@igon0011',
                  'db_name': 'rm_db'
                 }
data = {'reservation_id': '22222',
        'label': 'test4',
        'host_id': "12212817268DJKHSAJD",
        'host_name': 'hai_compute',
        'user_id': 'ffbc3c72aa9f44769f3430093c59c457',
        'user_name': 'admin',
        'tenant_id': '4a766494021447c7905b81adae050a97',
        'tenant_name': 'demo',
        'start_time': '2016-05-23 18:04:00',
        'end_time': '2016-05-23 18:09:00',
        'flavor_id': 1,
        'image_id': 'bf9d2214-4032-4b0a-8588-0fb73fc7d57c',
        'network_id': 'f61491df-3ad8-4ac4-9974-6b6ea27bf5f0',
        'number_instance': '1',
        'instance_id': 'null',   # this attribute need to be updated after instance is created (start_time arrived)
        'ns_id': 'ffbc3c72aa9f44769f3430093c59c457',
        'status': 'ACTIVE',
        'summary': 'reservation testing'
        }
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

            self.con =mdb.connect(self.host, self.user, self.passwd, self.database)
            print "DB: connected to %s@%s ---> %s" %(self.user, self.host, self.database)
            return 0
        except mdb.Error, e:
            print "cannot connect to %s@%s ---> %s Error %d:%s" % (self.user, self.host, self.database, e.args[0],
                                                                   e.args[1])
            return -1

    def disconnect(self):
        '''disconnect from specific data base'''
        try:
            self.con.close()
            del self.con
        except mdb.Error, e:
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
            # get last added id in a table
            added_uuid = self.cursor.lastrowid  # Returns the value generated for an AUTO_INCREMENT column TODO
            print added_uuid
            self.con.commit()
            if added > 0:

                print "Inserted new row successfully"
                return added, added_uuid
            else:
                print "Failed to add a new row into database table: %s" % table_name
                return added

        except (mdb.Error, AttributeError), e:
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
        except (mdb.Error, AttributeError), e:
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
        except (mdb.Error, AttributeError), e:
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

        except (mdb.Error, AttributeError), e:
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
        except (mdb.Error, AttributeError), e:
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
        except(mdb.Error, AttributeError), e:
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
        except(mdb.Error, AttributeError), e:
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
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_rsv_by_status DB exception %d: %s" % (e.args[0], e.args[1])




    ####################################################################################################################
    # CRUD DB operations which are related to compute and network resources - CALCULATING AGAINST TOTAL CAPACITY
    ####################################################################################################################
    '''
    # RE-USE common adding data into db function above to add a new row into db table
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

        except (mdb.Error, AttributeError), e:
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

        except (mdb.Error, AttributeError), e:
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
                print "Number of row returned from table after query = %s " % listed
                print rows
                return listed, rows
        except(mdb.Error, AttributeError), e:
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
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_table_capacity DB exception %d: %s" % (e.args[0], e.args[1])



    # ****************************************************************************************************************************************************************
    # users and tenants based - resources management- basic DB operations. Go here
    # ****************************************************************************************************************************************************************

    def get_newest_row_by_timestamp_userid_tenantid(self, table_name, rsv):
        '''
        This function is used to query a latest row from users utilization resources tables such as: users_util_compute_rm or users_util_network_rm
        get one row that store current availability of resources, where the selected row has the most recent timestamp
        and co-responding to user_id in given tenant_id (to guarantee the unique and latest oof returned row)
        :param table_name:
        :param rsv:
        :return:
        '''
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM (SELECT * FROM %s WHERE user_id='%s' and tenant_id='%s' ORDER BY modified_at DESC LIMIT 1) A GROUP BY modified_at, uuid" \
                      % (table_name, rsv['user_id'], rsv['tenant_id'])
                print sql
                self.cur.execute(sql)
                row = self.cur.fetchall()
                listed = self.cur.rowcount
                # for row in rows:   # for debug
                #     print row
                print " query all of %s table successfully" % table_name
                # Print out uuid
                # print rows[0]['uuid']
                return listed, row[0]
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_table_capacity DB exception %d: %s" % (e.args[0], e.args[1])


    def __add_row_by_userid_tenantid(self, table_name, user_id,tenant_id, row_dict):
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

        self.con
        self.cursor = self.con.cursor()
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
            # get last added id in a table
            added_uuid = self.cursor.lastrowid  # Returns the value generated for an AUTO_INCREMENT column TODO
            print added_uuid
            self.con.commit()
            if added > 0:

                print "Inserted new row successfully"
                return added, added_uuid
            else:
                print "Failed to add a new row into database table: %s" % table_name
                return added

        except (mdb.Error, AttributeError), e:
            print "resource_db.add_row_rs DB Exception %d : %s" % (e.args[0], e.args[1])
            self.con.rollback()





    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def _new_row_internal(self, table, INSERT, tenant_id=None, add_uuid=False, root_uuid=None, log=False):
        ''' Add one row into a table. It DOES NOT begin or end the transaction, so self.con.cursor must be created
        Attribute
            INSERT: dictionary with the key: value to insert
            table: table where to insert
            tenant_id: only useful for logs. If provided, logs will use this tenant_id
            add_uuid: if True, it will create an uuid key entry at INSERT if not provided
        It checks presence of uuid and add one automatically otherwise
        Return: (result, uuid) where result can be 0 if error, or 1 if ok
        '''

        if add_uuid:
            #create uuid if not provided
            if 'uuid' not in INSERT:
                uuid = INSERT['uuid'] = str(myUuid.uuid1()) # create_uuid
            else:
                uuid = str(INSERT['uuid'])
        else:
            uuid=None
        if add_uuid:
            #defining root_uuid if not provided
            if root_uuid is None:
                root_uuid = uuid
            #inserting new uuid
            cmd = "INSERT INTO uuids (uuid, root_uuid, used_at) VALUES ('%s','%s','%s')" % (uuid, root_uuid, table)
            print cmd
            self.cur.execute(cmd)
        #insertion
        cmd= "INSERT INTO " + table +" SET " + \
            ",".join(map(self.__tuple2db_format_set, INSERT.iteritems() ))
        print cmd
        self.cur.execute(cmd)
        nb_rows = self.cur.rowcount
        #inserting new log
        if nb_rows > 0 and log:
            if add_uuid: del INSERT['uuid']
            if uuid is None: uuid_k = uuid_v = ""
            else: uuid_k=",uuid"; uuid_v=",'" + str(uuid) + "'"
            if tenant_id is None: tenant_k = tenant_v = ""
            else: tenant_k=",nfvo_tenant_id"; tenant_v=",'" + str(tenant_id) + "'"
            cmd = "INSERT INTO logs (related,level%s%s,description) VALUES ('%s','debug'%s%s,\"new %s %s\")" \
                % (uuid_k, tenant_k, table, uuid_v, tenant_v, table[:-1], str(INSERT).replace('"','-'))
            print cmd
            self.cur.execute(cmd)
        return nb_rows, uuid


    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def new_row(self, table, INSERT, tenant_id=None, add_uuid=False, log=False):
        ''' Add one row into a table.
        Attribute
            INSERT: dictionary with the key: value to insert
            table: table where to insert
            tenant_id: only useful for logs. If provided, logs will use this tenant_id
            add_uuid: if True, it will create an uuid key entry at INSERT if not provided
        It checks presence of uuid and add one automatically otherwise
        Return: (result, uuid) where result can be 0 if error, or 1 if ok
        '''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    return self._new_row_internal(table, INSERT, tenant_id, add_uuid, None, log)

            except (mdb.Error, AttributeError), e:
                print "nfvo_db.new_row DB Exception %d: %s" % (e.args[0], e.args[1])
                # r,c = self.format_error(e)
                # if r!=-HTTP_Request_Timeout or retry_==1: return r,c


    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def __get_rows(self,table,uuid):
        self.cur.execute("SELECT * FROM " + str(table) +" where uuid='" + str(uuid) + "'")
        rows = self.cur.fetchall()
        return self.cur.rowcount, rows

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def get_rows(self,table,uuid):
        '''get row from a table based on uuid'''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    self.cur.execute("SELECT * FROM " + str(table) +" where uuid='" + str(uuid) + "'")
                    rows = self.cur.fetchall()
                    return self.cur.rowcount, rows
            except (mdb.Error, AttributeError), e:
                print "nfvo_db.get_rows DB Exception %d: %s" % (e.args[0], e.args[1])
                # r,c = self.format_error(e)
                # if r!=-HTTP_Request_Timeout or retry_==1: return r,c


    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def __update_rows(self, table, UPDATE, WHERE, log=False):
        ''' Update one or several rows into a table.
        Atributes
            UPDATE: dictionary with the key: value to change
            table: table where to update
            WHERE: dictionary of elements to update
        Return: (result, descriptive text) where result indicates the number of updated files, negative if error
        '''
                #gettting uuid
        uuid = WHERE['uuid'] if 'uuid' in WHERE else None

        cmd= "UPDATE " + table +" SET " + \
            ",".join(map(self.__tuple2db_format_set, UPDATE.iteritems() )) + \
            " WHERE " + " and ".join(map(self.__tuple2db_format_where, WHERE.iteritems() ))
        print cmd
        self.cur.execute(cmd)
        nb_rows = self.cur.rowcount
        if nb_rows > 0 and log:
            #inserting new log
            if uuid is None: uuid_k = uuid_v = ""
            else: uuid_k=",uuid"; uuid_v=",'" + str(uuid) + "'"
            cmd = "INSERT INTO logs (related,level%s,description) VALUES ('%s','debug'%s,\"updating %d entry %s\")" \
                % (uuid_k, table, uuid_v, nb_rows, (str(UPDATE)).replace('"','-')  )
            print cmd
            self.cur.execute(cmd)
        return nb_rows, "%d updated from %s" % (nb_rows, table[:-1])

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
    def update_rows(self, table, UPDATE, WHERE, log=False):
        ''' Update one or several rows into a table.
        Atributes
            UPDATE: dictionary with the key: value to change
            table: table where to update
            WHERE: dictionary of elements to update
        Return: (result, descriptive text) where result indicates the number of updated files
        '''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    return 1, self.__update_rows(table, UPDATE, WHERE, log)

            except (mdb.Error, AttributeError), e:
                print "nfvo_db.update_rows DB Exception %d: %s" % (e.args[0], e.args[1])
                # r,c = self.format_error(e)

                # if r!=-HTTP_Request_Timeout or retry_==1: return r,c

    def get_table(self, **sql_dict):
        ''' Obtain rows from a table.
        Attribute sql_dir: dictionary with the following key: value
            'SELECT': (list or tuple of fields to retrieve) (by default all)
            'FROM': string of table name (Mandatory)
            'WHERE': dict of key:values, translated to key=value AND ... (Optional)
            'WHERE_NOT': dict of key:values, translated to key<>value AND ... (Optional)
            'WHERE_NOTNULL': (list or tuple of items that must not be null in a where ... (Optional)
            'LIMIT': limit of number of rows (Optional)
        Return: a list with dictionaries at each row
        '''
        #print sql_dict
        select_= "SELECT " + ("*" if 'SELECT' not in sql_dict else ",".join(map(str,sql_dict['SELECT'])) )
        #print 'select_', select_
        from_  = "FROM " + str(sql_dict['FROM'])
        #print 'from_', from_
        if 'WHERE' in sql_dict and len(sql_dict['WHERE']) > 0:
            w=sql_dict['WHERE']
            where_ = "WHERE " + " AND ".join(map(self.__tuple2db_format_where, w.iteritems() ))
        else: where_ = ""
        if 'WHERE_NOT' in sql_dict and len(sql_dict['WHERE_NOT']) > 0:
            w=sql_dict['WHERE_NOT']
            where_2 = " AND ".join(map(self.__tuple2db_format_where_not, w.iteritems() ) )
            if len(where_)==0:   where_ = "WHERE " + where_2
            else:                where_ = where_ + " AND " + where_2
        if 'WHERE_NOTNULL' in sql_dict and len(sql_dict['WHERE_NOTNULL']) > 0:
            w=sql_dict['WHERE_NOTNULL']
            where_2 = " AND ".join(map( lambda x: str(x) + " is not Null",  w) )
            if len(where_)==0:   where_ = "WHERE " + where_2
            else:                where_ = where_ + " AND " + where_2
        #print 'where_', where_
        limit_ = "LIMIT " + str(sql_dict['LIMIT']) if 'LIMIT' in sql_dict else ""
        #print 'limit_', limit_
        cmd =  " ".join( (select_, from_, where_, limit_) )
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    print cmd
                    self.cur.execute(cmd)

                    rows = self.cur.fetchall()

                    return self.cur.rowcount, rows
            except (mdb.Error, AttributeError), e:
                print "nfvo_db.get_table DB Exception %d: %s" % (e.args[0], e.args[1])
                # r,c = self.format_error(e)
                # if r!=-HTTP_Request_Timeout or retry_==1: return r,c


    ####################################################################################################################
    # helper functions so far (before intergration with playnetMANO v2)
    ####################################################################################################################

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************

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
    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
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

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
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

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
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

    # **************************
    # Reused function from PlaynetMano V2 - nfvo_db.py file
    # **************************
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
    a = db.connect_db(host="116.89.184.43", user="root", passwd="", database="mano_db")
    update = {'total_vcpus_allocated': 55, 'total_vmem_allocated': 66}
    where = {'uuid': 20}
    # cursor = db.con.cursor()
    #cursor = db.con.cursor(MySQLdb.cursors.DictCursor)
    #db.add_row_rs('reservation', data) #sh_compute.vmem_op_stats())
    #db.add_row_rs('vcpu_capacity', vcpu) #sh_compute.vmem_op_stats())

    #db.delete_row_by_rsv_id(table_name,'12345')
    # db.update_row_timestamp_by_rsv_id(table_name,'12345','2016-04-14 11:11:11','2016-04-15 22:22:22')
    #db.get_rsv_by_id('reservation','12345')
    #db.update_row_capacity_by_uuid('vmem_capacity', 2, vmem_capa)
    dat_table = db.update_rows('tenants_utilization_compute_rm', update, where, log=False )
    print dat_table
    # list_rsv = db.get_rsv_by_status('ACTIVE')
    # for rsv in list_rsv:
    #     print rsv
    #     start_time = rsv['start_time']
    #     print start_time
