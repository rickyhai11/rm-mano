import todo
# from resource_db import resource_db as rdb
import resource_db as rdb
import vimconn
from multiprocessing import Process

import sys
import json
import time
import datetime

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

global data
data = {'reservation_id': '12345',
        'label': 'test3',
        'host': "hai_compute_3",
        'user': 'hainguyen_3',
        'project': 'admin',
        'start_time': '2016-05-03 00:59:00',
        'end_time': '2016-05-03 01:05:00',
        'flavor_id': '1',
        'image_id': '80b5f1d7-ba4d-43a6-85b4-7bf8429e9032',
        'instance_id': 'null',   # this attribute need to be updated after instance is created (start_time arrived)
        'summary': 'reservation testing',
        'status': 'created'
        }
'''
Should consider to user array for status field
'''

vmem_capa= {'uuid': 3, "mem_total": 12, "vmem_total": 12, "vmem_used": 5, "mem_available": 5, "vmem_available": 6}

vcpu={'uuid': 13, "cpu_total": 15, "vcpu_total": 20, "vcpu_used": 10, "cpu_available": 8, "vcpu_available": 65}
            #"created_at": '2016-04-13 12:30:20', "modified_at": '2016-04-13 12:30:59' }
flavor_dict = {'flavor_id': 2, 'name': 'm.medium', 'ram': 1024, 'disk': 2, 'vcpu': 2}

image_dict = {'image_id': '19f7025b-b78a-4bf0-bc37-0cba68e16b10', 'name': 'ubuntu_01'}

class sh_reservation():
    def __init__(self):
        todo

    def create_reservation(self, data):
        rdb_ = rdb.resource_db()
        result = rdb_.add_row_rs('reservation', data)
        if result > 0:
            print "created reservation successfully "
            return result

    def delete_reservation(self, reservation_id):
        result = rdb.delete_row_by_rsv_id(table_name='reservation', reservation_id=reservation_id)
        if result > 0:
            print "deleted successfully a reservation with reservation_id: %s" % reservation_id
            return result, reservation_id


    def update_reservation(self, reservation_id, new_values_dict):
        result, reservation_id = rdb.update_row_rsv(table_name='reservation', reservation_id=reservation_id,
                                                    new_values_dict=new_values_dict)
        if result > 0:
            print "sh_reservation.update_reservation() - updated reservation successfully"
            return result, reservation_id

    def update_time_stamp_reservation(self, reservation_id, start_time, end_time):
        result = rdb.update_row_timestamp_by_rsv_id(table_name='reservation', reservation_id=reservation_id,
                                                    start_time=start_time, end_time=end_time)
        if result > 0:
            print "updated starting time and ending time successfully for reservation_id: %s" % reservation_id
            return result, reservation_id

    def list_rsv_by_id(self):

        todo
    def list_all_created_rsv(self):
            rdb_ = rdb.resource_db()
            list_created_rsv = rdb_.get_rsv_by_status(status='created')
            print list_created_rsv
            return list_created_rsv



class sh_control():

    def __init__(self):
        return

    def start_time_trigger(self):
        nproject = vimconnector(uuid="", name="", tenant="admin", url="http://223.194.33.59:5000/v2.0",
                                                  url_admin="", user="admin", passwd="secrete")
        reservations = sh_reservation()
        while True:
            rsvs = reservations.list_all_created_rsv()
            for rsv in rsvs:
                print rsv
                start_time = rsv['start_time']
                reservation_id = rsv['reservation_id']
                if (abs(start_time - datetime.datetime.now()) < datetime.timedelta(minutes=1)):
                    res, vapp_id, image_name, assigned_ip = nproject.new_project_vapp(project_id='admin',
                        image_id='80b5f1d7-ba4d-43a6-85b4-7bf8429e9032',
                            network_id='ebf2704c-bf50-4594-b429-4b3d6905074f',
                                description='vm_test01')
                    rdb_ = rdb.resource_db()  #call for resource_db() class
                    rdb_.update_row_vapp_id_by_rsv_id(table_name='reservation', reservation_id=reservation_id,
                                                      vapp_id=vapp_id)

                    print "created instance successfully"
            time.sleep(100)


    def end_time_trigger(self):
        nproject = vimconnector(uuid="", name="", tenant="admin", url="http://223.194.33.59:5000/v2.0",
                                                  url_admin="", user="admin", passwd="secrete")
        reservations = sh_reservation()
        while True:
            rsvs = reservations.list_all_created_rsv()
            for rsv in rsvs:
                print rsv
                start_time = rsv['end_time']
                vapp_id = rsv['instance_id']
                if (abs(start_time - datetime.datetime.now()) < datetime.timedelta(minutes=1)):
                    nproject.delete_vapp(vapp_id)
            time.sleep(100)

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
           # subnetm = self.neutron.list_subnets(network_id = mgnt_network_id)['subnets'][0]
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

def main_loop():
    # while 1:

        #run two functions in parallel like two threads
        # commands = ['start_vnf.start_time_trigger', 'start_vnf.end_time_trigger']
        # parallelpy.run(commands=commands)

    start_vnf = sh_control()
    p1 = Process(target=start_vnf.start_time_trigger)
    p1.start()
    print 'p1 started '
    p2 = Process(target=start_vnf.end_time_trigger)
    p2.start()
    print 'p2 started'
    p1.join()
    print 'p1 joined'
    p2.join()
    print 'p2 joined'



if __name__ == '__main__':
    sh_rsv = sh_reservation()
    create_rsv = sh_rsv.create_reservation(data=data)
    if create_rsv > 0:
        try:

            # db = resource_db.resource_db()
            # a = db.connect_db(host="localhost", user="root", passwd="S@igon0011", database="rm_db")
            main_loop()

        except KeyboardInterrupt:
            print >> sys.stderr, '\nExiting by user request.\n'
            sys.exit(0)

        # test = sh_reservation()
        # test.connect_db()


