# Copyright (c) 2015 VMware. All rights reserved
from flask import request, make_response
from flask.ext import restful

from cloudify_rest_client import exceptions
from score_api_server.common import util
from pyvcloud.vcloudair import VCA

logger = util.setup_logging(__name__)


class Login(restful.Resource):
    def get(self):
        logger.debug("Entering Login.get method.")
        try:
            logger.info("Seeking login parameters")
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

        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return make_response(str(e), e.status_code)
        except Exception as e:
            logger.error(str(e))
            return make_response("Connection error", e.message)


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
