
import itertools
import six

from sh_layer.common import consts
from sh_layer.common import exceptions
from sh_layer.rm_monitor.sh_rm_monitoring import *
from sh_layer.global_info import *


# Returns a iterator of tuples containing batch_size number of objects in each
def get_batch_projects(batch_size, project_list, fillvalue=None):
    # look at this link to see what happened
    # http://stackoverflow.com/questions/28847334/how-to-unserstand-the-code-using-izip-longest-to-chunk-a-list
    args = [iter(project_list)] * batch_size
    return itertools.izip_longest(fillvalue=fillvalue, *args)


# to do validate the quota limits
def validate_resource_by_name(resource):
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

def _build_visible_quota(quota_set):
    quota_map = [
        'id', 'instances', 'ram', 'cores', 'key_pairs',
        'floating_ips', 'fixed_ips',
        'injected_files', 'injected_file_path_bytes',
        'injected_file_content_bytes',
        'security_groups', 'security_group_rules',
        'metadata_items', 'server_groups', 'server_group_members',
    ]

    ret = {}
    # only return Nova visible quota items
    for k, v in quota_set.iteritems():
        if k in quota_map:
            ret[k] = v

    return ret


def build_absolute_limits(quotas):

    quota_map = {
        'maxTotalRAMSize': 'memory',
        'maxTotalInstances': 'vnfs',
        'maxTotalCores': 'vcpus',
        'maxTotalKeypairs': 'key_pairs',
        'maxTotalFloatingIps': 'floating_ip',
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
        'totalRAMUsed': 'memory',
        'totalCoresUsed': 'vcpus',
        'totalInstancesUsed': 'vnfs',
        'totalFloatingIpsUsed': 'floating_ip',
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

def load_flavors_from_vim(flavor_id):
    '''
    loading flavor details directly from vim (openstack)
    :param flavor_id:
    :return: a dict - all details about required resources for that flavor
    '''
    nova_client = get_nova_client('admin')
    flavor_list = nova_client.flavors.list(detailed=True)
    flavor_details = {}

    for flavor in flavor_list:
        if int(flavor.id) == int(flavor_id):
            # flavor_details['name'] = flavor.name
            # flavor_details['uuid'] = flavor.id
            flavor_details['vcpus'] = flavor.vcpus
            flavor_details['memory'] = flavor.ram
            flavor_details['gigabytes'] = flavor.disk
            return flavor_details
        else:
            print "flavor %s is not existing in VIM (Openstack)" % flavor_id
            return False


def build_db_quota_limit(quotas):
        '''
        build quota limit dict to store in DB
        :param quotas:
        :return:
        '''
        # validate input quotas
        validate_quota_limits(payload=quotas)
        #
        quota = collections.defaultdict(dict)
        for resource, limit in quotas.iteritems():
            quota[resource] = collections.defaultdict(dict)
            quota[resource]['resource'] = resource
            quota[resource]['hard_limit'] = limit
            quota[resource]['allocated'] = 0
        print quota
        return quota

# convert quotas limit from db format to output format that will be response to api request
# input quotas (db format):
# quotas_db = {'uuid': '1234dsd', 'project_id': 'af10gh', 'resource': 'vcpus', 'hard_limit': 10}
#
# desired output format for quotas = {'vcpus': 8, 'vnfs': 10}
def build_output_quota_limit(db_quotas):
    out_quotas = {}
    k = db_quotas['resource']
    v = db_quotas['hard_limit']
    out_quotas[k] = v
    # out_quotas['project_id'] = db_quotas['project_id']
    return out_quotas

# db_resource_usage= {'deleted_at': None, 'resource': 'port', 'uuid': '8b36d48f-903d-11e6-b184-0050568b49a9',
# 'user_id': None, 'created_at': None, 'in_use': 0L, 'updated_at': datetime.datetime(2016, 10, 12, 14, 13, 14),
# 'until_refresh': 0, 'reserved': 0L, 'project_id': '25970fbcfb0a4c2fb42ccc18f1bccde3'}
#
# convert from db format to output format for api request
def build_output_resource_usage(db_resource_usage):
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