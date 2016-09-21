# Copyright (c) 2016 VMware. All rights reserved
from flask.ext import restful
from flask_restful_swagger import swagger
from walle_api_server.common import util
from flask import make_response
from walle_api_server.login import login_openstack
from walle_api_server.login import login_vcloud


logger = util.setup_logging(__name__)


class Login(restful.Resource):
    @swagger.operation(
        nickname="login",
        notes="Returns information for authorization",
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
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'auth_url',
                     'description': 'OpenStack keystore url',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'service_type',
                     'description': 'Type of service "subscription"'
                                    ' or "ondemand". Default: "ondemand"',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'host',
                     'description': 'vCloud Air authorization host.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'service_version',
                     'description': 'API version of service one of'
                                    ' 5.6 or 5.7. Default 5.6.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'instance',
                     'description': 'Instance ID. Required for'
                                    ' ondemand service.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'service',
                     'description': 'Service name. Required'
                                    ' for subscription service.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'org_name',
                     'description': 'Organisation name.',
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
             "host": {"type": "string"},
             "service_type": {"type": "string"},
             "service_version": {"type": "string"},
             "instance": {"type": "string"},
             "service": {"type": "string"},
             "org_name": {"type": "string"},
         },
         "required": ["username", "password"]}
    )
    def post(self, json):
        logger.debug("Entering Login.get method.")

        username = json.get('username')
        password = json.get('password')
        auth_url = json.get('auth_url')
        tenant_name = json.get('tenant_name')
        instance = json.get('instance')
        org_name = json.get('org_name')

        if not (username and password):
            return make_response("Unauthorized. Recheck username and password.",
                                 401)
        elif auth_url and tenant_name:
            return login_openstack.login(json)
        elif instance and org_name:
            return login_vcloud.login(json)
        else:
            return make_response("Unauthorized. Recheck parameters.",
                                 401)
