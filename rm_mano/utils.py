import bottle
import httplib
import logging.handlers
import os
import yaml
import json
import datetime

from jsonschema import validate as js_v, exceptions as js_e

from rm_mano.playnetmano_schemas import config_schema
from global_info import *


##
#  log handler setting
##
def set_logger(module_name, log_level, log_path, log_size, log_num):

    mlog = logging.getLogger(module_name)

    if log_level == 'CRITICAL':
        mlog.setLevel(logging.CRITICAL)
    elif log_level == 'ERROR':
        mlog.setLevel(logging.ERROR)
    elif log_level == 'WARNING':
        mlog.setLevel(logging.WARNING)
    elif log_level == 'INFO':
        mlog.setLevel(logging.INFO)
    elif log_level == 'DEBUG':
        mlog.setLevel(logging.DEBUG)
    else:
        return False, None

    filename = module_name + '_log'
    log_filename = log_path + '/' + filename

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=log_size, backupCount=log_num)
    mlog.addHandler(handler)

#   formatter = logging.Formatter('%(asctime)s : %(funcName)s : %(lineno)d : %(message)s')
    formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s(%(lineno)d)] :: %(message)s', datefmt='%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    return True, mlog


def read_file(file_to_read):
    """Reads a file specified by 'file_to_read' and returns (True,<its content as a string>) in case of success or (False, <error message>) in case of failure"""
    try:
        f = open(file_to_read, 'r')
        read_data = f.read()
        f.close()
    except Exception,e:
        return (False, str(e))
      
    return (True, read_data)


def write_file(file_to_write, text):
    """Write a file specified by 'file_to_write' and returns (True,NOne) in case of success or (False, <error message>) in case of failure"""
    try:
        f = open(file_to_write, 'w')
        f.write(text)
        f.close()
    except Exception,e:
        return (False, str(e))
      
    return (True, None)


def load_configuration():
    default_tokens = {'http_port': 9090, 'http_host': 'http://playnet-mano.fncp.re.kr'}
    try:
        # Check config file exists
        if not os.path.isfile(config_file):
            #            print "Error : Configuration file %s does not exists.", configuration_file
            return (False, "Error: Configuration file '" + config_file + "' does not exists.")

        # Read file
        (return_status, code) = read_file(config_file)
        if not return_status:
            #            print "Error : Can't load configuration file %s : %s", configuration_file, code
            return (return_status, "Error loading configuration file '" + config_file + "': " + code)
        # Parse configuration file
        try:
            config = yaml.load(code)
        except yaml.YAMLError, exc:
            error_pos = ""
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                error_pos = " at position: (%s:%s)" % (mark.line + 1, mark.column + 1)
            # print "Error : Can't load configuration file %s " configuration_file
            #            print "        %s : content format error: Failed to parse yaml format" error_pos
            return (False,
                    "Error loading configuration file '" + config_file + "'" + error_pos + ": content format error: Failed to parse yaml format")

        # Validate configuration file with the config_schema
        try:
            js_v(config, config_schema)
        except js_e.ValidationError, exc:
            error_pos = ""
            if len(exc.path) > 0:
                error_pos = " at '" + ":".join(map(str, exc.path)) + "'"
            # print "Error : Can't load configuration file %s", configuration_file
            #            print "        %s : %s", error_pos, exc.message
            return (
            False, "Error loading configuration file '" + config_file + "'" + error_pos + ": " + exc.message)

        # Check default values tokens
        for k, v in default_tokens.items():
            if k not in config: config[k] = v

    except Exception, e:
        #        print "Error : Can't load configuration file %s (%s)", configuration_file, str(e)
        return (False, "Error loading configuration file '" + config_file + "': " + str(e))

    return (True, config)


def remove_extra_items(data, schema):
    deleted=[]
    if type(data) is tuple or type(data) is list:
        for d in data:
            a= remove_extra_items(d, schema['items'])
            if a is not None: deleted.append(a)
    elif type(data) is dict:
        #TODO deal with patternProperties
        if 'properties' not in schema:
            return None
        for k in data.keys():
            if k not in schema['properties'].keys():
                del data[k]
                deleted.append(k)
            else:
                a = remove_extra_items(data[k], schema['properties'][k])
                if a is not None:  deleted.append({k:a})
    if len(deleted) == 0: return None
    elif len(deleted) == 1: return deleted[0]
    else: return deleted


