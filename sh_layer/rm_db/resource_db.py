import MySQLdb.cursors
import MySQLdb as mdb
import uuid as myUuid
import json
import sys

from sh_layer.global_info import *
from sh_layer.rm_db.utils_db import *

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
        'number_vnfs': '1',
        'ns_id': 'ffbc3c72aa9f44769f3430093c59c457',
        'status': 'ACTIVE',
        'summary': 'reservation testing'
        }
flavor_dict = {'flavor_id': 2, 'name': 'm.medium', 'ram': 1024, 'disk': 2, 'vcpu': 2}

image_dict = {'image_id': '19f7025b-b78a-4bf0-bc37-0cba68e16b10', 'name': 'ubuntu_01'}

class resource_db(utils_db):

    ####################################################################################################################
    #connect and disconnect DB
    ####################################################################################################################
    def __init__(self):
        utils_db.__init__(self)
        return

    def connect(self, host=None, user=None, passwd=None, database=None):
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


    ####################################################################################################################
    #CRUD DB operations for reservation
    ####################################################################################################################

    # common adding data to DB table function
    def add_row_rs(self, table_name, row_dict):
        '''

        :param table_name:
        :param row_dict:
        :return:
        '''

        # self.con
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
            added_uuid = self.cursor.lastrowid  # Returns the value generated for an AUTO_INCREMENT column
            # TODO (rickyhai) using existing new_row() in playnetmano if using UUID instead of ID (auto increment)
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
            print "resource_db.replace_row_by_uuid_composite DB Exception %d : %s" % (e.args[0], e.args[1])

    # vnfTid (vnf_id) DB operations that related to reservation, go here!

    ###################################################

    # call this function when vnf(s) are/is created successfully in VIM and vnftid should be updated accordingly
    #  to associated table 'rsv_vnf_rm'
    def add_vnfTid_by_rsv_id(self, table_name, reservation_id, vnf_id):
        '''
        to update list of vnf_id from a reservation to table 'rsv_vnf_rm'
        :param talble_name: name of table
        :param reservation_id: esxting reservation in DB
        :param vnf_id = instance_id, in this case this field need to be updated after starting time has been
        triggered, reservation status "Running" and vnf_id(s) has been instantiated
        :return: result and vnf_id
        '''
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "INSERT INTO %s SET vnf_id='%s', reservation_id ='%s'" % (table_name,
                                                                                 vnf_id, reservation_id)
                print sql
                self.cur.execute(sql)
                added = self.cur.rowcount
                print "added vnf_id: %s successfully for %s reservation" % (vnf_id, added)
            return added, vnf_id
        except (mdb.Error, AttributeError), e:
            print "resource_db.update_vnfTid_by_rsv_id DB Exception %d : %s" % (e.args[0], e.args[1])

    # call this function when user would like to update vnfTid in a reservation
    # vnfTid should be updated accordingly
    # to associated table 'rsv_vnf_rm'. To do this, consider the following actions:
    # 1. stop vnf and delete vnf
    # 2. cache deleted vnfTid
    # 3. bring up new vnf and get new vnfTid
    # 4. replace new vnfTid with old vnfTid that regrading to a reservation
    def update_vnfTid_by_rsv_id(self, table_name, reservation_id, vnf_id, new_vnf_id):
        '''
        to update list of vnf_id from a reservation to table 'rsv_vnf_rm'
        :param talble_name: name of table
        :param reservation_id: esxting reservation in DB
        :param vnf_id = instance_id, in this case this field need to be updated after starting time has been
        triggered, reservation status "Running" and vnf_id(s) has been instantiated
        :return: result and vnf_id
        '''
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "UPDATE %s SET vnf_id='%s' WHERE reservation_id = '%s' AND vnf_id = '%s' "\
                      % (table_name, new_vnf_id, reservation_id, vnf_id)
                print sql
                self.cur.execute(sql)
                updated = self.cur.rowcount
                print "Updated vnf_id: %s successfully for %s reservation" % (vnf_id, updated)
            return updated, vnf_id
        except (mdb.Error, AttributeError), e:
            print "resource_db.update_vnfTid_by_rsv_id DB Exception %d : %s" % (e.args[0], e.args[1])

    # vnfdId DB operations, go here

    ###################################################

    def _get_vnfdId_by_rsv_id(self, reservation_id, vnfdId):
        '''
        check in vnfdid_rsv_rm table if (reservation_id, vnfdId) is already present
        :param reservation_id:
        :param vnfdId:
        :return:
        '''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    self.cur.execute("SELECT * FROM vnfdid_rsv_rm where reservation_id= '%s' AND vnfdId='%s'"
                                     % (reservation_id, vnfdId))
                    row = self.cur.fetchall()
                    return self.cur.rowcount, row
            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_vnfdId_by_rsv_id DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_ == 1:
                    return r,c

    def get_vnfdId_by_rsv_id(self, reservation_id, vnfdId):
        return _get_vnfdId_by_rsv_id(self, reservation_id, vnfdId)

    # this function is called only after a reservation is created to track vnfdId(s) with co-responding reservation(s)
    # n-n relationship between vnf descriptor table and reservation table
    def add_vnfdId_by_rsv_id(self, table_name, reservation_id, vnfdId):
        '''
        to update list of vnf_id from a reservation to table 'sv_vnf_auth_rm'
        :param talble_name:
        :param reservation_id: esxting reservation in DB
        :param vnf_id = instance_id, in this case this field need to be updated after starting time has been
        triggered, reservation status "Running" and vnf_id(s) has been instantiated
        :return: result and vnf_id
        '''
        # are existing in the same row in DB table (not duplicated row)
        result, row = self._get_vnfdId_by_rsv_id(reservation_id, vnfdId)
        if result < 0:
            nlog.error("vnfdId: %s for reservation_id %s is already present in DB" % (vnfdId, reservation_id))
            return False
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "INSERT INTO %s SET vnfdId='%s',reservation_id='%s'" % (table_name,
                                                                                 vnfdId, reservation_id)
                print sql
                self.cur.execute(sql)
                added = self.cur.rowcount
                print "resource_db.add_vnfdId_by_rsv_id() : added vnfdId: %s and reservation_id: %s into " \
                      "vnfdid_rsv_info table successfully " % (vnfdId, added)
            return added, reservation_id, vnfdId
        except (mdb.Error, AttributeError), e:
            print "resource_db.add_vnfdId_by_rsv_id DB Exception %d : %s" % (e.args[0], e.args[1])

    # call this function when updating vnfdId for a reservation by reservation_id
    # vnfdId should be updated accordingly to associated table 'vnfdid_rsv_info'
    # TODO (rickyhai) update behaviors when reservation status = 'ACTIVE' and 'INACTIVE' ?
    def update_vnfdId_by_rsv_id(self, table_name, reservation_id, vnfdId):
        '''
        to update list of vnf_id from a reservation to table 'sv_vnf_auth_rm'
        :param talble_name:
        :param reservation_id: esxting reservation in DB
        :param vnf_id = instance_id, in this case this field need to be updated after starting time has been
        triggered, reservation status "Running" and vnf_id(s) has been instantiated
        :return: result and vnf_id
        '''
        try:
            with self.con:
                self.cur= self.con.cursor()
                sql = "UPDATE %s SET vnf_id='%s' WHERE reservation_id = '%s'" % (table_name,
                                                                                 vnfdId, reservation_id)
                print sql
                self.cur.execute(sql)
                updated = self.cur.rowcount
                print "Updated vnf_id: %s successfully for %s reservation" % (vnfdId, updated)
            return updated, vnfdId
        except (mdb.Error, AttributeError), e:
            print "resource_db.update_vnfdId_by_rsv_id DB Exception %d : %s" % (e.args[0], e.args[1])


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


    def get_rsv_by_status(self, status):
        '''
        Query reservation by a status
        :param status:
        :return:
        '''

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



    # Quota Management DB operations, go here
    ######################################################
    def replace_row_by_uuid_composite(self, table_name, uuid, new_values_dict):
        '''
        Removes the old one (based on uuid) and adds the new values for resource capacity tables (vcpu, vmem,vdisk, network etc...)
        Attribute
        :param table_name: table where to insert
        :param uuid: input uuid that using to del
        :param new_values_dict: is a dictionary with format as below (included new 'uuid' field)
            vcpu={'uuid': 13,"cpu_total": 15, "vcpu_total" : 20,"vcpu_used": 10, "cpu_available": 8, "vcpu_available":65}
        :return: (delete, new_uuid)
        '''
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
            print "resource_db.replace_row_by_uuid_composite DB Exception %d : %s" % (e.args[0], e.args[1])

    # update a specific resource usage in a given project/tenant by name
    def update_resource_usage_by_name_for_tenant(self, tenant_id, resource, actual_usage):
        if 'in_use' not in actual_usage:
            nlog.error("ERROR: resource usage format, 'in_use' is not present")
        # actual resource usage could be (1) or (2):
        # (1) to update DB after manually calculating resource usage ( with per resource request)
        # (1) actual_usage = {'in_use': actual_usage['in_use'], 'reserved': actual_usage['reserved']}
        #
        # (2) to update DB after resource usage sync from VIM (until_refresh flag =True)
        # (2) actual_usage = {'in_use': actual_usage['in_use']}
        where_info = {'project_id': tenant_id, 'resource': resource}
        result, _ = utils_db.update_rows('resource_usage_rm', UPDATE=actual_usage, WHERE=where_info, log=True)
        if result <= 0:
            nlog.error("Error : DB update (resource =%s, project ID =%s actual resource usage = %s)", resource,
                       tenant_id, actual_usage)
            return False, None
        else:
            nlog.debug("Success : Update resource information into resource_usage_rm table")

        return result

    # update resource usage by uuid or name (default is uuid if no --> name)
    def update_resource_usage_by_uuid_name(self, table, uuid_name):
        return

    # update resource usage by uuid only
    def update_resource_usage_by_uuid(self, table, uuid):
        return

    # quota-hard limit
    #####################################################

    def create_all_quotas_for_tenant(self, tenant_id, quota):
        return

    def create_quota_for_resource_tenant(self, tenant_id, resource, resource_quota):
        return

    def update_quota_for_resource_tenant(self, tenant_id, resource, update_quota):
        return

    def update_all_quotas_for_tenant(self, tenant_id, update_quota):
        return

    def get_quota_for_tenant_by_resource(self, tenant_id, resource):
        return

    def get_all_quotas_for_tenant(self, tenant_id):
        return

    def delete_quota_for_tenant(self, tenant_id):
        return

    def delete_quota_for_resource_tenant(self, tenant_id, resource):
        return











    def update_tenants_utilization_compute_rm_table(self, uuid, action):
        # get vnf_using_cnt
        result, content = self.get_table_by_uuid_name("tenants_utilization_compute_rm", uuid, error_item_text=None, allow_serveral=False)
        if result <= 0:
            nlog.error("Error : Can't get tenants_utilization_compute_rm table")
            return False, None
        else:
            vnfd_using_cnt = content['vnfdUsingCnt']
            nlog.debug("vnfd using cnt = %d", vnfd_using_cnt)

        if action == 'ADD':            vnfd_using_cnt = vnfd_using_cnt + 1
        elif action == 'DELETE':       vnfd_using_cnt = vnfd_using_cnt - 1
        else:                          return False, None

        # update vnf_using_cnt
        update_info = {'vnfdUsingCnt': vnfd_using_cnt}
        result, _ = self.update_rows("vnfd_using_info", UPDATE=update_info, WHERE={'uuid':uuid}, log=True)
        if result < 0:
            nlog.error("Error : Can't table(vnfd_using_info) update")
            return False, None

        return True, vnfd_using_cnt

    def delete_row_by_uuid_composite(self, table_name, uuid):
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
            print "resource_db.replace_row_by_uuid_composite DB Exception %d : %s" % (e.args[0], e.args[1])

    def get_row_by_uuid_composite(self, table_name, uuid):
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM %s WHERE uuid = '%s'" % (table_name, uuid)
                self.cur.execute(sql)
                rows = self.cur.fetchone()
                listed = self.cur.rowcount
                print " Query table %s with uuid %s successfully" % (table_name, uuid)
                print "Number of row returned from table after query = %s " % listed
                print rows
                return listed, rows
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_row_by_uuid_composite DB exception %d: %s" % (e.args[0], e.args[1])

    def get_all_rows_for_table_composite(self, table_name):
        #self.con = self.reload_connect_db()
        try:
            with self.con:
                self.cur = self.con.cursor(MySQLdb.cursors.DictCursor)
                sql = "SELECT * FROM %s" % table_name
                self.cur.execute(sql)
                rows = self.cur.fetchall()
                listed = self.cur.rowcount
                # for row in rows:
                #     print row
                print " query all of %s table successfully" % table_name
                return listed, rows
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_all_rows_for_table_composite DB exception %d: %s" % (e.args[0], e.args[1])










    # ****************************************************************************************************************************************************************
    # users and tenants based - resources management- basic DB operations. Go here
    # ****************************************************************************************************************************************************************

    def get_newest_row_by_timestamp_userid_tenantid(self, table_name, user_id, tenant_id):
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
                      % (table_name, user_id, tenant_id)
                print sql
                self.cur.execute(sql)
                row = self.cur.fetchall()
                listed = self.cur.rowcount
                # for row in rows:   # for debug
                #     print row
                print " Query latest row in %s table with user-id: %s and tenant-id: %s successfully" % (table_name, user_id, tenant_id)
                # Print out uuid
                # print rows[0]['uuid']
                return listed, row
        except(mdb.Error, AttributeError), e:
            print "resource_db.get_all_rows_for_table_composite DB exception %d: %s" % (e.args[0], e.args[1])


    def __add_row_by_userid_tenantid(self, table_name, user_id, tenant_id, row_dict):
        ''' add_row_resources could be used like global adding function for adding any data with dict/json format to DB
        for example:
            if Add a new reservation to reservation table
            input parameters:
                table_name: name of table in mySQL DB
                rowdict: dictionary that include attributes regarding to kind of resource
        '''

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


    ####################################################################################################################
    # main function for testing above code
    ####################################################################################################################

