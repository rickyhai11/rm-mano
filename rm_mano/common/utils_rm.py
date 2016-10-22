import collections
import itertools
import six

from rm_mano.common import consts
from rm_mano.common import exceptions
from rm_mano.rm_monitor.sh_rm_monitoring import *
from rm_mano.global_info import *

def validate_resource_by_name(resource):
    # to do validate the quota limits
    if resource not in itertools.chain(consts.CINDER_QUOTA_FIELDS,
                                       consts.NOVA_QUOTA_FIELDS,
                                       consts.NEUTRON_QUOTA_FIELDS):
        raise exceptions.InvalidInputError


def validate_quota_limits(payload):
    for resource in payload:
        # Check valid resource name
        if resource not in itertools.chain(consts.CINDER_QUOTA_FIELDS,
                                           consts.NOVA_QUOTA_FIELDS,
                                           consts.NEUTRON_QUOTA_FIELDS):
            raise exceptions.InvalidInputError
        # Check valid quota limit value in case for put/post
        # TODO (ricky) implement constrains for input data
        # if isinstance(payload, dict) and (not isinstance(payload[resource], int) or payload[resource] <= 0):
        #     raise exceptions.InvalidInputError


def build_db_quota_limit(quotas):
    '''
    convert quota limit (dict: key as resource name and value as integer)
    to db format (key as columns and value as column values)
    :param quotas:
    :return:
    '''
    # validate input quotas
    validate_quota_limits(payload=quotas)

    quota = collections.defaultdict(dict)
    for resource, limit in quotas.iteritems():
        quota[resource] = collections.defaultdict(dict)
        quota[resource]['resource'] = resource
        quota[resource]['hard_limit'] = limit
        quota[resource]['allocated'] = 0
    print quota
    return quota


def build_db_usage_limit(resources, label_update):
    '''
    convert resource usage (dict: key as resource name and value as integer)
    to DB format (key as columns and value as column values)
    :param resources: dict {'cpus': 10, 'memory': 1024}
    :param label_update: enum (in_use or reserved)
    :return:usage (dict)
    {'vcpus' : {'resource': 'vcpus', 'in_use': 10}}
    OR
    {'vcpus' : {'resource': 'vcpus', 'reserved': 10}}
    '''
    # TODO (ricky) not tested yet
    # validate input resources
    validate_quota_limits(payload=resources)

    usage = collections.defaultdict(dict)
    for resource, limit in resources.iteritems():
        usage[resource] = collections.defaultdict(dict)
        usage[resource]['resource'] = resource
        # if label == in_use, convert resource dict to usage dict that included 'in_use' field
        # update 'in_use' field only
        if label_update == 'in_use':
            usage[resource]['in_use'] = limit
        # if label == reserved, convert resource dict to usage dict that included 'reserved' field
        # update 'reserved' field only
        if label_update == 'reserved':
            usage[resource]['reserved'] = limit
    print usage
    return usage


def build_output_quota_limit(db_quotas):
    # convert quotas limit from db format to output format that will be response to api request
    # input quotas (db format):
    # quotas_db = {'uuid': '1234dsd', 'project_id': 'af10gh', 'resource': 'vcpus', 'hard_limit': 10}
    #
    # desired output format for quotas = {'vcpus': 8, 'vnfs': 10}
    out_quotas = {}
    k = db_quotas['resource']
    v = db_quotas['hard_limit']
    out_quotas[k] = v
    # out_quotas['project_id'] = db_quotas['project_id']
    return out_quotas


def build_output_resource_usage(db_resource_usage):
    # db_resource_usage= {'deleted_at': None, 'resource': 'port', 'uuid': '8b36d48f-903d-11e6-b184-0050568b49a9',
    # 'user_id': None, 'created_at': None, 'in_use': 0L, 'updated_at': datetime.datetime(2016, 10, 12, 14, 13, 14),
    # 'until_refresh': 0, 'reserved': 0L, 'project_id': '25970fbcfb0a4c2fb42ccc18f1bccde3'}
    #
    # convert from db format to output format for api request
    #
    # get resource name
    resource = db_resource_usage['resource']

    # initiate dict for resource
    out_usage = collections.defaultdict(dict)
    out_usage[resource] = collections.defaultdict(dict)

    # convert data format
    out_usage[resource]['project_id'] = db_resource_usage['project_id']
    out_usage[resource]['user_id'] = db_resource_usage['user_id']
    out_usage[resource]['resource'] = db_resource_usage['resource']
    out_usage[resource]['in_use'] = db_resource_usage['in_use']
    out_usage[resource]['reserved'] = db_resource_usage['reserved']
    out_usage[resource]['until_refresh'] = db_resource_usage['until_refresh']

    return out_usage