def convert_bandwidth(data, reverse=False):
    '''Check the field bandwidth recursivelly and when found, it removes units and convert to number 
    It assumes that bandwidth is well formed
    Attributes:
        'data': dictionary bottle.FormsDict variable to be checked. None or empty is consideted valid
        'reverse': by default convert form str to int (Mbps), if True it convert from number to units
    Return:
        None
    '''
    if type(data) is dict:
        for k in data.keys():
            if type(data[k]) is dict or type(data[k]) is tuple or type(data[k]) is list:
                convert_bandwidth(data[k], reverse)
        if "bandwidth" in data:
            try:
                value=str(data["bandwidth"])
                if not reverse:
                    pos = value.find("bps")
                    if pos>0:
                        if value[pos-1]=="G": data["bandwidth"] =  int(data["bandwidth"][:pos-1]) * 1000
                        elif value[pos-1]=="k": data["bandwidth"]= int(data["bandwidth"][:pos-1]) / 1000
                        else: data["bandwidth"]= int(data["bandwidth"][:pos-1])
                else:
                    value = int(data["bandwidth"])
                    if value % 1000 == 0: data["bandwidth"]=str(value/1000) + " Gbps"
                    else: data["bandwidth"]=str(value) + " Mbps"
            except:
                print "convert_bandwidth exception for type", type(data["bandwidth"]), " data", data["bandwidth"]
                return
    if type(data) is tuple or type(data) is list:
        for k in data:
            if type(k) is dict or type(k) is tuple or type(k) is list:
                convert_bandwidth(k, reverse)


def convert_str2boolean(data, items):
    '''Check recursively the content of data, and if there is an key contained in items, convert value from string to boolean 
    Done recursively
    Attributes:
        'data': dictionary variable to be checked. None or empty is considered valid
        'items': tuple of keys to convert
    Return:
        None
    '''
    if type(data) is dict:
        for k in data.keys():
            if type(data[k]) is dict or type(data[k]) is tuple or type(data[k]) is list:
                convert_str2boolean(data[k], items)
            if k in items:
                if type(data[k]) is str:
                    if   data[k]=="false" or data[k]=="False": data[k]=False
                    elif data[k]=="true"  or data[k]=="True":  data[k]=True
    if type(data) is tuple or type(data) is list:
        for k in data:
            if type(k) is dict or type(k) is tuple or type(k) is list:
                convert_str2boolean(k, items)


def check_valid_uuid(uuid):
    id_schema = {"type" : "string", "pattern": "^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$"}
    try:
        js_v(uuid, id_schema)
        return True
    except js_e.ValidationError:
        return False


def delete_nulls(var):
    if type(var) is dict:
        for k in var.keys():
            if var[k] is None:
                del var[k]
            elif type(var[k]) is dict or type(var[k]) is list or type(var[k]) is tuple:
                if delete_nulls(var[k]): del var[k]
        if len(var) == 0: return True
    elif type(var) is list or type(var) is tuple:
        for k in var:
            if type(k) is dict: delete_nulls(k)
        if len(var) == 0: return True
    return False


def convert_datetime2str(var):
    '''Converts a datetime variable to a string with the format '%Y-%m-%dT%H:%i:%s'
    It enters recursively in the dict var finding this kind of variables
    '''
    if type(var) is dict:
        for k, v in var.its():
            if type(v) is datetime.datetime:
                var[k] = v.strftime('%Y-%m-%dT%H:%M:%S')
            elif type(v) is dict or type(v) is list or type(v) is tuple:
                convert_datetime2str(v)
        if len(var) == 0: return True
    elif type(var) is list or type(var) is tuple:
        for v in var:
            convert_datetime2str(v)


def change_keys_http2db(data, http_db, reverse=False):
    '''Change keys of dictionary data acording to the key_dict values
    This allow change from http interface names to database names.
    When reverse is True, the change is otherwise
    Attributes:
        data: can be a dictionary or a list
        http_db: is a dictionary with hhtp names as keys and database names as value
        reverse: by default change is done from http api to database. If True change is done otherwise
    Return: None, but data is modified'''
    if type(data) is tuple or type(data) is list:
        for d in data:
            change_keys_http2db(d, http_db, reverse)
    elif type(data) is dict or type(data) is bottle.FormsDict:
        if reverse:
            for k, v in http_db.items():
                if v in data: data[k] = data.pop(v)
        else:
            for k, v in http_db.items():
                if k in data: data[v] = data.pop(k)


def format_out(data):
        bottle.response.content_type = 'application/json'

        # return data #json no style
        return json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False, encoding='utf-8') + "\n"


def format_out_notsort(data):
        bottle.response.content_type = 'application/json'

        # return data #json no style
        return json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False, encoding='utf-8') + "\n"


def format_in(default_schema):
    try:
#        format_type = bottle.request.headers.get('Content-Type', 'application/json')
        client_data = json.load(bottle.request.body)

        used_schema = default_schema
        if used_schema == None:
            bottle.abort(HTTP_Bad_Request, "Invalid schema version or missing version field")

        js_v(client_data, used_schema)

        return client_data, used_schema

    except js_e.ValidationError as exc:
        nlog.info("validate_in error, jsonschema exception %s at %s", exc.message, exc.path)

        error_pos = ""
        if len(exc.path) > 0: error_pos = " at " + ":".join(map(json.dumps, exc.path))
        bottle.abort(HTTP_Bad_Request, "Invalid content " + exc.message + error_pos)