if __name__ == '__main__':
    db = resource_db()
    a = db.connect(host="116.89.184.43", user="root", passwd="", database="mano_db")
    update = {'total_vcpus_allocated': 55, 'total_vmem_allocated': 66}
    where = {'uuid': 20}
    # cursor = db.con.cursor()
    #cursor = db.con.cursor(MySQLdb.cursors.DictCursor)
    #db.add_row_rs('reservation', data) #sh_compute.vmem_op_stats())
    #db.add_row_rs('vcpu_capacity', vcpu) #sh_compute.vmem_op_stats())

    #db.delete_row_by_rsv_id(table_name,'12345')
    # db.update_row_timestamp_by_rsv_id(table_name,'12345','2016-04-14 11:11:11','2016-04-15 22:22:22')
    #db.get_rsv_by_id('reservation','12345')
    #db.replace_row_by_uuid_composite('vmem_capacity', 2, vmem_capa)
    dat_table = db.update_vnfTid_by_rsv_id('rsv_vnf_rm', '23762sbdhgwshdg', 'sjhdgsjdh121' , 'haiupdated')
    print dat_table
    # list_rsv = db.get_rsv_by_status('ACTIVE')
    # for rsv in list_rsv:
    #     print rsv
    #     start_time = rsv['start_time']
    #     print start_time

