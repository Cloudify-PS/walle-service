# Copyright (c) 2015 VMware. All rights reserved

from flask import Flask
from flask.ext import restful
from flask import request, g, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.cors import CORS

# vcloud air
from pyvcloud.vcloudsession import VCS
# openstack
import keystoneclient.v2_0.client as ksclient

from cloudify_rest_client.client import CloudifyClient

from walle_api_server.common import cfg
from walle_api_server.common import util
from walle_api_server.common import client
from walle_api_server.common import service_limit
from walle_api_server.resources import resources
from urlparse import urlparse


app = Flask(__name__)
CORS(app)
api = restful.Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CONF = cfg.CONF
app.config['SQLALCHEMY_DATABASE_URI'] = CONF.server.db_uri
util.setup_logging_for_app(app)
logger = util.setup_logging(__name__)
app.url_map.strict_slashes = False
ALLOWED_URLS = ['vchs.vmware.com']

# note: assume vcs.organization.id is unique across the service


@app.before_request
def check_authorization():
    logger.debug("Request headers %s", str(request.headers))
    if _can_skip_auth(request.path):
        return

    # doesn't have any rights
    g.rights = []

    walle_token = request.headers.get('x-walle-authorization')
    vcloud_token = request.headers.get('x-vcloud-authorization')
    vcloud_org_url = request.headers.get('x-vcloud-org-url', '')
    vcloud_version = request.headers.get('x-vcloud-version')

    if walle_token:
        return check_authorization_walle(walle_token)

    if (vcloud_org_url and vcloud_token and vcloud_version):
        return check_authorization_vcloud(
            vcloud_org_url, vcloud_token, vcloud_version
        )

    openstack_authorization = request.headers.get(
        'x-openstack-authorization'
    )
    openstack_keystore = request.headers.get("x-openstack-keystore-url")
    openstack_region = request.headers.get("x-openstack-keystore-region", "")
    tenant_name = request.headers.get("x-openstack-keystore-tenant", "")

    if (openstack_keystore and openstack_authorization):
        return check_authorization_openstack(
            openstack_authorization, openstack_keystore,
            openstack_region, tenant_name
        )
    logger.error("Unauthorized. Aborting.")
    return make_response("Unauthorized.", 401)


def check_authorization_walle(token):

    if not service_limit.valid_walle_admin_token(token):
        return make_response("Unauthorized.", 401)

    g.rights = [
        service_limit.TENANT_EDIT_RIGHT,
        service_limit.PLUGIN_EDIT_RIGHT
    ]


def check_authorization_openstack(
    openstack_authorization, openstack_keystore, openstack_region, tenant_name
):
    openstack_logined = False
    try:
        keystone = ksclient.Client(
            auth_url=openstack_keystore, token=openstack_authorization,
            project_name=tenant_name
        )
        g.token = keystone.auth_ref['token']['id']
        g.tenant_id = keystone.user_id
        g.openstack_region = openstack_region
        g.tenant_name = tenant_name
        openstack_logined = True
    except Exception as e:
        logger.error("Login failed: %s.", str(e))

    if not openstack_logined:
        return make_response("Unauthorized.", 401)

    g.keystore_url = openstack_keystore
    if not service_limit.check_endpoint_url(g.keystore_url, 'openstack'):
        logger.error("Unauthorized. Aborting authorization "
                     "for Keystore Url: %s.", g.keystore_url)
        return make_response("Unauthorized.", 401)

    logger.info("Tenant id: %s.", str(g.tenant_id))

    g.current_tenant = service_limit.get_endpoint_tenant(
        g.keystore_url, 'openstack', tenant_name
    )
    if g.current_tenant:
        g.rights = service_limit.tenant_rights(g.current_tenant.id)
        logger.info("Have such rights: %s", str(g.rights))

        logger.info("Org-ID limits entity: %s",
                    g.current_tenant.to_dict())
        logger.info("Limits for Keystore Url:%s were found.", g.keystore_url)
        g.cc = CloudifyClient(host=g.current_tenant.cloudify_host,
                              port=g.current_tenant.cloudify_port)
        g.proxy = client.HTTPClient(g.current_tenant.cloudify_host)
    else:
        logger.error(
            "No limits were defined for Keystore Url: %s/%s",
            g.keystore_url, tenant_name
        )
        return make_response("Limits for Org-ID: %s were not defined. "
                             "Please contact administrator."
                             % g.tenant_id, 403)


def check_authorization_vcloud(vcloud_org_url, vcloud_token, vcloud_version):
    if not _is_valid_url(vcloud_org_url):
        logger.error("Unauthorized. Invalid 'vcloud_org_url'. Aborting.")
        return make_response("Unauthorized:"
                             " 'vcloud_org_url' value not allowed", 401)
    vcs = VCS(vcloud_org_url, None, None, None,
              vcloud_org_url, vcloud_org_url,
              version=vcloud_version)
    result = vcs.login(token=vcloud_token)
    if result:
        logger.info("Organization authorized successfully.")
        g.tenant_id = vcs.organization.id[vcs.organization.id.rfind(':') + 1:]
        g.token = vcloud_token
        g.org_url = vcloud_org_url
        logger.info("Org-ID: %s.", g.tenant_id)
        if not service_limit.check_endpoint_url(
                vcloud_org_url, 'vcloud'
        ):
            logger.error("Unauthorized. Aborting authorization "
                         "for Org-ID: %s.", g.tenant_id)
            return make_response("Unauthorized.", 401)

        g.current_tenant = service_limit.get_endpoint_tenant(
            vcloud_org_url, g.tenant_id
        )
        if g.current_tenant:
            logger.info("Org-ID limits entity: %s",
                        g.current_tenant.to_dict())
            logger.info("Limits for Org-ID:%s were found.", g.tenant_id)
            g.cc = CloudifyClient(host=g.current_tenant.cloudify_host,
                                  port=g.current_tenant.cloudify_port)
        else:
            logger.error("No limits were defined for Org-ID: %s", g.tenant_id)
            return make_response("Limits for Org-ID: %s were not defined. "
                                 "Please contact administrator."
                                 % g.tenant_id, 403)
    else:
        logger.error(str(vcs.response.status_code))
        return make_response(str(vcs.response.reason),
                             vcs.response.status_code)


def _can_skip_auth(path):
    name = path.split('/')[1].lower()
    if name == 'api':
        logger.info("Skipping authorizations with request headers,"
                    " show api specification.")
        return True
    elif name == 'login_vcloud':
        logger.info("Skipping authorizations with request headers,"
                    " using user:password VCloud authorization.")
        return True
    elif name == 'login_openstack':
        logger.info("Skipping authorizations with request headers,"
                    " using user:password OpenStack authorization.")
        return True
    elif name == 'login_walle':
        logger.info("Skipping authorizations with request headers,"
                    " using user:password Walle authorization.")
        return True
    return False


def _is_valid_url(vcloud_org_url):
    org_url = urlparse(vcloud_org_url)
    hostname = org_url.hostname
    for url in ALLOWED_URLS:
        if hostname and hostname.endswith(url):
            return True
    return False

resources.setup_resources(api)


def main():
    host, port, workers = (CONF.server.host,
                           CONF.server.port,
                           CONF.server.workers)
    app.logger_name = "walle_api_server"
    app._logger_name = "walle_api_server"
    app._logger = util.setup_logging(__name__)
    try:
        app.run(
            host=host,
            port=port,
            processes=workers,
            debug=(True if CONF.logging.level ==
                   "DEBUG" else False)
        )
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
