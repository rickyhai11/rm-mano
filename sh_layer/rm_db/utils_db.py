# -*- coding: utf-8 -*-

'''
NFVO DB engine. It implements all the methods to interact with the playnetmano Database
'''

import MySQLdb as mdb
import uuid as myUuid
import json
import bottle

from jsonschema import validate as js_v, exceptions as js_e

from sh_layer.global_info import *
from sh_layer import utils
from sh_layer.common.utils_rm import *

# import utils


class utils_db():

    def __init__(self):
        #initialization
        return

    def connect(self, host=None, user=None, passwd=None, database=None):
        '''Connect to specific data base. 
        The first time a valid host, user, passwd and database must be provided,
        Following calls can skip this parameters
        '''
        try:
            if host     is not None: self.host = host
            if user     is not None: self.user = user
            if passwd   is not None: self.passwd = passwd
            if database is not None: self.database = database

            self.con = mdb.connect(self.host, self.user, self.passwd, self.database)
            nlog.info("DB: connected to %s@%s -> %s" % (self.user, self.host, self.database))
            return 0
        except mdb.Error, e:
            nlog.error("Error connecting to DB %s@%s -> %s Error %d: %s" % (self.user, self.host, self.database, e.args[0], e.args[1]))
            return -1
        

    def disconnect(self):
        '''disconnect from specific data base'''
        try:
            self.con.close()
            del self.con
        except mdb.Error, e:
            nlog.error("Error disconnecting from DB: Error %d: %s" % (e.args[0], e.args[1]))
            return -1
        except AttributeError, e: #self.con not defined
            if e[0][-5:] == "'con'": return -1, "Database internal error, no connection."
            else: raise

    def conn_db(self, db_host, db_user, db_passwd, db_name):
        if self.connect(db_host, db_user, db_passwd, db_name) == -1:
            nlog.error("Error : connecting to database %s at %s @ %s", 'db_name', db_user, db_host)
            return (False, None)

        nlog.info("Success : Connect DB")
        return True


    def format_in(self, default_schema):
        try:
            format_type = bottle.request.headers.get('Content-Type', 'application/json')
            if 'application/json' in format_type:
                client_data = bottle.request.json
            else:
                nlog.error('Content-Type %s not supported.', str(format_type))
                bottle.abort(HTTP_Not_Acceptable, 'Content-Type ' + str(format_type) + ' not supported.')
                return

            if default_schema == None:
                bottle.abort(HTTP_Bad_Request, "Invalid schema version or missing version field")

            used_schema = default_schema
            js_v(client_data, used_schema)

            return client_data, used_schema

        except js_e.ValidationError as exc:
            nlog.error("validate_in error, jsonschema exception %s at %s", exc.message, exc.path)
            error_pos = ""
            if len(exc.path)>0:
                error_pos=" at " + ":".join(map(json.dumps, exc.path))
            bottle.abort(HTTP_Bad_Request, error_text + exc.message + error_pos)


    def format_error(self, e, command=None, extra=None): 
        if type(e[0]) is str:
            if e[0][-5:] == "'con'":
                return -HTTP_Internal_Server_Error, "DB Exception, no connection."
            else:
                raise

        if e.args[0]==2006 or e.args[0]==2013 : #MySQL server has gone away (((or)))    Exception 2013: Lost connection to MySQL server during query
            #reconnect
            self.connect()
            return -HTTP_Request_Timeout,"Database reconnection. Try Again"
        
        fk=e.args[1].find("foreign key constraint fails")
        if fk>=0:
            if command=="update":
                return -HTTP_Bad_Request, "tenant_id %s not found." % extra
            elif command=="delete":
                return -HTTP_Bad_Request, "Resource is not free. There are %s that prevent deleting it." % extra

        de = e.args[1].find("Duplicate entry")
        fk = e.args[1].find("for key")
        uk = e.args[1].find("Unknown column")
        wc = e.args[1].find("in 'where clause'")
        fl = e.args[1].find("in 'field list'")
        if de>=0:
            if fk>=0: #error 1062
                return -HTTP_Conflict, "Value %s already in use for %s" % (e.args[1][de+15:fk], e.args[1][fk+7:])
        if uk>=0:
            if wc>=0:
                return -HTTP_Bad_Request, "Field %s can not be used for filtering" % e.args[1][uk+14:wc]
            if fl>=0:
                return -HTTP_Bad_Request, "Field %s does not exist" % e.args[1][uk+14:wc]
        return -HTTP_Internal_Server_Error, "Database internal Error %d: %s" % (e.args[0], e.args[1])


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


    def __update_rows(self, table, UPDATE, WHERE, log=False):
        ''' Update one or several rows into a table.
        Atributes
            UPDATE: dictionary with the key: value to change
            table: table where to update
            WHERE: dictionary of elements to update
        Return: (result, descriptive text) where result indicates the number of updated files, negative if error
        '''
        # gettting uuid
        uuid = WHERE['uuid'] if 'uuid' in WHERE else None

        cmd = "UPDATE " + table +" SET " + \
            ",".join(map(self.__tuple2db_format_set, UPDATE.iteritems() )) + \
            " WHERE " + " and ".join(map(self.__tuple2db_format_where, WHERE.iteritems() ))
        if log:
            nlog.info(cmd)
        print cmd
        self.cur.execute(cmd)
        nb_rows = self.cur.rowcount
        print nb_rows

        if nb_rows > 0 and log:
            #inserting new log
            if uuid is None:
                uuid_k = uuid_v = ""
            else:
                uuid_k=",uuid"; uuid_v=",'" + str(uuid) + "'"

            cmd = "INSERT INTO logs (related,level%s,description) VALUES ('%s','debug'%s,\"updating %d entry %s\")" \
                % (uuid_k, table, uuid_v, nb_rows, (str(UPDATE)).replace('"','-')  )
            nlog.info(cmd)
            self.cur.execute(cmd)

        return nb_rows, "%d updated from %s" % (nb_rows, table[:-1])


    def _new_row_internal(self, table, INSERT, add_uuid=False, log=False):
        ''' Add one row into a table. It DOES NOT begin or end the transaction, so self.con.cursor must be created
        Attribute 
            INSERT: dictionary with the key: value to insert
            table: table where to insert
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

        #insertion
        cmd = "INSERT INTO " + table +" SET " + \
            ",".join(map(self.__tuple2db_format_set, INSERT.iteritems() ))
        if log:     nlog.info(cmd)
        self.cur.execute(cmd)
        nb_rows = self.cur.rowcount

        #inserting new log
        if nb_rows > 0 and log:
            if add_uuid:
                del INSERT['uuid']

            if uuid is None:
                uuid_k = uuid_v = ""
            else:
                uuid_k=",uuid"; uuid_v=",'" + str(uuid) + "'"

            cmd = "INSERT INTO logs (related,level%s,description) VALUES ('%s','debug'%s,\"new %s %s\")" \
                % (uuid_k, table, uuid_v, table[:-1], str(INSERT).replace('"','-'))

            nlog.info(cmd)
            #self.cur.execute(cmd)

        return nb_rows, uuid


    def __get_rows(self,table,uuid):
        self.cur.execute("SELECT * FROM " + str(table) +" where uuid='" + str(uuid) + "'")
        rows = self.cur.fetchall()
        return self.cur.rowcount, rows


    def new_row(self, table, INSERT, add_uuid=False, log=False):
        ''' Add one row into a table.
        Attribute 
            INSERT: dictionary with the key: value to insert
            table: table where to insert
            add_uuid: if True, it will create an uuid key entry at INSERT if not provided
        It checks presence of uuid and add one automatically otherwise
        Return: (result, uuid) where result can be 0 if error, or 1 if ok
        '''

        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    return self._new_row_internal(table, INSERT, add_uuid, log)
                    
            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.new_row DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


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
                nlog.error("nfvo_db.update_rows DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c
            

    def delete_row(self, table, uuid, log=False):
        for retry_ in range(0,2):
            try:
                with self.con:
                    #delete host
                    self.cur = self.con.cursor()
                    cmd = "DELETE FROM %s WHERE uuid = '%s'" % (table, uuid)
                    if log == True:
                        nlog.info(cmd)
                    self.cur.execute(cmd)
                    deleted = self.cur.rowcount

                return deleted, table[:-1] + " '%s' %s" %(uuid, "deleted" if deleted==1 else "not found")

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.delete_resource_by_name_uuid_for_tenant DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c =  self.format_error(e, "delete", 'instances' if table=='hosts' or table=='tenants' else 'dependencies')
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


    def delete_row_by_dict(self, log=False, **sql_dict):
        ''' Deletes rows from a table.
        Attribute sql_dir: dictionary with the following key: value
            'FROM': string of table name (Mandatory)
            'WHERE': dict of key:values, translated to key=value AND ... (Optional)
            'WHERE_NOT': dict of key:values, translated to key<>value AND ... (Optional)
            'WHERE_NOTNULL': (list or tuple of items that must not be null in a where ... (Optional)
            'LIMIT': limit of number of rows (Optional)
        Return: the (number of items deleted, descriptive test) if ok; (negative, descriptive text) if error
        '''
        from_  = "FROM " + str(sql_dict['FROM'])
        if 'WHERE' in sql_dict and len(sql_dict['WHERE']) > 0:
            w=sql_dict['WHERE']
            where_ = "WHERE " + " AND ".join(map(self.__tuple2db_format_where, w.iteritems()))
        else:
            where_ = ""

        if 'WHERE_NOT' in sql_dict and len(sql_dict['WHERE_NOT']) > 0: 
            w=sql_dict['WHERE_NOT']
            where_2 = " AND ".join(map(self.__tuple2db_format_where_not, w.iteritems()))
            if len(where_)==0:
                where_ = "WHERE " + where_2
            else:
                where_ = where_ + " AND " + where_2

        if 'WHERE_NOTNULL' in sql_dict and len(sql_dict['WHERE_NOTNULL']) > 0: 
            w=sql_dict['WHERE_NOTNULL']
            where_2 = " AND ".join(map( lambda x: str(x) + " is not Null",  w) )
            if len(where_)==0:
                where_ = "WHERE " + where_2
            else:
                where_ = where_ + " AND " + where_2

        limit_ = "LIMIT " + str(sql_dict['LIMIT']) if 'LIMIT' in sql_dict else ""
        cmd =  " ".join( ("DELETE", from_, where_, limit_) )
        if log == True:
            nlog.info(cmd)

        for retry_ in range(0,2):
            try:
                with self.con:
                    #delete host
                    self.cur = self.con.cursor()
                    self.cur.execute(cmd)
                    deleted = self.cur.rowcount
                return deleted, "%d deleted from %s" % (deleted, sql_dict['FROM'][:-1] )
            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.delete_resource_by_name_uuid_for_tenant DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c =  self.format_error(e, "delete", 'dependencies')
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


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
                nlog.error("nfvo_db.get_rows DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


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
        select_= "SELECT " + ("*" if 'SELECT' not in sql_dict else ",".join(map(str,sql_dict['SELECT'])) )
        from_  = "FROM " + str(sql_dict['FROM'])

        if 'WHERE' in sql_dict and len(sql_dict['WHERE']) > 0:
            w=sql_dict['WHERE']
            where_ = "WHERE " + " AND ".join(map(self.__tuple2db_format_where, w.iteritems() ))
        else:
            where_ = ""

        if 'WHERE_NOT' in sql_dict and len(sql_dict['WHERE_NOT']) > 0: 
            w=sql_dict['WHERE_NOT']
            where_2 = " AND ".join(map(self.__tuple2db_format_where_not, w.iteritems() ) )
            if len(where_)==0:
                where_ = "WHERE " + where_2
            else:
                where_ = where_ + " AND " + where_2

        if 'WHERE_NOTNULL' in sql_dict and len(sql_dict['WHERE_NOTNULL']) > 0: 
            w=sql_dict['WHERE_NOTNULL']
            where_2 = " AND ".join(map( lambda x: str(x) + " is not Null",  w) )
            if len(where_)==0:
                where_ = "WHERE " + where_2
            else:
                where_ = where_ + " AND " + where_2

        limit_ = "LIMIT " + str(sql_dict['LIMIT']) if 'LIMIT' in sql_dict else ""
        cmd =  " ".join( (select_, from_, where_, limit_) )
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    nlog.info(cmd)
                    self.cur.execute(cmd)
                    
                    rows = self.cur.fetchall()
                    
                    return self.cur.rowcount, rows
            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_table DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


    def get_table_by_uuid_name(self, table, uuid_name, error_item_text=None, allow_serveral=False):
        ''' Obtain One row from a table based on name or uuid.
        Attribute:
            table: string of table name
            uuid_name: name or uuid. If not uuid format is found, it is considered a name
            allow_severeral: if False return ERROR if more than one row are founded 
            error_item_text: in case of error it identifies the 'item' name for a proper output text 
        Return: if allow_several==False, a dictionary with this row, or error if no item is found or more than one is found
                if allow_several==True, a list of dictionaries with the row or rows, error if no item is found
        '''

        if error_item_text==None:
            error_item_text = table
        what = 'uuid' if utils.check_valid_uuid(uuid_name) else 'name'
        cmd =  " SELECT * FROM " + table + " WHERE " + what +" ='"+uuid_name+"'"
        print cmd
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    nlog.info(cmd)
                    self.cur.execute(cmd)
                    number = self.cur.rowcount
                    if number==0:
                        return -HTTP_Not_Found, "No %s found with %s '%s'" %(error_item_text, what, uuid_name)
                    elif number>1 and not allow_serveral: 
                        return -HTTP_Bad_Request, "More than one %s found with %s '%s'" %(error_item_text, what, uuid_name)

                    if allow_serveral:
                        rows = self.cur.fetchall()
                    else:
                        rows = self.cur.fetchone()

                    return number, rows

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_table_by_uuid_name DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    def get_uuid(self, uuid):
        '''check in the database if this uuid is already present'''
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    self.cur.execute("SELECT * FROM uuids where uuid ''='" + str(uuid) + "'")
                    rows = self.cur.fetchall()
                    return self.cur.rowcount, rows
            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_uuid DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    # Resource management, go here
    #
    ####################################################################################
    def _get_resource_for_tenant_from_db(self, table, tenant_id):
        '''
        get resource usage for a given tenant/project
        :param table:
        :param tenant_id:
        :return:
        '''
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    cmd = "SELECT * FROM %s WHERE project_id='%s'" % (table, tenant_id)
                    self.cur.execute(cmd)
                    rows = self.cur.fetchall()
                    return self.cur.rowcount, rows
            except (mdb.Error, AttributeError), e:
                nlog.error("utils_db._get_resource_for_tenant_from_db DB Exception %d: %s" % (e.args[0], e.args[1]))
                r, c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    # if allow_serveral= True and resource name is used
    # return: all rows from all existing tenants with corresponding resource name
    # if allow_serveral= False and uuid is used
    # return: only one row with corresponding uuid
    def get_resource_by_uuid_name(self, table, uuid_name, error_item_text=None, allow_serveral=False):
        ''' Obtain One row or All rows from a table based on name or uuid.
        Attribute:
            table: string of table name
            uuid_name: name or uuid. If not uuid format is found, it is considered a name
            allow_severeral: if False return ERROR if more than one row are founded
            error_item_text: in case of error it identifies the 'item' name for a proper output text
        Return: if allow_several==False, a dictionary with this row, or error if no item is found or more than one is found
                if allow_several==True, a list of dictionaries with the row or rows, error if no item is found
        '''

        if error_item_text == None:
            error_item_text = table

        what = 'uuid' if utils.check_valid_uuid(uuid_name) else 'resource'
        # validate resource name (input data)
        if what == 'resource':
            validate_resource_by_name(resource=uuid_name)

        cmd = " SELECT * FROM " + table + " WHERE " + what +" ='"+uuid_name+"'"
        print cmd
        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    nlog.info(cmd)
                    self.cur.execute(cmd)
                    number = self.cur.rowcount
                    if number==0:
                        return -HTTP_Not_Found, "No %s found with %s '%s'" %(error_item_text, what, uuid_name)
                    elif number>1 and not allow_serveral:
                        return -HTTP_Bad_Request, "More than one %s found with %s '%s'" %(error_item_text, what, uuid_name)

                    if allow_serveral:
                        rows = self.cur.fetchall()
                    else:
                        rows = self.cur.fetchone()

                    return number, rows

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_table_by_uuid_name DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    # get a specific resource by uuid or name for a given tenant/project
    # help to check if there is any duplicate rows with (tenant id and uuid or resource name)
    def _get_resource_by_uuid_name_for_tenant(self, table, tenant_id, uuid_name, error_item_text=None, allow_serveral=False):
        ''' Obtain One row from a table based on name or uuid.
        Attribute:
            table: string of table name
            tenant_id: tenant/project ID
            uuid_name: name or uuid. If not uuid format is found, it is considered a name
            allow_severeral: if False return ERROR if more than one row are founded
            error_item_text: in case of error it identifies the 'item' name for a proper output text
        Return: if allow_several==False, a dictionary with this row, or error if no item is found or more than one is found
                if allow_several==True, a list of dictionaries with the row or rows, error if no item is found
        '''

        if error_item_text == None:
            error_item_text = table

        what = 'uuid' if utils.check_valid_uuid(uuid_name) else 'resource'

        # validate input resource name
        if what == 'resource':
            validate_resource_by_name(resource=uuid_name)

        cmd = " SELECT * FROM " + table + " WHERE " + what +" ='"+uuid_name+"' AND project_id='%s'" % tenant_id
        print cmd
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    nlog.info(cmd)
                    self.cur.execute(cmd)
                    number = self.cur.rowcount
                    if number == 0:
                        nlog.error("%s No %s found with %s '%s' in project ID '%s' ", -HTTP_Not_Found, error_item_text,
                                   what, uuid_name, tenant_id)
                        # return -HTTP_Not_Found, "No %s found with %s '%s' in project ID %s" %(error_item_text, what,
                        #                                                                       uuid_name, tenant_id)
                    elif number > 1 and not allow_serveral:
                        nlog.error("%s More than one %s found with %s '%s' ",
                                   -HTTP_Bad_Request,error_item_text, what, uuid_name)
                        # return -HTTP_Bad_Request, "More than one %s found with %s '%s'" %(error_item_text, what, uuid_name)

                    if allow_serveral:
                        rows = self.cur.fetchall()
                    else:
                        rows = self.cur.fetchone()
                    # print number
                    # print rows

                    return number, rows

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_table_by_uuid_name DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c = self.format_error(e)
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    # delete all resources for a given tenant
    def delete_resource_for_tenant(self, table, tenant_id, log=False):

        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    cmd = "DELETE FROM %s WHERE project_id = '%s'" % (table, tenant_id)
                    if log == True:
                        nlog.info(cmd)
                    self.cur.execute(cmd)
                    deleted = self.cur.rowcount

                return deleted, table[:-1] + " '%s' %s" %(tenant_id, "all resources for a given project: deleted" if deleted == 1 else "not found")

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.delete_resource_by_name_uuid_for_tenant DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c =  self.format_error(e, "delete", 'instances' if table =='hosts' or table =='tenants' else 'dependencies')
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c

    # delete a specific resource by name for a given tenant
    # uuid_name  =  resource name e.g; 'vcpus'... or uuid
    def delete_resource_by_name_uuid_for_tenant(self, table, tenant_id, uuid_name, log=False):

        what = 'uuid' if utils.check_valid_uuid(uuid_name) else 'resource'
        # validate input resource name
        if what == 'resource':
            validate_resource_by_name(resource=uuid_name)
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    cmd = " DELETE FROM " + table + " WHERE " + what +" ='"+uuid_name+"' AND project_id= '%s'" % tenant_id
                    if log == True:
                        nlog.info(cmd)
                    self.cur.execute(cmd)
                    deleted = self.cur.rowcount

                return deleted, table[:-1] + " '%s' %s" %(uuid_name, "deleted" if deleted == 1 else "not found")

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.delete_resource_by_name_uuid_for_tenant DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c =  self.format_error(e, "delete", 'instances' if table =='hosts' or table =='tenants' else 'dependencies')
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c




