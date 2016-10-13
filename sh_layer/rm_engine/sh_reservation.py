'''
Reservation, All function are related to reservation service should be implemented here and they are used by
NFVO API or RM API modules
'''

import datetime
import time

import glanceclient.v2.client as glClient
import keystoneclient.exceptions as ksExceptions
import keystoneclient.v2_0.client as ksClient
from neutronclient.neutron import client as neClient
from novaclient import client as nClient, exceptions as nvExceptions

from sh_layer.drivers import vimconn
from sh_layer.rm_engine.sh_quota_manager import check_user_compute_capacity
from utils import todo


class sh_reservation():
    def __init__(self):
        todo

    def create_reservation(self, nfvodb, rsv_content):
        print "Checking available resources. Please be patient..."
        rp = check_user_compute_capacity(mydb=nfvodb, rsv=rsv_content)
        if rp:
            result = nfvodb.add_row_rs('reservation', rsv_content)
            if result > 0:
                print "created reservation successfully "
                return result
        else:
            print 'Resources error occurred: resources are exhausted. Please recheck'

    def delete_reservation(self, table, nfvodb, reservation_id):
        result = nfvodb.delete_row_by_rsv_id(table=table, reservation_id=reservation_id)
        if result > 0:
            print "deleted successfully a reservation with reservation_id: %s in table %s" % (reservation_id, table)
            return result, reservation_id

    def update_reservation(self, nfvodb, reservation_id, new_values_dict):
        result, reservation_id = nfvodb.update_reservation_for_project(table_name='reservation', reservation_id=reservation_id,
                                                                       new_values_dict=new_values_dict)
        if result > 0:
            print "sh_reservation.update_reservation() - updated reservation successfully"
            return result, reservation_id

    def update_time_stamp_reservation(self, nfvodb, reservation_id, start_time, end_time):
        result = nfvodb.update_row_timestamp_by_rsv_id(table_name='reservation', reservation_id=reservation_id,
                                                       start_time=start_time, end_time=end_time)
        if result > 0:
            print "updated starting time and ending time successfully for reservation_id: %s" % reservation_id
            return result, reservation_id

    def list_rsv_by_id(self):
        todo

    def list_all_created_rsv(self, nfvodb):
            list_created_rsv = nfvodb.get_rsv_by_status(status='ACTIVE')
            print list_created_rsv
            return list_created_rsv

def reservation_expire(context):
    return

class sh_control():

    def __init__(self):
        todo

    def start_time_trigger(self, nfvodb):
        nproject = vimconnector(uuid="", name="", tenant="admin", url="http://129.254.39.209:5000/v2.0",
                                                  url_admin="", user="admin", passwd="fncp2015")
        reservations = sh_reservation()
        print "start_time_trigger process is running"
        rsv_vnf_auth_dict = {}
        while True:
            rsvs = reservations.list_all_created_rsv(nfvodb)
            for rsv in rsvs:
                print rsv
                start_time = rsv['start_time']
                image_id = rsv['image_id']
                network_id = rsv['network_id']
                if (abs(start_time - datetime.datetime.now()) < datetime.timedelta(minutes=1)):
                    res, vnf_id, image_name, assigned_ip = nproject.new_project_vapp(project_id='admin',
                        image_id=image_id,
                            network_id=network_id,
                                description='vm_test01')
                    time.sleep(2)
                    # initiate rsv_vnf_auth_dict to insert into rsv_vnf_auth_rm DB table after vnf is created and vnf_id has been returned
                    rsv_vnf_auth_dict['reservation_id'] = rsv['reservation_id']
                    rsv_vnf_auth_dict['vnf_id'] = vnf_id
                    print "Print out rsv_vnf_auth_dict:"
                    print rsv_vnf_auth_dict
                    nfvodb.add_row_rs(table_name='rsv_vnf_auth_rm', row_dict=rsv_vnf_auth_dict)
                    print "Created vnf successfully"
            time.sleep(100)


    def end_time_trigger(self, nfvodb):

        nproject = vimconnector(uuid="", name="", tenant="admin", url="http://129.254.39.209:5000/v2.0",
                                                  url_admin="", user="admin", passwd="fncp2015")
        reservations = sh_reservation()
        print "end_time_trigger process is running"
        while True:
            rsvs = reservations.list_all_created_rsv(nfvodb)
            for rsv in rsvs:
                print rsv
                end_time = rsv['end_time']
                reservation_id = rsv['reservation_id']
                listed, row = nfvodb.get_rsv_by_id(table_name='rsv_vnf_auth_rm', reservation_id=reservation_id)
                vnf_id = row['vnf_id']
                if (abs(end_time - datetime.datetime.now()) <= datetime.timedelta(minutes=1)):
                    nproject.delete_vapp(vnf_id)
                    time.sleep(3)
                    reservations.delete_reservation(nfvodb=nfvodb, table='reservation', reservation_id=reservation_id)
                    reservations.delete_reservation(nfvodb=nfvodb, table='rsv_vnf_auth_rm', reservation_id=reservation_id)

                    break
            time.sleep(2)


