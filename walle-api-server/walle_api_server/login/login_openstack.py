# Copyright (c) 2016 VMware. All rights reserved
from flask import make_response, g
from walle_api_server.common import util
import keystoneclient.v2_0.client as ksclient
from walle_api_server.common import service_limit

logger = util.setup_logging(__name__)


def login(json):
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
