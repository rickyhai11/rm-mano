import logging

nlog = logging.getLogger('nfvo')
vlog = logging.getLogger('vnfm')
rmlog = logging.getLogger('rm')

config_file = 'playnetmanod.cfg'

##
# HTTP Status Code
##
HTTP_OK = 200

HTTP_Bad_Request = 400
HTTP_Unauthorized = 401
HTTP_Not_Found = 404
HTTP_Method_Not_Allowed = 405
HTTP_Not_Acceptable = 406
HTTP_Request_Timeout = 408
HTTP_Conflict = 409

HTTP_Playnet_Fail = 440     # Unassigned HTTP Error Code : 432 ~ 450

HTTP_Internal_Server_Error = 500
HTTP_Service_Unavailable = 503