# '''
# This class is implemented for interacting with openstack (VIM)
# '''
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
        self.reload_client = True

    def __setitem__(self, index, value):
        '''Set individuals parameters
        Throw TypeError, KeyError
        '''
        if index == 'tenant':
            self.reload_client=True
            self.tenant = value
            if value:
                self.k_creds['tenant_name'] = value
                self.n_creds['project_id'] = value
            else:
                del self.k_creds['tenant_name']
                del self.n_creds['project_id']
        elif index == 'user':
            self.reload_client = True
            self.user = value
            if value:
                self.k_creds['username'] = value
                self.n_creds['username'] = value
            else:
                del self.k_creds['username']
                del self.n_creds['username']
        elif index == 'passwd':
            self.reload_client=True
            self.passwd = value
            if value:
                self.k_creds['password'] = value
                self.n_creds['api_key']  = value
            else:
                del self.k_creds['password']
                del self.n_creds['api_key']
        elif index == 'url':
            self.reload_client=True
            self.url = value
            if value:
                self.k_creds['auth_url'] = value
                self.n_creds['auth_url'] = value
            else:
                raise TypeError, 'url param can not be NoneType'
        else:
            vimconn.vimconnector.__setitem__(self, index, value)

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
            self.glance_endpoint = 'http://223.194.33.59:9292'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            self.glance = glClient.Client(self.glance_endpoint, token=self.keystone.auth_token, **self.k_creds)  #TODO check k_creds vs n_creds
            self.ne_endpoint = 'http://223.194.33.59:9696'
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


    def delete_vapp(self,vapp_id):
        if self.debug:
            print "osconnector: Deleting  a  tenant from VIM"
        try:
          #  print tenant_id + " " + mgnt_network_id + " " +  ctrl_network_id + " " + " " + EMA_iid
            self._reload_connection()

            self.nova.servers.delete(vapp_id)
            time.sleep(7)
            #subnetm = self.neutron.list_subnets(network_id = mgnt_network_id)['subnets'][0]
            #router = self.neutron.list_routers(name = 'management-ext')['routers'][0]
            #self.neutron.remove_interface_router(router['id'], { 'subnet_id' : subnetm['id'] } )
            #self.neutron.remove_gateway_router(router['id'])
            #self.neutron.delete_router(router_id)

            #self.neutron.delete_network(mgnt_network_id)

            #self.keystone.tenants.add_user(self.k_creds["username"], #role)
            return 200, vapp_id
        except ksExceptions.ConnectionError, e:
            error_value=-vimconn.HTTP_Bad_Request
            error_text= type(e).__name__ + ": "+  (str(e) if len(e.args)==0 else str(e.args[0]))
        except ksExceptions.ClientException, e: #TODO remove
            error_value=-vimconn.HTTP_Bad_Request
            error_text= type(e).__name__ + ": "+  (str(e) if len(e.args)==0 else str(e.args[0]))
        #TODO insert exception vimconn.HTTP_Unauthorized
        #if reaching here is because an exception
        if self.debug:
            print "delete_tenant " + error_text
        return error_value, error_text


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
            print "get_tenant_vminstance" + error_text
        return error_value, error_text

