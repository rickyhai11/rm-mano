import sys

import todo
import resource_db

import vimconn
import json
import time

from novaclient import client as nClient, exceptions as nvExceptions
import keystoneclient.v2_0.client as ksClient
import keystoneclient.exceptions as ksExceptions
import glanceclient.v2.client as glClient
import glanceclient.client as gl1Client
import glanceclient.exc as gl1Exceptions
from httplib import HTTPException
from neutronclient.neutron import client as neClient
from neutronclient.common import exceptions as neExceptions
from requests.exceptions import ConnectionError


class sh_reservation():
    def __init__(self):
        todo

    def create_resercation(self):
        todo


    def delete_reservation(self):
        todo


    def update_reservation(self):
        todo

    def list_rsv_by_id(self):

        todo



class sh_control():

    def __init__(self):
        return

    def start_time_trigger(self):
        nproject = vimconnector(uuid="", name="", tenant="admin", url="http://223.194.33.74:5000/v2.0",
                                                  url_admin="", user="admin", passwd="zz")
        # con_op =nproject._reload_connection_tenant('admin')
        # nova = self.nova.servers.create
        nproject.new_project_vapp(project_id='admin', image_id='19f7025b-b78a-4bf0-bc37-0cba68e16b10',
                                  network_id='f3d72a2d-1a56-46e6-b0f7-bda7ca87788e',
                                  description='vm_test01')



    def end_time_trigger(self):
        todo


