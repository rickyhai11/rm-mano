import sys

import todo

import resource_db
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

    def start_time_trigger(self):
        todo

    def end_time_trigger(self):
        todo





class vim_connector():

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
            self.glance_endpoint = 'http://210.114.94.20:9292'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.glance_endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            self.glance = glClient.Client(self.glance_endpoint, token=self.keystone.auth_token, **self.k_creds)  #TODO check k_creds vs n_creds
            self.ne_endpoint = 'http://210.114.94.20:9696'
           #endpoint fixed(2015.12.02) if changed infra return again
           #self.ne_endpoint=self.keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
            self.neutron = neClient.Client('2.0', endpoint_url=self.ne_endpoint, token=self.keystone.auth_token, **self.k_creds)
            self.reload_client = False




