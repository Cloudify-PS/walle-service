# Copyright (c) 2015 VMware. All rights reserved
from flask import make_response
from walle_api_server.resources import responses
from flask.ext import restful
from walle_api_server.common import util
from pyvcloud.vcloudair import VCA
from flask_restful_swagger import swagger
from walle_api_server.common import service_limit


logger = util.setup_logging(__name__)


class LoginVcloud(restful.Resource):
    @swagger.operation(
        responseClass=responses.LoginVCloud,
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
                    {'name': 'service_type',
                     'description': 'Type of service "subscription"'
                                    ' or "ondemand". Default: "ondemand"',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'host',
                     'description': 'vCloud Air authorization host.',
                     'required': True,
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
             "user": {"type": "string", "minLength": 1},
             "password": {"type": "string", "minLength": 1},
             "host": {"type": "string"},
             "service_type": {"type": "string"},
             "service_version": {"type": "string"},
             "instance": {"type": "string"},
             "service": {"type": "string"},
             "org_name": {"type": "string"},
         },
         "required": ["user", "password"]}
    )
    def post(self, json):
        logger.debug("Entering Login.get method.")
        user = json.get('user')
        password = json.get('password')
        service_type = json.get('service_type', 'ondemand')
        host = _set_host(json.get('host'), service_type)
        service_version = _set_version(json.get('service_version'),
                                       service_type)
        instance = json.get('instance')
        org_name = json.get('org_name')
        service = json.get('service')
        vca = _login_user_to_service(user, host, password, service_type,
                                     service_version,
                                     instance, service, org_name)
        reply = {}
        if vca:
            org_id = vca.vcloud_session.org_url.split('/')[-1]
            logger.info("Authorizing Org-ID {0}.".format(org_id))
            logger.info("Org-ID registered object {0}".format(
                service_limit.check_endpoint_url(host, 'vcloud')))
            logger.info("Org-ID registered limit{0}".format(
                service_limit.get_endpoint_tenant(host, 'vcloud', org_id)))
            if (service_limit.get_endpoint_tenant(host, 'vcloud', org_id)):
                reply["x_vcloud_authorization"] = vca.vcloud_session.token
                reply["x_vcloud_org_url"] = vca.vcloud_session.org_url
                reply["x_vcloud_version"] = vca.version
                if vca.instances and not instance:
                    reply['instances'] = self._get_instances(vca.instances)
                elif vca.services and not service and not org_name:
                    reply['services'] = self._get_services_with_orgs(vca)
                logger.debug("Done. Exiting Login.get method.")
                return reply
            else:
                message = "Organization is not authorized"
        else:
            message = ("Invalid credentials or can't authorize instance or "
                       "service with its organization")
        logger.error("Unauthorized. {}. Aborting.".format(message))
        return make_response("Unauthorized. {}.".format(message), 401)

    def _get_instances(self, instances):
        reply = []
        for instance in instances:
            reply.append(dict(id=instance['id'],
                              region=instance['region']))
        return reply

    def _get_services_with_orgs(self, vca):
        reply = []
        for service in vca.services.get_Service():
            orgs = vca.get_vdc_references(service.serviceId)
            reply.append({'id': service.serviceId,
                          'orgs': [org.name for org in orgs]})
        return reply


def _login_user_to_service(user, host, password, service_type,
                           service_version, instance, service, org_name):
    try:
        vca = VCA(host, user, service_type, service_version)
        result = vca.login(password=password)
        if result:
            if _is_ondemand(service_type):
                if not instance:
                    if not vca.instances:
                        return None
                    instance = vca.instances[0]['id']
                result = vca.login_to_instance(instance, password)
                logger.info("Login using instance: {0}. "
                            "Result: {1}.".format(instance, result))
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
                logger.info(
                    "Login using service and organization: "
                    "{0}, {1}. Result: {2}.".format(
                        service, org_name, result))
            if (result and
                    hasattr(vca, 'vcloud_session') and
                    hasattr(vca.vcloud_session, 'org_url')):
                        return vca
        return None
    except Exception as e:
        logger.exception(e)
        http_response_code = e.message
        return make_response("vCloud connection error:"
                             " Can't login to vCloud service",
                             http_response_code)


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
        return "https://vca.vmware.com"
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


def _compare(service_type, string):
    return service_type.lower().strip() == string
