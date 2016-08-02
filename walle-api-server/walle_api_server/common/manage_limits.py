from walle_api_server.db import models
from walle_api_server.common import service_limit


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
    return True, updated_tenant.to_dict()


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

    tenant_rights = models.TenantRights.find_by(
        rights_id=id)

    if tenant_rights:
        return False, "ERROR: we have some tenant with such role"

    rights.delete()
    return True, "OK"


def rights_list():
    return True, models.Rights.list()


def tenant_rights_add(tenant_id, rights_id):

    if not tenant_id or not rights_id:
        return False, "ERROR: please set both params"

    rights = models.Rights.find_by(
        id=rights_id)

    if not rights:
        return False, "ERROR: we dont have such rights id"

    tenant = models.Tenant.find_by(
        id=tenant_id)

    if not tenant:
        return False, "ERROR: no such tenant"

    return True, models.TenantRights(tenant_id, rights_id)


def tenant_rights_list():
    return True, models.TenantRights.list()


def tenant_rights_delete(id):
    tenant_rights = models.TenantRights.find_by(
        id=id)

    if not tenant_rights:
        return False, "ERROR: No such rights/tenant entity."

    tenant_rights.delete()
    return True, "OK"