def build_visible_quota_at_vim(quota_set):
    # convert to quota name that is used at vim (openstack)
    # because some quotas are renamed from original name (at vim)
    # such as: vcpu-cores ; ram-vmemory; vnfs-instances
    #
    # quota_set: dict-with key as resource name and value as value of resource (integer)
    quota_map = [
        # compute quota
        "metadata_items", "cores", "instances", "ram", "key_pairs",
        "floating_ips", "fixed_ips", "injected_files", 'injected_file_path_bytes',
        'injected_file_content_bytes', 'security_groups', 'security_group_rules',
        'server_groups', 'server_group_members'
        # cinder quota
                         "volumes", "snapshots", "gigabytes", "backups", "backup_gigabytes",
        # neutron quota
        "network", "subnet", "port", "router", "floatingip", "security_group", "security_group_rule"]

    different_quota_map = {'vcpus': 'cores', 'vnfs': 'instances', 'vmemory': 'ram'}

    ret = {}
    # only return visible quota items
    for k, v in quota_set.iteritems():
        if k in quota_map:
            ret[k] = v
            pass
        else:
            for display_name, key_vim in different_quota_map.items():
                if k == display_name:
                    ret[key_vim] = v
    return ret


def build_visible_resources_at_nfvo(vim_resources):
    # mapping resources that are got from vim (openstack) to resource that are renamed to use at nfvo db
    # because some resource are renamed from original name (at vim)
    # such as: vcpu-cores ; ram-vmemory; vnfs-instances
    #
    # resources: dict-with key as resource name and value as integer from vim

    resources_map = [
        # compute quota
        "metadata_items", "vcpus", "vnfs", "vmemory", "key_pairs",
        "floating_ips", "fixed_ips", "injected_files", 'injected_file_path_bytes',
        'injected_file_content_bytes', 'security_groups', 'security_group_rules',
        'server_groups', 'server_group_members'
        # cinder quota
                         "volumes", "snapshots", "gigabytes", "backups", "backup_gigabytes",
        # neutron quota
        "network", "subnet", "port", "router", "floatingip", "security_group", "security_group_rule"]

    different_quota_map = {'cores': 'vcpus', 'instances': 'vnfs', 'ram': 'vmemory'}

    ret = {}
    # only return visible quota items
    for k, v in vim_resources.iteritems():
        if k in resources_map:
            ret[k] = v
            pass
        else:
            for display_name, key_vim in different_quota_map.items():
                if k == display_name:
                    ret[key_vim] = v
    return ret


def resource_calculation(current_value, acquired_value, action):
    # to calculate resource whether resource usage is increased or decreased
    '''
        to calculate resource whether resource usage is increased or decreased
        :param current_value: current value that is being stored in db
        :param acquired_value: required resource value that needed to be increased or decreased
        :param action: (string) (ADD,UPDATE,DELETE, SYNC)
        :return:
        '''

    if action == 'ADD' or action == 'UPDATE':
        cal_usage = current_value + acquired_value
        return cal_usage

    elif action == 'DELETE':
        cal_usage = current_value - acquired_value
        return cal_usage

    elif action == 'SYNC':
        if current_value > acquired_value:
            cal_usage = acquired_value  # TODO (ricky) need to re-consider formula
            return cal_usage
        elif current_value == acquired_value:
            cal_usage = current_value
            return cal_usage
        # current resource could be lower then actual vim usage as 'in_use' in nfvo db did not include
        # reserved resources, but otherwise 'in_use' from vim that already included 'reserved' when a reservation
        # had been started (start time arrived)
        elif current_value < acquired_value:
            # cal_usage =  TODO (ricky) need to re-consider formula that involve to reservation
            return

    else:
        nlog.error("ERROR: utils_rm.resource_calculation() - Failed to calculate resource usage")
        return False, None


#
# currently Un-used code
#################################


