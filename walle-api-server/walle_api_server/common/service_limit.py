# Copyright (c) 2016 VMware. All rights reserved
# Copyright (c) 2016 GigaSpaces Technologies 2016, All Rights Reserved.
import time

DEPLOYMENT_LIMIT = 'deployments'
# User can edit tenant list on server
TENANT_EDIT_RIGHT = 'tenants'
# User can change list of approved plugins
PLUGIN_EDIT_RIGHT = 'plugins'
# Have rights to see blueprint/deployments/executions,
# users in  WalleAdministrators doesn't have such right
USER_RIGHT = 'user'
# Common right for walle administrators
ADMIN_RIGHT = 'admin'


def check_endpoint_url(endpoint_url, type):
    """Checks endpoint for existence."""
    from walle_api_server.db.models import Endpoint
    endpoint = Endpoint.find_by(endpoint=endpoint_url, type=type)
    if endpoint:
        return endpoint


def get_endpoint_tenant(endpoint_url, endpoint_type, tenant):
    """Gets Cloudify credentials and current tenant."""
    from walle_api_server.db.models import Tenant
    endpoint = check_endpoint_url(endpoint_url, endpoint_type)
    if endpoint:
        return Tenant.find_by(
            endpoint_id=endpoint.id, tenant_name=tenant)


def get_endpoint_tenant_limit(endpoint_url, type, tenant_name,
                              limit_type):
    """Gets tenants limit"""
    from walle_api_server.db.models import Limit
    tenant = get_endpoint_tenant(endpoint_url, type, tenant_name)
    if tenant:
        return Limit.find_by(
            tenant_id=tenant.id, type=limit_type)


def get_tenant_limit(tenant_id, limit_type):
    """Gets tenants limit"""
    from walle_api_server.db.models import Limit
    return Limit.find_by(tenant_id=tenant_id, type=limit_type)


def get_right(rights_name):
    from walle_api_server.db.models import Rights

    return Rights.find_by(name=rights_name)


def user_rights(user_id):
    from walle_api_server.db.models import UserRights

    list = []

    rights = UserRights.query.filter(
        UserRights.user_id == user_id).all()
    for right in rights:
        if right.right:
            list += [right.right.name]

    return list


def cant_edit_tenants():

    from flask import g, make_response

    if TENANT_EDIT_RIGHT not in g.rights:
        return make_response("Forbidden.", 403)

    return False


def cant_edit_plugins():

    from flask import g, make_response

    if PLUGIN_EDIT_RIGHT not in g.rights:
        return make_response("Forbidden.", 403)

    return False


def cant_see_blueprints():

    from flask import g, make_response

    if USER_RIGHT not in g.rights:
        return make_response("Forbidden.", 403)

    return False


def general_response_todict(status, value):
    from flask import make_response

    if status:
        return value.to_dict()
    else:
        return make_response(value, 400)