def filter_query_string(qs, http2db, allowed):
    '''Process query string (qs) checking that contains only valid tokens for avoiding SQL injection
    Attributes:
        'qs': bottle.FormsDict variable to be processed. None or empty is considered valid
        'http2db': dictionary with change f rom http API naming (dictionary key) to database naming(dictionary value)
        'allowed': list of allowed string tokens (API http naming). All the keys of 'qs' must be one of 'allowed'
    Return: A tuple with the (select,where,limit) to be use in a database query. All of then transformed to the database naming
        select: list of items to retrieve, filtered by query string 'field=token'. If no 'field' is present, allowed list is returned
        where: dictionary with key, value, taken from the query string token=value. Empty if nothing is provided
        limit: limit dictated by user with the query string 'limit'. 100 by default
    abort if not permited, using bottel.abort
    '''
    where = {}
    limit = 100
    select = []
    if type(qs) is not bottle.FormsDict:
        nlog.info('!!!!!!!!!!!!!!invalid query string not a dictionary')
        # bottle.abort(HTTP_Internal_Server_Error, "call programmer")
    else:
        for k in qs:
            if k == 'field':
                select += qs.getall(k)
                for v in select:
                    if v not in allowed:
                        bottle.abort(HTTP_Bad_Request, "Invalid query string at 'field=" + v + "'")
            elif k == 'limit':
                try:
                    limit = int(qs[k])
                except:
                    bottle.abort(HTTP_Bad_Request, "Invalid query string at 'limit=" + qs[k] + "'")
            else:
                if k not in allowed:
                    bottle.abort(HTTP_Bad_Request, "Invalid query string at '" + k + "=" + qs[k] + "'")
                if qs[k] != "null":
                    where[k] = qs[k]
                else:
                    where[k] = None
    if len(select) == 0: select += allowed
    # change from http api to database naming
    for i in range(0, len(select)):
        k = select[i]
        if http2db and k in http2db:
            select[i] = http2db[k]
    if http2db:
        change_keys_http2db(where, http2db)
    nlog.info("filter_query_string", select, where, limit)

    return select, where, limit


def conn_httpserver(host=None, port=0, time_out=0):
    if (host == None) | (port == 0) | (time_out < 0):
        nlog.error("Error : Invalid parameter(host = %s, port = %d)", host, port)
        return False, None

    nlog.debug("host : %s, port : %d, time_out = %d", host, port, time_out)

    if time_out == 0:
        connection = httplib.HTTPConnection(host, port)
    else:
        connection = httplib.HTTPConnection(host, port, timeout=time_out)

    return True, connection


def send_msg(conn=None, method=None, uri=None, message=None):
    if (conn == None) | (method == None) | (uri == None) | (message == None):
        nlog.error("Error : Invalid parameter(method = %s, uri = %s, message = %s)", method, uri, message)
        return False

    headers = {'Content-type': 'application/json'}
    json_msg = json.dumps(message)
    conn.request(method, uri, json_msg, headers)

    return True


def recv_msg(conn=None):
    if (conn == None):
        nlog.error("Error : Invalid parameter(conn = None)")
        return False, None

    response = conn.getresponse()
    data = response.read()

    return True, data


def conn_vim(config, method, uri, message):

    rst, conn = conn_httpserver(config['vim_ip'], config['vim_port'])
    if (rst == False) | (conn == None):
        nlog.error("Error : Can't connect httpserver('VIM')")
        return False, None

    # Send message to VIM
    rst = send_msg(conn, method, uri, message)
    if rst == False:
        nlog.error("Error : Can't send message to VIM")
        return False, None

    # Receive message to VIM
    rst, rcv_msg = recv_msg(conn)
    if rst == False:
        nlog.debug("Error : receive message from VIM")
        return False, None

    return True, rcv_msg


'''
class httpclient():
    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
        return

    def conn_httpserver(self, host=None, port=0):
        if (host == None) | (port == 0):
            nlog.error("Error : Invalid parameter(host = %s, port = %d)", host, port)
            return False, None

#        data_str = host + ':' + str(port)
        try:
            connection = httplib.HTTPConnection(host, port)
            self.conn = connection
        except httplib.HTTPException as e:
            nlog.error("Error : %s", e.args[0])
            return False, None

        return True, connection

    def send_msg(self, method=None, uri=None, message=None):
        if (method == None) | (uri == None) | (message == None):
            nlog.error("Error : Invalid parameter(method = %s, uri = %s, message = %s)", method, uri, message)
            return False

        try:
            json_msg = json.dumps(message)
            self.conn.request(method, uri, json_msg, self.headers)
        except:
            nlog.error("Error : send_msg")
#            nlog.error("Error : %s", e.args[0])
            return False

        return True

    def recv_msg(self):
        try:
            response = self.conn.getresponse()
            data = response.read()
        except httplib.HTTPException as e:
            nlog.error("Error : %s", e.args[0])
            return None

        return data
'''
