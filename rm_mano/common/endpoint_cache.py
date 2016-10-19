
import collections

from keystoneclient.auth.identity import v3 as auth_identity
from keystoneclient.auth import token_endpoint
from keystoneclient import session
from keystoneclient.v3 import client as keystone_client
from oslo_config import cfg

config = {
    'VERSION': '2.1',
    'AUTH_URL': "http://116.89.184.94:5000/v3",
    'USERNAME': "admin",
    'PASSWORD': "fncp2015",
    'TENANT_ID': "f4211c8eee044bfb9dea2050fef2ace5",
    'TENANT_NAME': "admin",
    'admin_user_domain_name': 'Default',
    'admin_project_domain_name': 'Default'}

class EndpointCache(object):
    def __init__(self):
        self.endpoint_map = collections.defaultdict(dict)
        self.admin_session = None
        self.keystone_client = None
        self._update_endpoints()

    @staticmethod
    def _get_admin_token(self):
        auth = auth_identity.Password(
            auth_url=config['AUTH_URL'],
            username=config['USERNAME'],
            password=config['PASSWORD'],
            project_name=config['TENANT_NAME'],
            user_domain_name=config['admin_user_domain_name'],
            project_domain_name=config['admin_project_domain_name'])
        sess = session.Session(auth=auth)
        self.admin_session = sess
        return sess.get_token()

    # refer to http://docs.openstack.org/developer/keystone/api_curl_examples.html for details
    @staticmethod
    def _get_endpoint_from_keystone(self):
        auth = token_endpoint.Token(config['AUTH_URL'],
                                    EndpointCache._get_admin_token(self))
        sess = session.Session(auth=auth)
        cli = keystone_client.Client(session=sess)
        self.keystone_client = cli

        service_id_name_map = {}
        for service in cli.services.list():
            service_dict = service.to_dict()
            # map id of service (playnetmano_rm service which was registered with keystone) to proper service name
            # such as: "27365273672= playnetmano_rm"
            service_id_name_map[service_dict['id']] = service_dict['name']

        # http://docs.openstack.org/developer/keystone/api_curl_examples.html-searching endpoint
        # to see endpoints example
        region_service_endpoint_map = {}
        for endpoint in cli.endpoints.list():
            endpoint_dict = endpoint.to_dict()
            if endpoint_dict['interface'] != 'public':
                continue
            region_id = endpoint_dict['region']
            service_id = endpoint_dict['service_id']
            url = endpoint_dict['url']
            service_name = service_id_name_map[service_id]
            if region_id not in region_service_endpoint_map:
                region_service_endpoint_map[region_id] = {}
            region_service_endpoint_map[region_id][service_name] = url
        return region_service_endpoint_map

    def _get_endpoint(self, region, service, retry):
        if service not in self.endpoint_map[region]:
            if retry:
                self.update_endpoints()
                return self._get_endpoint(region, service, False)
            else:
                return ''
        else:
            return self.endpoint_map[region][service]

    def _update_endpoints(self):
        endpoint_map = EndpointCache._get_endpoint_from_keystone(self)

        for region in endpoint_map:
            for service in endpoint_map[region]:
                self.endpoint_map[region][
                    service] = endpoint_map[region][service]

    def get_endpoint(self, region, service):
        """Get service endpoint url

        :param region: region the service belongs to
        :param service: service type
        :return: url of the service
        """
        return self._get_endpoint(region, service, True)

    def update_endpoints(self):
        """Update endpoint cache from Keystone

        :return: None
        """
        self._update_endpoints()

    def get_all_regions(self):
        """Get region list

        return: List of regions
        """
        return self.endpoint_map.keys()
