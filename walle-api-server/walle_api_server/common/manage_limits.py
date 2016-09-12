from walle_api_server.db import models
from walle_api_server.common import service_limit
import keystoneclient.v2_0.client as ksclient


def endpoint_add(endpoint_url, type, version, description):

    if not endpoint_url or not type:
        return False, "ERROR: endpoint/type is required"

    endpoint = service_limit.check_endpoint_url(endpoint_url, type)
    if endpoint:
        return False, "ERROR: already exist"

    return True, models.Endpoint(endpoint_url, type, version, description)


def endpoint_delete(endpoint_url, type):

    if not endpoint_url or not type:
        return False, "ERROR: endpoint-url/type is required"

    endpoint = service_limit.check_endpoint_url(endpoint_url, type)
    if endpoint:
        endpoint.delete()
        return True, "OK"
    else:
        return False, "ERROR: endpoint not found"


def endpoint_delete_id(id):

    if not id:
        return False, "ERROR: endpoint id is required"

    endpoint = models.Endpoint.find_by(id=id)

    if endpoint:
        endpoint.delete()
        return True, "OK"
    else:
        return False, "ERROR: endpoint not found"


def endpoint_list():

    return True, models.Endpoint.list()


def tenant_add(endpoint_url, type, tenant_name, cloudify_host,
               cloudify_port, description):

    if not cloudify_host or not cloudify_port:
        return False, "ERROR: Cloudify host and port are required."

    endpoint = service_limit.check_endpoint_url(endpoint_url, type)
    if not endpoint:
        return False, "ERROR: No such endpoint/type."

    tenant = service_limit.get_endpoint_tenant(endpoint_url, type, tenant_name)
    if tenant:
        return False, "ERROR: already exist"

    tenant = models.Tenant(
        endpoint.id, tenant_name, cloudify_host, cloudify_port,
        description
    )

    return True, tenant


def tenant_list():
    return True, models.Tenant.list()


def tenant_update(**kwargs):

    update_kwargs = {}

    tenant_id = kwargs["id"]

    keys = ["endpoint_id", "tenant_name", "cloudify_host", "cloudify_port",
            "description"]

    for key in keys:
        if kwargs.get(key):
            update_kwargs.update({key: kwargs.get(key)})

    if not tenant_id:
        return False, "ERROR: ID or existing  required."

    tenant = models.Tenant.find_by(
        id=tenant_id)
    if not tenant:
        return False, "No such tenant entity."

    tenant.update(**update_kwargs)
    updated_tenant = (
        models.Tenant.find_by(
            id=tenant_id))
    return True, updated_tenant


def tenant_delete(id):
    tenant = models.Tenant.find_by(
        id=id)

    if not tenant:
        return False, "ERROR: No such tenant entity."

    tenant.delete()
    return True, "OK"


def limit_add(endpoint_url, type, tenant_name, limit_type, soft, hard):

    endpoint = service_limit.check_endpoint_url(endpoint_url, type)
    if not endpoint:
        return False, "ERROR: No such endpoint/type."

    tenant = service_limit.get_endpoint_tenant(
        endpoint_url, type, tenant_name
    )
    if not tenant:
        return False, "ERROR: No such tenant."

    tenant_limit = service_limit.get_endpoint_tenant_limit(
        endpoint_url, type, tenant_name, limit_type
    )
    if tenant_limit:
        return False, "ERROR: already exist"

    if not limit_type:
        return False, "ERROR: please set limit type"

    limit = models.Limit(
        tenant.id, soft, hard, limit_type
    )

    return True, limit


def limit_list():
    return True, models.Limit.list()


def limit_update(**kwargs):

    update_kwargs = {}

    limit_id = kwargs["id"]

    keys = ["tenant_id", "type", "soft", "hard"]

    for key in keys:
        if kwargs.get(key):
            update_kwargs.update({key: kwargs.get(key)})

    if not limit_id:
        return False, "ERROR: ID required."

    limit = models.Limit.find_by(
        id=limit_id)
    if not limit:
        return False, "No such limit entity."

    limit_check = models.Limit.find_by(
        tenant_id=limit.tenant_id, type=kwargs.get('type'))
    if limit_check and limit_check.id != limit_id:
        return False, "We already have such limit type/tenant"

    limit = models.Limit.find_by(
        id=limit_id)
    if not limit:
        return False, "No such limit entity."

    limit.update(**update_kwargs)
    updated_limit = (
        models.Limit.find_by(
            id=limit_id))
    return True, updated_limit


def limit_delete(id):
    limit = models.Limit.find_by(id=id)

    if not limit:
        return False, "ERROR: No such tenant entity."

    limit.delete()
    return True, "OK"


def rights_add(name, description=None):
    if not name:
        return False, "ERROR: endpoint/type is required"

    endpoint = service_limit.get_right(name)
    if endpoint:
        return False, "ERROR: already exist"

    return True, models.Rights(name, description)


def rights_delete(id):
    rights = models.Rights.find_by(
        id=id)

    if not rights:
        return False, "ERROR: No such rights entity."

    user_rights = models.UserRights.find_by(
        rights_id=id)

    if user_rights:
        return False, "ERROR: we have some tenant with such role"

    rights.delete()
    return True, "OK"


def rights_list():
    return True, models.Rights.list()


def user_rights_add(username, password, tenant_name, endpoint_url,
                    endpoint_type, right):
    rights = None

    if right:
        rights = models.Rights.find_by(name=right)

    if not rights:
        return False, "ERROR: we dont have such rights"

    if endpoint_url and endpoint_type and tenant_name:
        tenant = service_limit.get_endpoint_tenant(
            endpoint_url, endpoint_type, tenant_name
        )

    if not tenant:
        return False, "ERROR: no such tenant '{}'"\
                      " for endpoint '{}'".format(tenant, endpoint_url)
    try:
        keystone = ksclient.Client(
            auth_url=endpoint_url,
            username=username,
            password=password,
            tenant_name=tenant_name
        )
    except Exception as e:
        return False, "Login failed: %s.".format(str(e))
    user_id = keystone.user_id
    userrights = models.UserRights.find_by(user_id=user_id,
                                           rights_id=rights.id)
    if userrights:
        return True, userrights
    return True, models.UserRights(user_id, rights.id)


def user_rights_list():
    return True, models.UserRights.list()


def user_rights_delete(id):
    user_rights = models.UserRights.find_by(
        id=id)

    if not user_rights:
        return False, "ERROR: No such rights/tenant entity."

    user_rights.delete()
    return True, "OK"