def get_batch_projects(batch_size, project_list, fillvalue=None):
    # Returns a iterator of tuples containing batch_size number of objects in each
    # look at this link to see what happened
    # http://stackoverflow.com/questions/28847334/how-to-unserstand-the-code-using-izip-longest-to-chunk-a-list
    args = [iter(project_list)] * batch_size
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def build_absolute_limits(quotas):

    quota_map = {
        'maxTotalRAMSize': 'vmemory',
        'maxTotalInstances': 'vnfs',
        'maxTotalCores': 'vcpus',
        'maxTotalKeypairs': 'key_pairs',
        'maxTotalFloatingIps': 'floating_ips',
        'maxPersonality': 'injected_files',
        'maxPersonalitySize': 'injected_file_content_bytes',
        'maxSecurityGroups': 'security_groups',
        'maxSecurityGroupRules': 'security_group_rules',
        'maxServerMeta': 'metadata_items',
        'maxServerGroups': 'server_groups',
        'maxServerGroupMembers': 'server_group_members',
    }

    limits = {}
    for display_name, key in six.iteritems(quota_map):
        if key in quotas:
            limits[display_name] = quotas[key]['limit']
    return limits


def build_used_limits(quotas):

    quota_map = {
        'totalRAMUsed': 'vmemory',
        'totalCoresUsed': 'vcpus',
        'totalInstancesUsed': 'vnfs',
        'totalFloatingIpsUsed': 'floating_ips',
        'totalSecurityGroupsUsed': 'security_groups',
        'totalServerGroupsUsed': 'server_groups',
    }

    # need to refresh usage from the bottom pods? Now from the data in top
    used_limits = {}
    for display_name, key in six.iteritems(quota_map):
        if key in quotas:
            reserved = quotas[key]['reserved']
            used_limits[display_name] = quotas[key]['in_use'] + reserved

    return used_limits


#
# added 2016-10-16
#


def validate_required_fields_set(body, fields):
    for field in fields:
        if field not in body:
            return False
    return True


TRUE_STRINGS = ('1', 't', 'true', 'on', 'y', 'yes')
FALSE_STRINGS = ('0', 'f', 'false', 'off', 'n', 'no')


def is_valid_boolstr(val):
    """Check if the provided string is a valid bool string or not."""
    val = str(val).lower()
    return (val in TRUE_STRINGS) or (val in FALSE_STRINGS)


def bool_from_string(subject, strict=False, default=False):
    """Interpret a string as a boolean.

    A case-insensitive match is performed such that strings matching 't',
    'true', 'on', 'y', 'yes', or '1' are considered True and, when
    `strict=False`, anything else returns the value specified by 'default'.
    Useful for JSON-decoded stuff and config file parsing.
    If `strict=True`, unrecognized values, including None, will raise a
    ValueError which is useful when parsing values passed in from an API call.
    Strings yielding False are 'f', 'false', 'off', 'n', 'no', or '0'.
    """

    if not isinstance(subject, six.string_types):
        subject = six.text_type(subject)

    lowered = subject.strip().lower()

    if lowered in TRUE_STRINGS:
        return True
    elif lowered in FALSE_STRINGS:
        return False
    elif strict:
        acceptable = ', '.join(
            "'%s'" % s for s in sorted(TRUE_STRINGS + FALSE_STRINGS))
        msg = _("Unrecognized value '%(val)s', acceptable values are:"
                " %(acceptable)s") % {'val': subject,
                                      'acceptable': acceptable}
        raise ValueError(msg)
    else:
        return default


def check_string_length(value, name=None, min_len=0, max_len=None):
    """Check the length of specified string

    :param value: the value of the string
    :param name: the name of the string
    :param min_len: the minimum length of the string
    :param max_len: the maximum length of the string

    """
    if not isinstance(value, six.string_types):
        if name is None:
            msg = rmlog.error("The input is not a string or unicode")
        else:
            msg = rmlog.error("%s is not a string or unicode") % name
        raise exceptions.InvalidInput(message=msg)

    if name is None:
        name = value

    if len(value) < min_len:
        msg = rmlog.error("%(name)s has a minimum character requirement of "
                "%(min_length)s.") % {'name': name, 'min_length': min_len}
        raise exceptions.InvalidInput(message=msg)

    if max_len and len(value) > max_len:
        msg = rmlog.error("%(name)s has more than %(max_length)s "
                "characters.") % {'name': name, 'max_length': max_len}
        raise exceptions.InvalidInput(message=msg)
