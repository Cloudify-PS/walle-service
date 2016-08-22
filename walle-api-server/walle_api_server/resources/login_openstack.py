# Copyright (c) 2016 VMware. All rights reserved
from flask import make_response, g
from walle_api_server.resources import responses
from flask.ext import restful
from walle_api_server.common import util
import keystoneclient.v2_0.client as ksclient
from flask_restful_swagger import swagger
from walle_api_server.common import service_limit
import ceilometerclient.client
import novaclient.client
from datetime import datetime, timedelta


logger = util.setup_logging(__name__)


class LoginOpenStack(restful.Resource):
    @swagger.operation(
        responseClass=responses.LoginOpenStack,
        nickname="login_openstack",
        notes="Returns information for authorization in OpenStack.",
        parameters=[{'name': 'user',
                     'description': 'User login.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'password',
                     'description': 'User password.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant_name',
                     'description': 'tenant name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'auth_url',
                     'description': 'OpenStack keystore url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=['application/json']
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "username": {"type": "string", "minLength": 1},
             "password": {"type": "string", "minLength": 1},
             "auth_url": {"type": "string"},
             "tenant_name": {"type": "string"},
         },
         "required": ["username", "password", "auth_url", "tenant_name"]}
    )
    def post(self, json):
        logger.debug("Entering Login.get method.")
        user = json.get('username')
        password = json.get('password')
        auth_url = json.get('auth_url')
        tenant_name = json.get('tenant_name')

        openstack_logined = False
        try:
            keystone = ksclient.Client(
                auth_url=auth_url,
                username=user,
                password=password,
                tenant_name=tenant_name
            )
            g.token = keystone.auth_ref['token']['id']
            openstack_logined = True
        except Exception as e:
            logger.error("Login failed: %s.", str(e))
        if openstack_logined:
            nova_client = novaclient.client.Client(2, user, password, tenant_name, auth_url)
            servers = nova_client.servers.list()
            server_id = None
            for server in servers:
                if server.name == 'vyatta-node':
                    server_id = server.id
            if server_id:
                meterclient = ceilometerclient.client.get_client(2, os_username=user, os_password=password, os_tenant_name=tenant_name, os_auth_url=auth_url)
                now_stamp = datetime.utcnow()
                query = [
                    dict(field='timestamp', op='gt', value=(now_stamp - timedelta(seconds=5)).isoformat()),
                    dict(field='resource_id', op='eq', value='4238d0b2-142f-4219-b0ff-576ea33dabba')
                ]
                raise Exception(str(meterclient.new_samples.list(q=query, limit=10)))
            logger.info("Authorizing tenant {0}.".format(tenant_name))
            logger.info("Org-ID registered object {0}".format(
                service_limit.check_endpoint_url(auth_url, 'openstack')))
            logger.info("Org-ID registered limit{0}".format(
                service_limit.get_endpoint_tenant(auth_url, 'openstack',
                                                  tenant_name)))

            if service_limit.get_endpoint_tenant(auth_url, 'openstack',
                                                 tenant_name):
                reply = {
                    'x-openstack-authorization': g.token,
                    'x-openstack-keystore_url': auth_url
                }
                return reply
        return make_response("Unauthorized. Recheck credentials.", 401)