'''
This class is implemented for iteracting with openstack (VIM)
'''
class vimconnector(vimconn.vimconnector):
    def __init__(self, uuid, name, tenant, url, url_admin=None, user=None, passwd=None, debug=True, config={}):
        '''using common constructor parameters. In this case
        'url' is the keystone authorization url,
        'url_admin' is not use
        '''
        vimconn.vimconnector.__init__(self, uuid, name, tenant, url, url_admin, user, passwd, debug, config)

        self.k_creds={}
        self.n_creds={}
        if not url:
            raise TypeError, 'url param can not be NoneType'
        self.k_creds['auth_url'] = url
        self.n_creds['auth_url'] = url
        if tenant:
            self.k_creds['tenant_name'] = tenant
            self.n_creds['project_id']  = tenant
        if user:
            self.k_creds['username'] = user
            self.n_creds['username'] = user
        if passwd:
            self.k_creds['password'] = passwd
            self.n_creds['api_key']  = passwd
        self.reload_client       = True

    def __setitem__(self, index, value):
        '''Set individuals parameters
        Throw TypeError, KeyError
        '''
        if index=='tenant':
            self.reload_client=True
            self.tenant = value
            if value:
                self.k_creds['tenant_name'] = value
                self.n_creds['project_id'] = value
            else:
                del self.k_creds['tenant_name']
                del self.n_creds['project_id']
        elif index=='user':
            self.reload_client = True
            self.user = value
            if value:
                self.k_creds['username'] = value
                self.n_creds['username'] = value
            else:
                del self.k_creds['username']
                del self.n_creds['username']
        elif index=='passwd':
            self.reload_client=True
            self.passwd = value
            if value:
                self.k_creds['password'] = value
                self.n_creds['api_key']  = value
            else:
                del self.k_creds['password']
                del self.n_creds['api_key']
        elif index=='url':
            self.reload_client=True
            self.url = value
            if value:
                self.k_creds['auth_url'] = value
                self.n_creds['auth_url'] = value
            else:
                raise TypeError, 'url param can not be NoneType'
        else:
            vimconn.vimconnector.__setitem__(self,index, value)

    def _reload_connection(self):
        '''Called before any operation, it check if credentials has changed
        Throw keystoneclient.apiclient.exceptions.AuthorizationFailure
        '''
        #TODO control the timing and possible token timeout, but it seams that python client does this task for us :-)
        if self.reload_client:
            #test valid params
            if len(self.n_creds) <4:
                raise ksExceptions.ClientException("Not enough parameters to connect to openstack")
            self.nova = nClient.Client(2, **self.n_creds)
            self.keystone = ksClient.Client(**self.k_creds)
            self.glance_endpoint = 'http://223.194.33.74:9292'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            self.glance = glClient.Client(self.glance_endpoint, token=self.keystone.auth_token, **self.k_creds)  #TODO check k_creds vs n_creds
            self.ne_endpoint = 'http://223.194.33.74:9696'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.ne_endpoint=self.keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
            self.neutron = neClient.Client('2.0', endpoint_url=self.ne_endpoint, token=self.keystone.auth_token, **self.k_creds)
            self.reload_client = False


    def _reload_connection_tenant(self,project_iid):
        '''Called before any operation, it check if credentials has changed
        Throw keystoneclient.apiclient.exceptions.AuthorizationFailure
        '''
        #TODO control the timing and possible token timeout, but it seams that python client does this task for us :-)
        self.__setitem__('tenant', project_iid)

        if self.reload_client:
            #test valid params b n
            if len(self.n_creds) <4:
                raise ksExceptions.ClientException("Not enough parameters to connect to openstack")
            self.nova = nClient.Client(2, **self.n_creds)
            self.keystone = ksClient.Client(**self.k_creds)
            self.glance_endpoint = 'http://210.114.94.20:9292'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            self.glance = glClient.Client(self.glance_endpoint, token=self.keystone.auth_token, **self.k_creds)  #TODO check k_creds vs n_creds
            self.ne_endpoint = 'http://210.114.94.20:9696'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.ne_endpoint=self.keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
            self.neutron = neClient.Client('2.0', endpoint_url=self.ne_endpoint, token=self.keystone.auth_token, **self.k_creds)
            self.reload_client = False


    def new_project_vapp(self,project_id, image_id,network_id, description):
        '''Adds a VM instance to VIM
            Params:
            start: indicates if VM must start or boot in pause mode. Ignored
            image_id,flavor_id: iamge and flavor uuid
            net_list: list of interfaces, each one is a dictionary with:
                name:
                net_id: network uuid to connect
                vpci: virtual vcpi to assign, ignored because openstack lack #TODO
                model: interface model, ignored #TODO
                mac_address: used for  SR-IOV ifaces #TODO for other types
                use: 'data', 'bridge',  'mgmt'
                type: 'virtual', 'PF', 'VF', 'VFnotShared'
                vim_id: filled/added by this function
                #TODO ip, security groups
            Returns >=0, the instance identifier
                <0, error_text
        '''

        if self.debug:
            print "osconnector: Creating VM into VIM"
           # print "   image %s  flavor %s   nics=%s" %(image_id, flavor_id,net_list)


            self._reload_connection_tenant(project_id)
            image = self.nova.images.find(id=image_id)
            nflavor = self.nova.flavors.find(name="m1.tiny")
            #network = self.nova.networks.find(label="Management_Network")
            server = self.nova.servers.create(name=image.name, image = image.id, flavor = nflavor.id, nics = [{'net-id':network_id}], key_name = "")
            time.sleep(2)
            server_f = self.nova.servers.get(server.id)
            ip = str(server_f.networks.values()).strip('[u]\'')
            print ip
            print "====================================================="
            return 200, server.id, image.name, ip

        else:
            return 400, project_id, "error"


    def get_tenant_vminstance(self,vm_id):
        '''this function could be reused for getting instance_id from openstack (VIM). Returns the VM instance information from VIM'''
        if self.debug:
            print "osconnector: Getting VM from VIM"
        try:
            self._reload_connection()
            server = self.nova.servers.find(id=vm_id)
            #TODO parse input and translate to VIM format (playnetmano_schemas.new_vminstance_response_schema)
            return 1, {"server": server.to_dict()}
        except nvExceptions.NotFound, e:
            error_value=-vimconn.HTTP_Not_Found
            error_text= "vm instance %s not found" % vm_id
        except (ksExceptions.ClientException, nvExceptions.ClientException), e:
            error_value=-vimconn.HTTP_Bad_Request
            error_text= type(e).__name__ + ": "+  (str(e) if len(e.args) == 0 else str(e.args[0]))
        #TODO insert exception vimconn.HTTP_Unauthorized
        #if reaching here is because an exception
        if self.debug:
            print "get_tenant_vminstance " + error_text
        return error_value, error_text



if __name__ == '__main__':
    start_vnf = sh_control()
    start_vnf.start_time_trigger()



