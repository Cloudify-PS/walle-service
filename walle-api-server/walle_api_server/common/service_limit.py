# Copyright (c) 2016 VMware. All rights reserved
# Copyright (c) 2016 GigaSpaces Technologies 2016, All Rights Reserved.

DEPLOYMENT_LIMIT = 'deployments'


def check_endpoint_url(endpoint_url, type):
    """Checks endpoint for existence."""
    from walle_api_server.db.models import Endpoint
    endpoint = Endpoint.find_by(endpoint=endpoint_url, type=type)
    if endpoint:
        return endpoint


def get_endpoint_tenant(endpoint_url, type, tenant):
    """Gets Cloudify credentials and current tenant."""
    from walle_api_server.db.models import Tenant
    endpoint = check_endpoint_url(endpoint_url, type)
    if endpoint:
        return Tenant.find_by(
            endpoint_id=endpoint.id)


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
