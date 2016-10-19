# -*- coding: utf-8 -*-

'''
NFVO DB engine. It implements all the methods to interact with the playnetmano Database
'''

import MySQLdb as mdb
import uuid as myUuid
import json
import yaml

from jsonschema import validate as js_v, exceptions as js_e

from utils_db import *
from rm_mano.global_info import *


class nfvo_db(utils_db):

    def __init__(self):
        utils_db.__init__(self)
        return


    def get_row_composite(self, table, project_tid, uuid, log=False):
        WHERE = "(projectTId, uuid) = (" + "\'" + project_tid + "\'" + "," + "\'" + str(uuid) + "\'" + ")"
        cmd = " SELECT * FROM " + table + " WHERE " + WHERE
        for retry_ in range(0, 2):
            try:
                with self.con:
                    self.cur = self.con.cursor(mdb.cursors.DictCursor)
                    if log:      nlog.info(cmd)
                    self.cur.execute(cmd)
                    rows = self.cur.fetchone()

                    return self.cur.rowcount, rows

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.get_row_composite DB Exception %d: %s" % (e.args[0], e.args[1]))
                r, c = self.format_error(e)
                if r != -HTTP_Request_Timeout or retry_ == 1:
                    return r, c


    def delete_row_composite(self, table, project_tid, uuid, log=False):
        WHERE = "(projectTId, uuid) = (" + "\'" + project_tid + "\'" + "," + "\'" + str(uuid) + "\'" + ")"
        nlog.debug(WHERE)

        for retry_ in range(0,2):
            try:
                with self.con:
                    self.cur = self.con.cursor()
                    cmd = "DELETE FROM %s WHERE %s" % (table, WHERE)
                    if log == True:         nlog.info(cmd)
                    self.cur.execute(cmd)
                    deleted = self.cur.rowcount

                return deleted, table[:-1] + " '%s' %s" %(WHERE, "deleted" if deleted==1 else "not found")

            except (mdb.Error, AttributeError), e:
                nlog.error("nfvo_db.delete_row_composite DB Exception %d: %s" % (e.args[0], e.args[1]))
                r,c =  self.format_error(e, "delete", 'instances' if table=='hosts' or table=='tenants' else 'dependencies')
                if r!=-HTTP_Request_Timeout or retry_==1:
                    return r,c


    def update_vnf_using_info_table(self, uuid, action):
        # get vnf_using_cnt
        result, content = self.get_table_by_uuid_name("vnfd_using_info", uuid, error_item_text=None, allow_serveral=False)
        if result <= 0:
            nlog.error("Error : Can't get vnfd_using_info table")
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


    '''
    def update_vnf_saveStatus(self, project_tid, vnf_tid, status):
        # get saveStatus
        result, content = self.get_row_composite("vnf_info", project_tid, vnf_tid, log=True)
        if result <= 0:
            nlog.error("Error : Can't get vnf_info table")
            return False, None
        else:
            vnf_save_status = content['saveStatus']
            nlog.debug("VNF save status = %s", vnf_save_status)

        # update saveStatus
        result, _ = self.update_row_composite("vnf_info", {'saveStatus':status}, project_tid, vnf_tid, log=True)
        if result < 0:
            nlog.error("Error : Can't update VNF Status(%s)", status)
            return False, None

        return True, vnf_save_status
    '''


    def management_vnf_info(self, project_tid, vnf_tid, vnfd_id, flag):
        if flag == "REMOVE_VNF":
            # delete vnf_info table
            result, _ = self.delete_row_composite("vnf_info", project_tid, vnf_tid, log=True)
            if result < 0:          nlog.error("Error : Can't del vnf_info table(continue)")

            # update vnf_using_info table
            result, vnfd_using_cnt = self.update_vnf_using_info_table(vnfd_id, action='DELETE')
            if result == False:
                nlog.error("Error : Can't update vnfd_using_info table")
                return False

        elif flag == "WITH_SAVE":
            # update vnf saveStatus from vnf_info table
            where_info = {'projectTId': project_tid, 'uuid': vnf_tid}
            result, _ = self.update_rows("vnf_info", {'saveStatus': "SAVED"}, where_info, log=True)
            if result < 0:
                nlog.error("Error : Can't update VNF Status(SAVED)")
                return False

        elif flag == "WITHOUT_SAVE":
            # get saveStatus from vnf_info table
            result, content = self.get_row_composite("vnf_info", project_tid, vnf_tid, log=True)
            if result <= 0:
                nlog.error("Error : Can't get vnf_info table")
                return False, None
            else:
                vnf_save_status = content['saveStatus']
                nlog.debug("VNF save status = %s", vnf_save_status)

            if vnf_save_status == "RUNNING":
                # delete vnf_info table
                result, _ = self.delete_row_composite("vnf_info", project_tid, vnf_tid, log=True)
                if result < 0:          nlog.error("Error : Can't del vnf_info table(continue)")

                # update vnf_using_info table
                result, vnfd_using_cnt = self.update_vnf_using_info_table(vnfd_id, action='DELETE')
                if result == False:
                    nlog.error("Error : Can't update vnfd_using_info table")
                    return False

        else:
            nlog.error("Error : Invalid parameter(flag = %s)", flag)
            return False

        return True


    def get_project_vnf_content(self, project_tid, vnf_tid):
        # get project_iid from project_info table
        result, project_content = self.get_table_by_uuid_name("project_info", project_tid, error_item_text=None, allow_serveral=False)
        if result <= 0:
            nlog.error("Error : Get project_iid using project_tid")
            return False, None, None

        # get vnf_iid from vnfd table
        result, vnf_content = self.get_row_composite("vnf_info", project_tid, vnf_tid, log=True)
        if result <= 0:
            nlog.error("Error : Can't get vnf_info table")
            return False, None, None

        return True, project_content, vnf_content

