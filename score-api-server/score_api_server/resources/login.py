# Copyright (c) 2015 VMware. All rights reserved
from flask import request, make_response
from score_api_server.resources import responses
from flask.ext import restful

from score_api_server.common import util
from pyvcloud.vcloudair import VCA
from flask_restful_swagger import swagger

logger = util.setup_logging(__name__)


class Login(restful.Resource):
    @swagger.operation(
        responseClass=responses.Login,
        nickname="login",
        notes="Returns information for authentification in vCloud.",
        parameters=[{'name': 'user',
                     'description': 'User login.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'host',
                     'description': 'vCloud Air authentification host.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'password',
                     'description': 'User password.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'service_type',
                     'description': 'Type of service "subscription"'
                                    ' or "ondemand".',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'service_version',
                     'description': 'API version of service one of'
                                    ' 5.6 or 5.7. Default 5.6.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'instance',
                     'description': 'Instance ID. Required for'
                                    ' ondemand service.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'service',
                     'description': 'Service name. Required'
                                    ' for subscription service.',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'org_name',
                     'description': 'Organisation name.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}],
        consumes=['application/json']
    )
    def get(self):
        logger.debug("Entering Login.get method.")
        try:
            logger.info("Seeking login parameters.")
            request_json = request.json
            user = request_json.get('user')
            host = request_json.get('host')
            password = request_json.get('password')
            service_type = request_json.get('service_type')
            service_version = request_json.get('service_version')
            instance = request_json.get('instance')
            service = request_json.get('service')
            org_name = request_json.get('org_name')
            vca = _login_user_to_service(user, host,
                                         password, service_type,
                                         service_version,
                                         instance, service, org_name)
            logger.debug("Done. Exiting Login.get method.")
            reply = {}
            if vca:
                reply["x-vcloud-authorization"] = vca.vcloud_session.token
                reply["x-vcloud-org-url"] = vca.vcloud_session.org_url
                reply["x-vcloud-version"] = vca.version
                return reply

            logger.error("Unauthorized. Aborting.")
            return make_response("Unauthorized.", 401)
        except Exception as e:
            logger.exception(e)
            http_response_code = e.message
            return make_response("Connection error: {}.".format(e),
                                 http_response_code)


def _login_user_to_service(user, host, password, service_type,
                           service_version, instance, service, org_name):
    vca = VCA(host, user, service_type, service_version)
    result = vca.login(password=password)
    if result:
        if 'ondemand' == service_type and instance:
            result = vca.login_to_instance(instance, password)
        elif 'subscription' == service_type and service:
            result = vca.login_to_org(service, org_name)
            if result:
                return vca
    return None
