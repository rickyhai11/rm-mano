import MySQLdb.cursors
import sys
import collections

# from sh_layer.global_info import *
# from sh_layer.common.consts import *
from sh_layer.rm_db.utils_db import *
from sh_layer.common.utils_rm import *

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

    # Reservation db functions go here
    #####################################################
    # common adding data to DB table function
    def add_row_rs(self, table_name, row_dict):
        '''
        common adding data to DB table function
        :param table_name:
        :param row_dict:
        :return:
        '''

        # self.cursor=self.con.cursor()
        self.cursor.execute("describe %s" % table_name)
        self.allowed_keys = set(row[0] for row in self.cursor.fetchall())
        print self.allowed_keys
        self.keys = self.allowed_keys.intersection(row_dict)
        print self.keys

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

    # to delete any row from any db tables that associated with reservation ID
    # hence, keep table as argument
    def delete_row_by_rsv_id(self, table, reservation_id):
        '''
        Delete a reservation from database with reservation ID from reservation table
        :param table:
        :return:
        '''
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur= self.con.cursor()
                    sql = "DELETE FROM %s WHERE reservation_id = '%s'" % (table, reservation_id)
                    print sql
                    self.cur.execute(sql)
                    deleted = self.cur.rowcount
                    print "Delete successfully a reservation: %s " % deleted
                return deleted
            except (mdb.Error, AttributeError), e:
                print "resource_db.delete_resource_by_name_uuid_for_tenant DB Exception %d : %s" % (e.argrs[0], e.args[1])

    # delete a reservation with rsv_id and project_id
    # provide project_id here to be easier when calculate resource usage for a given project
    def delete_row_by_rsv_id_for_project(self, project_id, reservation_id):
        '''
        Delete a reservation from database with reservation ID and project ID
        :param table:
        :return:
        '''
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur= self.con.cursor()
                    sql = "DELETE FROM reservation_rm WHERE reservation_id ='%s' and project_id ='%s'" \
                          % (reservation_id, project_id)
                    print sql
                    self.cur.execute(sql)
                    deleted = self.cur.rowcount
                    print "Delete successfully a reservation: %s " % deleted
                return deleted
            except (mdb.Error, AttributeError), e:
                print "resource_db.delete_resource_by_name_uuid_for_tenant DB Exception %d : %s" % (e.argrs[0], e.args[1])

    def update_row_timestamp_by_rsv_id(self, reservation_id, start_time, end_time):
        '''
        this function is to update start_time and end_time of a reservation from reservation table
        :param self:
        :param reservation_id:
        :param start_time:
        :param end_time:
        :return:
        '''
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur= self.con.cursor()
                    sql = "UPDATE reservation SET start_time='%s',end_time='%s' WHERE reservation_id = '%s'" \
                          % (start_time, end_time, reservation_id)
                    print sql
                    self.cur.execute(sql)
                    updated = self.cur.rowcount
                    print "Update successfully a reservation: %s " % updated
                return updated
            except (mdb.Error, AttributeError), e:
                print "resource_db.update_row DB Exception %d : %s" % (e.args[0], e.args[1])

    # unused code
    # def replace_reservation_by_rsv_id(self, table_name, reservation_id, new_values_dict):
    #     '''
    #     Removes the old (based on reservation_id) and adds a new reservation with new values (new reservation is created as well)
    #     Attribute
    #     :param table_name: table where to insert
    #     :param old_reservation:
    #     :param new_values_dict: is a dictionary with format as below
    #     :return: (delete, new_reservation_id)
    #     '''
    #     for retry_ in range(0, 2):
    #         try:
    #             with self.con:
    #                 self.cur= self.con.cursor()
    #                 sql = "DELETE FROM %s WHERE reservation_id= '%s'" % (table_name, reservation_id)
    #                 print sql
    #                 self.cur.execute(sql)
    #                 deleted = self.cur.rowcount
    #                 #print deleted
    #                 if deleted > 0 and new_values_dict:
    #                     print "Deleted successfully next step --> adding a new reservation for new values"
    #                     self.add_row_rs(table_name, new_values_dict)
    #                     print "Updated new values into %s table successfully" % table_name
    #                     new_reservation_id = new_values_dict['reservation_id']
    #
    #                     return deleted, new_reservation_id
    #
    #                 else:
    #                     print "Failed to delete previous values in db ######'%s row has been deleted'###### OR " \
    #                           "###### 'reservation_id': %s was not existing " \
    #                           "in %s table ######" % (deleted, reservation_id, table_name)
    #
    #         except (mdb.Error, AttributeError), e:
    #             print "resource_db.replace_row_by_uuid_composite DB Exception %d : %s" % (e.args[0], e.args[1])

    # update reservation for a given project
    def update_reservation_for_project(self, project_id, reservation_id, new_values_dict):
        '''
        update reservation with reservation id and project id
        :param project_id: project where reservation is created
        :param reservation_id: reservation id
        :param new_values_dict: is a dictionary with key/value for update fields
        :return:
        '''
        where = {'project_id': project_id, 'reservation_id': reservation_id}
        _, result = self.update_rows('quota_rm', UPDATE=new_values_dict, WHERE=where, log=False)

        # result is tuple and result[0] to pickup number of updated rows
        if result[0] <= 0:
            # debug only
            print "resource_db.update_reservation_for_project:  Failed to update reservation with (update values: '%s' " \
                  "and tenant ID: '%s'" % (new_values_dict, project_id)

            nlog.error("Error : can't update reservation for (update values ='%s' and tenant ID: '%s')",
                       new_values_dict, project_id)
            return False, None
        else:
            # debug only
            print "resource_db.update_reservation_for_project:  Sucessful to update reservation with (update values: '%s' " \
                  "and tenant ID: '%s'" % (new_values_dict, project_id)
            nlog.info("Success : update reservation for a tenant/project ID '%s' and update values: '%s'", project_id, new_values_dict)
            return True, result[0]





    # vnfTid (vnf_id) DB operations that related to reservation, go here!
    ###################################################

    # call this function when vnf(s) are/is created successfully in VIM and vnftid should be updated accordingly
    #  to associated table 'rsv_vnf_rm'
    def add_vnf_id_by_rsv_id(self, table_name, reservation_id, vnf_id):
        '''
        to add list of vnf_id from a reservation to table 'rsv_vnf_rm'
        :param talble name: name of table
        :param reservation_id: existing reservation in DB
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
                sql = "UPDATE %s SET vnf_id='%s' WHERE reservation_id = '%s' AND vnf_id = '%s' " \
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

    def _get_vnfd_id_by_rsv_id(self, reservation_id, vnfdId):
        '''
        using to get a specific vnfd_id that associated with a reservation id
        using: to check in vnfdid_rsv_rm table if (reservation_id, vnfdId) is already present
        :param reservation_id:
        :param vnfdId:
        :return: result count and row
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
                nlog.error("nfvo_db.get_vnfd_id_by_rsv_id DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_ == 1:
                    return r,c

    def get_vnfd_id_by_rsv_id(self, reservation_id, vnfd_id):
        '''
        using to get a specific vnfd_id that associated with a reservation id
        using: to check in vnfdid_rsv_rm table if (reservation_id, vnfdId) is already present
        :param reservation_id:
        :param vnfd_id:
        :return: result count and row
        '''
        return self._get_vnfd_id_by_rsv_id(reservation_id, vnfd_id)

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
        result, row = self._get_vnfd_id_by_rsv_id(reservation_id, vnfdId)
        if result < 0:
            nlog.error("vnfdId: %s for reservation_id %s is already present in DB" % (vnfdId, reservation_id))
            return False
        for retry_ in range(0,2):
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
        to update list of vnf_id from a reservation to table 'rsv_vnf_auth_rm'
        :param talble_name:
        :param reservation_id: esxting reservation in DB
        :param vnf_id = instance_id, in this case this field need to be updated after starting time has been
        triggered, reservation status "Running" and vnf_id(s) has been instantiated
        :return: result and vnf_id
        '''
        for retry_ in range(0,2):
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

    # get a specific reservation in a given project by reservation ID
    # don't need to use project_id in query condition as reservation_id is unique in system
    def get_rsv_by_id(self, reservation_id):
        '''
        this function is to query a specific reservation in a given project with reservation_id
        :param reservation_id:
        :return: listed (rows count),rows (reservation data)
        '''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur= self.con.cursor(MySQLdb.cursors.DictCursor)
                    sql = "SELECT * FROM reservation WHERE reservation_id= '%s'" % reservation_id
                    self.cur.execute(sql)
                    rows = self.cur.fetchone()
                    listed = self.cur.rowcount
                    print "query reservation with id %s successfully" % reservation_id
                    #print listed
                    print rows['reservation_id']
                    return listed, rows
            except(mdb.Error, AttributeError), e:
                print "resource_db.get_rsv_by_id DB exception %d: %s" % (e.args[0], e.args[1])
                return False, None

    # get list of reservations for a given project
    def get_reservation_for_project(self, project_id ):
        '''
        get list of reservations for a given project
        :param project_id:
        :return: result, list_reservations
        '''
        result, list_reservations = self._get_resource_for_tenant_from_db('reservation', project_id)
        if result <= 0:
            nlog.error("Error : get list of reservations from DB  (project ID =%s, )", project_id)
            return False, None
        else:
            nlog.info("Success : get list of reservations for project ID '%s'", project_id)

        return result, list_reservations

    # get list of reservations by status
    def get_rsv_by_status(self, status):
        '''
        Query list of reservations by a status
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

    # identify reservation is expired , then deleted reservation record in db and update "reserved" columns
    # which regard to resources in resource usage table
    def reservation_expire(self, rsv_id):
        #TODO (ricky) implement later in next phase
        return rsv_id


    # Quota Management DB operations, go here
    #####################################################
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
                # print sql
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

    # Create a resource usage by name for a given tenant
    # (using with reservation operations probably, for instance: after create reservation --> call this )
    def create_resource_usage_by_name_for_tenant(self, tenant_id, resource, in_use, reserved,  util_refresh=False):
        '''
        Create resource usage for a specific resource in a given tenant/project
        :param tenant_id:
        :param resource: : resource name
        :param in_use: value of in_use corresponding resource;
        :param reserved: value of reserved corresponding resource;
        :param until_refresh: False- not need to refresh resource usage yet (in mysql until_refresh =0)
        True: need to refresh resource usage (in mysql until_refresh =1)
        :return: resource usage that is created successfully
        '''
        # TODO (rickyhai) need to implement when we need to refresh resource usage (util_refresh=True) ?

        # First check if there are any duplicate rows with corresponding project id and resource in db
        nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=tenant_id,
                                                             uuid_name=resource, error_item_text=None,
                                                             allow_serveral=True)
        # print nb_rows
        # if there are no duplicates in db
        if nb_rows == 0:
            # create + store resource usage in DB for a specific resource in a given tenant
            usage_sync = {'project_id': tenant_id, 'resource': resource, 'in_use': in_use, 'reserved': reserved, 'util_refresh': util_refresh}
            r, uuid = self.new_row('resource_usage_rm', INSERT=usage_sync, add_uuid=True, log=False)
            if r > 0:
                # debug only
                print ("INFO: Successful to add a specific resource usage (resource name: '%s' and project ID '%s') "
                       "into resource usage table" % (resource, tenant_id))
                nlog.info("INFO: Successful to add a specific resource usage (resource name: '%s' and project ID '%s') "
                          "into resource usage table", resource, tenant_id)
                return r, usage_sync
            else:
                print ("ERROR: Failed to add a specific resource usage (resource name: '%s' and project ID '%s') "
                       "into resource usage table" % (resource, tenant_id))
                nlog.error("ERROR: Failed to add a specific resource usage (resource name: '%s' and project ID '%s') "
                          "into resource usage table", resource, tenant_id)
                return False, None
        # if number of rows > 0 --> row is already present
        elif nb_rows > 0:
            print ("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is already present"
                       "in resource usage table" % (resource, tenant_id))
            nlog.error("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is already present"
                          "in resource usage table", resource, tenant_id)
            return False, None
        # if number of rows is not integer
        else:
            print ("ERROR: Failed to check the presence of a specific resource(resource name: '%s' and project ID '%s') "
                       "from resource usage table" % (resource, tenant_id))
            nlog.error("ERROR: Failed to check the presence of a specific resource(resource name: '%s' and project ID '%s') "
                          "from resource usage table", resource, tenant_id)
            return False, None

    # # update a specific resource usage in a given project/tenant by name + using dict actual_usage as input data
    # def update_resource_usage_by_name(self, tenant_id, resource, actual_usage):
    #     if 'in_use' not in actual_usage:
    #         # debug only
    #         print "ERROR: Input data format: '%s' is incorrect, 'in_use' is not present" % actual_usage
    #         nlog.error("ERROR: input data format: '%s' is incorrect, 'in_use' is not present", actual_usage)
    #     else:
    #         # actual resource usage could be (1) or (2):
    #         # (1) to update DB after manually calculating resource usage ( with per resource request)
    #         # (1) actual_usage = {'in_use': actual_usage['in_use'], 'reserved': actual_usage['reserved']}
    #         #
    #         # (2) to update DB after resource usage sync from VIM (until_refresh flag =True)
    #         # (2) actual_usage = {'in_use': actual_usage['in_use']}
    #         where_info = {'project_id': tenant_id, 'resource': resource}
    #         _, result = self.update_rows('resource_usage_rm', UPDATE=actual_usage, WHERE=where_info, log=True)
    #         if result <= 0:
    #             nlog.error("Error : DB update (resource =%s, project ID =%s actual resource usage = %s)", resource,
    #                        tenant_id, actual_usage)
    #             return False, None
    #         else:
    #             nlog.info("Success : Update resource information into resource_usage_rm table")
    #
    #         return result[0]

    # update a specific resource usage in a given project/tenant by name + using particular value as input data
    # This function is invoked for handle api request in case user would like to update
    # a specific resource usage intentionally from explicit project
    def update_resource_usage_by_name_for_tenant(self, tenant_id, resource, in_use, reserved,
                                                 until_refresh=False):
        '''
        update a specific resource by name for a given tenant
        :param tenant_id:
        :param resource: name
        :param in_use: value
        :param reserved: value
        :param until_refresh: False or True: resource need to be refreshed/synced or not
        :return:
        '''
        # use cases (1) or (2):
        # (1) to update DB after manually calculating resource usage ( with per resource request)
        # (2) to update DB after resource usage sync from VIM (util_refresh flag =True)
        #
        # First check if there are any duplicate rows with corresponding project id and resource in db
        nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=tenant_id,
                                                             uuid_name=resource, error_item_text=None,
                                                             allow_serveral=True)
        # print nb_rows
        # if there is no record in db regarding to that resource and tenant
        if nb_rows == 0:
            # passing number of row = 0 to trigger create new record for correspond resource
            print ("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present"
                       "in resource usage table" % (resource, tenant_id))
            nlog.error("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present"
                          "in resource usage table", resource, tenant_id)
            return nb_rows

        # if number of rows > 1 --> row is already present and trigger update operation
        elif nb_rows == 1:
            where_info = {'project_id': tenant_id, 'resource': resource}
            update_usage = {'in_use': in_use, 'reserved': reserved, 'until_refresh': until_refresh}
            _, result = self.update_rows('resource_usage_rm', UPDATE=update_usage, WHERE=where_info, log=True)

            # result[0] = number of rows have been updated
            if result[0] > 0:
                nlog.info("Success : Update resource information into resource_usage_rm table")
                return nb_rows
            else:
                nlog.error("Error: Failed to update resource usage (resource =%s, project ID =%s actual resource usage = %s)",
                           resource, tenant_id, update_usage)
                # return False, None

        # if number of rows is not integer
        else:
            print ("ERROR: Failed to check presence of a specific resource (resource name: '%s' and project ID '%s') "
                       "from resource usage table" % (resource, tenant_id))
            nlog.error("ERROR: Failed to check presence of a specific resource (resource name: '%s' and project ID '%s') "
                          "from resource usage table", resource, tenant_id)
            # return False, None

    ######################################################
    # internal function which is called internally for handling resource management operations
    # Resource usage calculation
    # update a specific resource usage in a given project by name + using particular value as input data
    #

    def in_use_record_update(self, project_id, resource, in_use, action):
        '''
        to update 'in_use' value for a specific resource in resource usage table against action = (ADD, UPDATE, DELETE)
        if action == ADD or UPDATE --> increase in_use
        if action == DELETE --> decrease in_use
        :param project_id:
        :param resource: name
        :param in_use: value
        :param action: (ADD, UPDATE, DELETE) --> to decide whether in_use resource is increased or decreased
        :return:
        '''

        # First checks that the state of records is what the thread previously knew to exist.
        # The UPDATE statement will include a WHERE condition that will ensure that the rows are only updated
        # in the table IF the current row values are what the thread thought they were
        # when previously reading the rows with the SELECT statement. The thread will check the number of rows
        # affected by the UPDATE statement.
        # If the number of rows affected is 0, then a randomized exponential backoff loop will be hit
        # and the process of reading and
        # then UPDATE ing with the WHERE condition will repeat until a pre-defined number of tries has been attempted.

        # use cases (1) or (2):
        # (1) to update DB after calculating reserved/allocated resource ( with per resource request)
        # (2) to update DB after resource usage sync from VIM (util_refresh flag =True)
        #
        # First get current resource usage and
        # check if there are any duplicate rows with corresponding project id and resource in db
        nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=project_id,
                                                                    uuid_name=resource, error_item_text=None,
                                                                    allow_serveral=True)

        # if there is no record in db regarding to that resource and tenant
        if nb_rows == 0:
            # passing number of row = 0 to trigger create new record for correspond resource
            print ("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present in db"
                   % (resource, project_id))
            nlog.error("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present in db",
                       resource, project_id)
            return False, nb_rows

        # if number of rows > 1 --> row is already present and trigger update operation
        elif nb_rows == 1:
            # define max_attempts and number_attempts
            max_attempts = 10
            num_attempts = 0

            # get current usage
            current_in_use = usage['in_use']

            while num_attempts < max_attempts:
                # resource calculation (increased or decreased) that depend on action value (ADD or DELETE or UPDATE)
                updated_in_use = resource_calculation(current_value=current_in_use, acquired_value=in_use, action=action)

                # using previous queried 'in_use' value as condition for WHERE
                where_info = {'project_id': project_id, 'resource': resource, 'in_use': current_in_use}
                update_usage = {'in_use': updated_in_use}

                _, result = self.update_rows('resource_usage_rm', UPDATE=update_usage, WHERE=where_info, log=True)

                # result[0] = number of rows have been updated
                if result[0] > 0:
                    nlog.info("Success : Update resource usage to resource_usage_rm table")
                    break
                # increase number attempts
                num_attempts += 1

                # get current usage record again
                nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=project_id,
                                                                            uuid_name=resource, error_item_text=None,
                                                                            allow_serveral=True)
                # update current in_use resource again
                current_in_use = usage['in_use']

            return True, result[0]

        # if number of rows is not integer
        else:
            print ("ERROR: Failed to update specific resource usage record (resource name: '%s' and project ID '%s')"
                   % (resource, project_id))
            nlog.error("ERROR: Failed to check presence of a specific resource (resource name: '%s' and projectID '%s')"
                       , resource, project_id)
            return False, None

    def reserved_record_update(self, project_id, resource, reserved, action):
        '''
        to update 'reserved' value for a specific resource in resource usage table against action = (ADD, UPDATE, DELETE)
        if action == ADD or UPDATE --> increase reserved
        if action == DELETE --> decrease reserved
        :param project_id:
        :param resource: name
        :param reserved: value
        :param action: (ADD, UPDATE, DELETE) --> to decide whether reserved resource is increased or decreased
        :return:
        '''

        # First checks that the state of records is what the thread previously knew to exist.
        # The UPDATE statement will include a WHERE condition that will ensure that the rows are only updated
        # in the table IF the current row values are what the thread thought they were
        # when previously reading the rows with the SELECT statement. The thread will check the number of rows
        # affected by the UPDATE statement.
        # If the number of rows affected is 0, then a randomized exponential backoff loop will be hit
        # and the process of reading and
        # then UPDATE ing with the WHERE condition will repeat until a pre-defined number of tries has been attempted.

        # use cases (1) or (2):
        # (1) to update DB after calculating reserved/allocated resource ( with per resource request)
        # (2) to update DB after resource usage sync from VIM (util_refresh flag =True)
        #
        # First get current resource usage and
        # check if there are any duplicate rows with corresponding project id and resource in db
        nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=project_id,
                                                                    uuid_name=resource, error_item_text=None,
                                                                    allow_serveral=True)

        # if there is no record in db regarding to that resource and tenant
        if nb_rows == 0:
            # passing number of row = 0 to trigger create new record for correspond resource
            print ("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present in db"
                   % (resource, project_id))
            nlog.error("ERROR: Resource usage with (resource name: '%s' and project ID '%s') is NOT present in db",
                       resource, project_id)
            return False, nb_rows

        # if number of rows > 1 --> row is already present and trigger update operation
        elif nb_rows == 1:
            # define max_attempts and number_attempts
            max_attempts = 10
            num_attempts = 0

            # get current usage
            current_reserved = usage['reserved']

            while num_attempts < max_attempts:
                # resource calculation (increased or decreased) that depend on action value (ADD or DELETE or UPDATE)
                updated_in_use = resource_calculation(current_value=current_reserved, acquired_value=reserved,
                                                      action=action)

                # using previous queried 'in_use' value as condition for WHERE
                where_info = {'project_id': project_id, 'resource': resource, 'in_use': current_reserved}
                update_usage = {'reserved': updated_in_use}

                _, result = self.update_rows('resource_usage_rm', UPDATE=update_usage, WHERE=where_info, log=True)

                # result[0] = number of rows have been updated
                if result[0] > 0:
                    nlog.info("Success : Update resource usage to resource_usage_rm table")
                    break
                # increase number attempts
                num_attempts += 1

                # get current usage record again
                nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=project_id,
                                                                            uuid_name=resource, error_item_text=None,
                                                                            allow_serveral=True)
                # update current in_use resource again
                current_reserved = usage['reserved']

            return True, result[0]

        # if number of rows is not integer
        else:
            print ("ERROR: Failed to update specific resource usage record (resource name: '%s' and project ID '%s')"
                   % (resource, project_id))
            nlog.error("ERROR: Failed to check presence of a specific resource (resource name: '%s' and projectID '%s')"
                       , resource, project_id)
            return False, None

    # get resource usage by uuid or resource name (default is uuid if no --> name) for all existing tenants/projects
    def get_resource_usage_by_uuid_name(self, uuid_name):
        '''
        get resource usage by uuid or resource name
        by uuid: return 1 row only
        by resource name: return more than 1 rows (same resource from different tenants)
        :param table:
        :param uuid_name:
        :return:
        '''
        result, resource_usage = self.get_resource_by_uuid_name('resource_usage_rm', uuid_name, error_item_text=None,
                                                                allow_serveral=True)
        if result <= 0:
            nlog.error("Error : can't get resource usage from DB with (uuid/resource name =%s, )", uuid_name)
            return False, None
        else:
            nlog.info("Success : get resource usage information from resource_usage_rm table")
        return result, resource_usage

    # get all resource usages for a given tenant
    def get_resource_usage_for_tenant(self, tenant_id):
        '''
        get resource usage for a tenant/project
        :param tenant_id:
        :return: result and rows (list of resource usage dict)
        '''

        result, resource_usage = self._get_resource_for_tenant_from_db('resource_usage_rm', tenant_id)
        if result <= 0:
            nlog.error("Error : get resource usage DB  (tenant ID =%s, )", tenant_id)
            return False, None
        else:
            nlog.info("Success : get resource usage information from resource_usage_rm table for a tenant")

        return result, resource_usage

    # get resource usage by uuid or name for a given tenant
    # check if a resource in a given tenant_id/project id is unique (non-duplicated)
    def get_resource_usage_by_uuid_name_for_tenant(self, tenant_id, uuid_name):
        '''
        Get resource usage by uuid or name for a given tenant
        :param tenant_id:
        :param uuid_name:
        :return: dict-specific resource usage for a tenant
        '''
        result, resource_usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id, uuid_name,
                                                                            error_item_text=None, allow_serveral=False)
        if result <= 0:
            nlog.error("Error : can't get resource usage from DB by uuid or resource name with "
                       "(uuid/resource name =%s in tenant ID '%s')", uuid_name, tenant_id)
            return False, None

        # check if a resource in a given tenant_id/project id is unique
        # if number of returned rows > 2 --> not unique
        elif result >= 2:
            nlog.warning("WARNING: Resource '%s' of project ID '%s' is duplicated in 'Resource usage' db table"
                         ,uuid_name, tenant_id )
        else:
            nlog.info("Success : Return 1 rows - '%s' resource usage information from resource_usage_rm table "
                      "for a tenant ID '%s'", uuid_name,tenant_id)
        return result, resource_usage


    def delete_resource_usage_for_tenant(self, tenant_id):
        result, _ = self.delete_resource_for_tenant('resource_usage_rm', tenant_id,
                                                                 log=False)
        if result <= 0:
            nlog.error("Error :  can't '_delete'resource usage for tenant ID '%s' from DB", tenant_id)
            return False, None
        else:
            nlog.info("Success : __del resource usage information from resource_usage_rm table for a tenant ID '%s'",
                      tenant_id)
        return result

    def delete_resource_usage_by_name_for_tenant(self, tenant_id, uuid_name):
        result, _ = self.delete_resource_by_name_uuid_for_tenant('resource_usage_rm', tenant_id, uuid_name,
                                                                              log=False)
        if result <= 0:
            nlog.error("Error : can't del resource usage from DB with (uuid/resource name =%s in tenant ID '%s')",
                       uuid_name, tenant_id)
            return False, None
        else:
            nlog.info("Success : del resource usage information from resource_usage_rm table for a tenant ID '%s'", tenant_id)
        return result

    def sync_resource_usage_for_tenant_from_vim(self, tenant_id, sync_usage=False):
        # TODO (rickyhai)
        return

    # quota-hard limit management
    #####################################################

    def create_all_quotas_for_tenant(self, tenant_id, quotas):

        '''
        Create quota for a given tenant
        :param tenant_id:
        :param quotas: (dict) input dictionary that is from api request
        quotas = {"cores": 10,"ram": 51200, "metadata_items": 100,"key_pairs": 100, "network":20,"security_group": 20,
        "security_group_rule": 20}}'
        :return:
        result
        quotas_data: out put dict with format that is used to store in db
        '''

        quotas_data = collections.defaultdict(dict)
        for resource, limit in quotas.iteritems():
            quotas_data[resource] = collections.defaultdict(dict)
            quotas_data[resource]['project_id'] = tenant_id
            quotas_data[resource]['resource'] = resource
            quotas_data[resource]['hard_limit'] = limit
            # quotas_data['allocated'] = 0
            # TODO(rickyhai) enable allocated when it's supported-hierarchy projects/tenants
            # TODO (ricky) implement existence checking for quota operations here

            result, uuid = self.new_row('quota_rm', INSERT=quotas_data[resource], add_uuid=True, log=False)
            if result <= 0:
                # debug only
                print "resource_db.create_all_quotas_for_tenant: Failed to create quota limit " \
                      "with (resource '%s' and tenant ID '%s')" % (resource, tenant_id)
                nlog.error("Error : can't create quota for (resource ='%s' for tenant ID '%s')", resource, tenant_id)
                # return False, None # Not used to avoid break
            else:
                # debug only
                print "resource_db.create_all_quotas_for_tenant: Successful to create quota limit " \
                      "with (resource '%s' and tenant ID '%s')" % (resource, tenant_id)
                nlog.info("Success : _create quotas for a tenant/project ID '%s'in quota db", tenant_id)

                # insert project_id and resource fields to resource usage table to keep updated/sync
                # between quota and resource usage tables
                #
                # First check if there are any duplicate rows with corresponding project id and resource in db
                nb_rows, usage = self._get_resource_by_uuid_name_for_tenant('resource_usage_rm', tenant_id=tenant_id,
                                                                     uuid_name=resource, error_item_text=None,
                                                                     allow_serveral=True)
                # print nb_rows
                # if there are no duplicates in db
                if nb_rows == 0:
                    # sync project_id and resource from quota table to resource usage table
                    usage_sync = {'project_id': tenant_id, 'resource': resource}
                    r, uuid = self.new_row('resource_usage_rm', INSERT=usage_sync, add_uuid=True, log=False)
                    if r >= 0:
                        # debug only
                        print ("INFO: Successful to add 'project_id' and 'resource' into resource usage table")
                        nlog.info("INFO: Successful to add 'project_id' and 'resource' into resource usage table ")
                else:
                    # debug only
                    print ("ERROR: No need to add Resource '%s' and project ID '%s' into Resource usage table due to: "
                           "Resource '%s' from project ID '%s' row is already present in DB "
                           % (resource, tenant_id, resource, tenant_id))

                    nlog.error("ERROR: No need to add Resource '%s' and project ID '%s' into Quota table due to:"
                               "Resource '%s' from project ID '%s' row is already present in DB",
                               resource, tenant_id, resource, tenant_id)
        return result, quotas_data

    def create_quota_by_name_for_tenant(self, tenant_id, resource, hard_limit, allocated):
        '''
        Create a resource quota for a tenant/project
        :param tenant_id:
        :param resource: resource name e.g: "vcpus"
        :param hard_limit: limit value for that resource e/g: hard_limit = 10
        :param allocated : set = 0  in db and no value at here as hierarchy projects/tenants
        is not supported yet in this version.
        :return:
        '''
        # TODO (ricky) need to implement for use of other functions

        return

    def update_all_quotas_for_tenant(self, tenant_id, update_quotas):

        quotas_data = collections.defaultdict(dict)
        for resource, limit in update_quotas.iteritems():
            quotas_data[resource] = collections.defaultdict(dict)
            # quotas_data[resource]['project_id'] = tenant_id
            # quotas_data[resource]['resource'] = resource
            quotas_data[resource]['hard_limit'] = limit
            # quotas_data['allocated'] = 0
            # TODO(rickyhai) enable allocated when it's supported-hierarchy projects/tenants

            # TODO (ricky) implement existence checking for quota operations here
            # add new record to DB if resource quota for that project is not present
            where = {'project_id': tenant_id, 'resource': resource}
            _, result = self.update_rows('quota_rm', UPDATE=quotas_data[resource], WHERE=where, log=False)

            # result is tuple and result[0] to pickup number of updated rows
            print result[0]
            if result[0] <= 0:
                # debug only
                print "resource_db.update_all_quotas_for_tenant:  Failed to update quota limit with (resource '%s' " \
                      "and tenant ID '%s'" % (resource, tenant_id)

                nlog.error("Error : can't update quotas for (resource ='%s' for tenant ID '%s')", resource, tenant_id)
                # return False, None
            else:
                # debug only
                print "resource_db.update_all_quotas_for_tenant:  Sucessful to update quota limit with (resource '%s' " \
                      "and tenant ID '%s'" % (resource, tenant_id)
                nlog.info("Success : update quotas for a tenant/project ID '%s'", tenant_id)
        print "Print result out of for loop: result[0] = %d" % result[0]  # TODO(ricky) disable when finish debug
        return result[0], quotas_data

    def update_quota_by_name_for_tenant(self, tenant_id, resource, hard_limit, allocated):
        '''
        update quota for a specific resource in a given tenant
        :param tenant_id:
        :param resource: name
        :param hard_limit: limit value
        :param allocated: not set yet as it is not support in this version (allocated is for hierarchy projects)
        :return:
        '''
        # TODO (ricky) need to implement for use of other functions
        return

    def get_all_quotas_for_tenant(self, tenant_id):
        '''
        Get all quota resources for a given tenant
        :param tenant_id:
        :return: all quota resources for a given tenant
        '''
        result, resource_usage = self._get_resource_for_tenant_from_db('quota_rm', tenant_id)
        if result <= 0:
            nlog.error("Error : get quota DB  (tenant ID =%s, )", tenant_id)
            return False, None
        else:
            nlog.info("Success : get quota information from quota table for a tenant")

        return result, resource_usage

    # get quota for a project by name
    def get_quota_for_project_by_name_uuid(self, tenant_id, resource):
        '''
        Get specific quota for a given tenant
        :param tenant_id:
        :param resource:
        :return: dict- quota for that resource
        '''
        result, quota = self._get_resource_by_uuid_name_for_tenant('quota_rm', tenant_id=tenant_id, uuid_name=resource,
                                                                            error_item_text=None, allow_serveral=False)
        if result <= 0:
            nlog.error("Error : can't get quota from DB by uuid or resource name with "
                       "(uuid/resource name =%s in tenant ID '%s')", resource, tenant_id)
            return False, None
        else:
            nlog.info("INFO: Successful to get quota by resource for a given project ")
            return result, quota


    def delete_all_quotas_for_project(self, tenant_id):
        '''
        Delete quota for a given tenant
        :param tenant_id:
        :return:
        '''
        result, _ = self.delete_resource_for_tenant('quota_rm', tenant_id, log=False)
        if result <= 0:
            nlog.error("Error :  can't '_delete' all quotas for tenant ID '%s' from DB", tenant_id)
            return False, None
        else:
            nlog.info("Success : __del resource usage information from resource_usage_rm table for a tenant ID '%s'",
                      tenant_id)
        return result

    # delete a specific quota resource by name
    def delete_quota_by_name_for_project(self, tenant_id, resource):
        result, _ = self.delete_resource_by_name_uuid_for_tenant('quota_rm', tenant_id=tenant_id,
                                                                 uuid_name=resource, log=False)
        if result <= 0:
            nlog.error("Error : can't del quota resource with (uuid/resource =%s in tenant ID '%s')",
                       resource, tenant_id)
            return False, None
        else:
            nlog.info("Success : del quota resource by name for a tenant ID '%s'/ resource '%s'",
                      tenant_id, resource)
        return result

    def sync_quota_for_tenant(self, tenant_id, sync=False):
        return









    ###############
    # Old codes
    ################################################################################
    # def update_tenants_utilization_compute_rm_table(self, uuid, action):
    #     # get vnf_using_cnt
    #     result, content = self.get_table_by_uuid_name("tenants_utilization_compute_rm", uuid, error_item_text=None, allow_serveral=False)
    #     if result <= 0:
    #         nlog.error("Error : Can't get tenants_utilization_compute_rm table")
    #         return False, None
    #     else:
    #         vnfd_using_cnt = content['vnfdUsingCnt']
    #         nlog.debug("vnfd using cnt = %d", vnfd_using_cnt)
    #
    #     if action == 'ADD':            vnfd_using_cnt = vnfd_using_cnt + 1
    #     elif action == 'DELETE':       vnfd_using_cnt = vnfd_using_cnt - 1
    #     else:                          return False, None
    #
    #     # update vnf_using_cnt
    #     update_info = {'vnfdUsingCnt': vnfd_using_cnt}
    #     result, _ = self.update_rows("vnfd_using_info", UPDATE=update_info, WHERE={'uuid':uuid}, log=True)
    #     if result < 0:
    #         nlog.error("Error : Can't table(vnfd_using_info) update")
    #         return False, None
    #
    #     return True, vnfd_using_cnt
    #
    # def delete_row_by_uuid_composite(self, table_name, uuid):
    #     try:
    #         with self.con:
    #             self.cur= self.con.cursor()
    #             sql = "DELETE FROM %s WHERE uuid= '%s'" % (table_name, uuid)
    #             print sql
    #             self.cur.execute(sql)
    #             deleted = self.cur.rowcount
    #             #print deleted
    #             if deleted > 0:
    #                 print "Deleted successfully next step --> adding new values"
    #                 return deleted
    #
    #             else:
    #                 print "Failed to delete"
    #                 print "###### %s row has been deleted ######" % deleted
    #                 print "###### 'uuid': %s was not existing in %s table ######" % (uuid, table_name)
    #
    #     except (mdb.Error, AttributeError), e:
    #         print "resource_db.replace_row_by_uuid_composite DB Exception %d : %s" % (e.args[0], e.args[1])

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
    # Old codes - users and tenants based - resources management- basic DB operations. Go here
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
        self.keys = self.allowed_keys.intersection(row_dict)

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
            added_uuid = self.cursor.lastrowid  # Returns the uuid value that is generated as AUTO_INCREMENT attribute
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
    db = resource_db.resource_db()
    # a = db.connect(host="116.89.184.43", user="root", passwd="", database="mano_db")

    # actual_usage = {'in_use': 4, 'reserved': 2}
    # r = db.update_resource_usage_by_name('f4211c8eee044bfb9dea2050fef2ace5', resource='vcpus', actual_usage=actual_usage)
    # c,r = db.get_resource_usage_for_tenant('f4211c8eee044bfb9dea2050fef2ace5')
    # c,r = db.delete_resource_usage_for_tenant(tenant_id='f4211c8eee044bfb9dea2050fef2ace5') #,uuid_name='vcpus')
    # print c
    # print r
    # where = {'uuid': 20}
    # dat_table = db.update_vnfTid_by_rsv_id('rsv_vnf_rm', '23762sbdhgwshdg', 'sjhdgsjdh121' , 'haiupdated')
    # print dat_table

    # sample input from other modules
    # quotas = {'vcpus': 2, 'vnfs' : 3, 'memory': 2000, 'network': 6 }
    # dat = db.create_all_quotas_for_tenant('f4211c8eee044bfb9dea2050fef2ace5', quotas)

    quotas_db = {'uuid': '1234dsd', 'project_id': 'af10gh', 'resource': 'vcpus', 'hard_limit': 10}
    quotas =db.build_quota_limit(quotas_db)


    # dat= db.create_all_quotas_for_tenant('f4211c8eee044bfb9dea2050fef2ace5', quotas)

