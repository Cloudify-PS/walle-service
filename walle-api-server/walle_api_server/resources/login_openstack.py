# Copyright (c) 2016 VMware. All rights reserved
from flask import make_response, g
from walle_api_server.resources import responses
from flask.ext import restful
from walle_api_server.common import util
import keystoneclient.v2_0.client as ksclient
from flask_restful_swagger import swagger
from walle_api_server.common import service_limit

logger = util.setup_logging(__name__)


class LoginOpenStack(restful.Resource):
    @swagger.operation(
        responseClass=responses.LoginOpenStack,
        nickname="login_vcloud",
        notes="Returns information for authorization in vCloud.",
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
             "user": {"type": "string", "minLength": 1},
             "password": {"type": "string", "minLength": 1},
             "auth_url": {"type": "string"},
             "tenant_name": {"type": "string"},
         },
         "required": ["user", "password", "auth_url", "tenant_name"]}
    )
    def post(self, json):
        logger.debug("Entering Login.get method.")
        user = json.get('user')
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
            if service_limit.get_service_url_limits(auth_url, tenant_name):
                reply = {
                    'x-openstack-authorization': g.token,
                    'x-openstack-keystore_url': auth_url
                }
                return reply
        return make_response("Unauthorized. Recheck credentials.", 401)
