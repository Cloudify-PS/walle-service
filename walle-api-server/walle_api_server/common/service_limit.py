# Copyright (c) 2016 VMware. All rights reserved
# Copyright (c) 2016 GigaSpaces Technologies 2016, All Rights Reserved.


def check_service_url(service_url, tenant):
    """Checks Keystore url for existence."""
    from walle_api_server.db.models import AllowedServiceUrl
    service_url = AllowedServiceUrl.find_by(service_url=service_url,
                                            tenant=tenant)
    if service_url:
        return service_url


def get_service_url_limits(service_url, tenant):
    """Gets Cloudify credentials and current Keystore url limits."""
    from walle_api_server.db.models import (
        ServiceUrlToCloudifyAssociationWithLimits, AllowedServiceUrl)
    service = AllowedServiceUrl.find_by(service_url=service_url,
                                        tenant=tenant)
    return ServiceUrlToCloudifyAssociationWithLimits.find_by(
        serviceurl_id=service.id)
