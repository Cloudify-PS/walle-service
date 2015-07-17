# Copyright (c) 2015 VMware. All rights reserved
from flask import request, make_response
from score_api_server.resources import responses
from flask.ext import restful
from werkzeug.exceptions import BadRequest
from score_api_server.common import util
from pyvcloud.vcloudair import VCA
from flask_restful_swagger import swagger

logger = util.setup_logging(__name__)


class Login(restful.Resource):
    @swagger.operation(
        responseClass=responses.Login,
        nickname="login",
        notes="Returns information for authorization in vCloud.",
        parameters=[{'name': 'user',
                     'description': 'User login.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'host',
                     'description': 'vCloud Air authorization host.',
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
    def post(self):
        logger.debug("Entering Login.get method.")
        try:
            logger.info("Seeking for login parameters.")
            request_json = request.json
            if request_json:
                user = request_json.get('user')
                password = request_json.get('password')
                service_type = request_json.get('service_type', 'ondemand')
                host = _set_host(request_json.get('host'), service_type)
                service_version = _set_version(request_json.
                                               get('service_version'),
                                               service_type)
                instance = request_json.get('instance')
                org_name = request_json.get('org_name')
                service = request_json.get('service')
                vca = _login_user_to_service(user, host,
                                             password, service_type,
                                             service_version,
                                             instance, service, org_name)
                reply = {}
                if vca:
                    reply["x_vcloud_authorization"] = vca.vcloud_session.token
                    reply["x_vcloud_org_url"] = vca.vcloud_session.org_url
                    reply["x_vcloud_version"] = vca.version
                    logger.debug("Done. Exiting Login.get method.")
                    return reply
            logger.error("Unauthorized. Aborting.")
            return make_response("Unauthorized.", 401)
        except BadRequest as e:
            logger.exception(e)
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
        if _is_ondemand(service_type):
            if not instance:
                if not vca.instances:
                    return None
                instance = vca.instances[0]['id']
            result = vca.login_to_instance(instance, password)
        elif _is_subscription(service_type):
            if not service:
                if org_name:
                    service = org_name
                else:
                    services = vca.services.get_Service()
                    if not services:
                        return None
                    service = services[0].serviceId
            if not org_name:
                org_name = vca.get_vdc_references(service)[0].name
            result = vca.login_to_org(service, org_name)
        if result:
            return vca
    return None


def _set_version(service_version, service_type):
    if not service_version:
        if _is_ondemand(service_type):
            service_version = '5.7'
        else:
            service_version = '5.6'
    return service_version


def _set_host(host, service_type):
    if host:
        return _add_prefix(host)
    if _is_ondemand(service_type):
        return "https://iam.vchs.vmware.com"
    else:
        return "https://vchs.vmware.com"


def _add_prefix(host):
    if not (host.startswith('https://') or host.startswith('http://')):
        host = 'https://' + host
    return host


def _is_ondemand(service_type):
    return _compare(service_type, 'ondemand')


def _is_subscription(service_type):
    return _compare(service_type, 'subscription')


_compare = lambda service_type, string: service_type.lower().strip() == string
