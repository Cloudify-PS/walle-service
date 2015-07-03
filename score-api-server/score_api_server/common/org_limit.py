# Copyright (c) 2015 VMware. All rights reserved

from flask import g


def check_org_id():
    """Checks Org-ID for existence."""
    from score_api_server.db.models import AllowedOrgs
    org = AllowedOrgs.find_by(org_id=g.org_id)
    if org:
        return org


def get_cloudify_credentials_and_org_id_limit():
    """Gets Cloudify credentials and current Org-ID limits."""
    from score_api_server.db.models import (
        OrgIDToCloudifyAssociationWithLimits)
    limit = OrgIDToCloudifyAssociationWithLimits.find_by(
        org_id=g.org_id)
    if limit:
        return limit, limit.cloudify_host, limit.cloudify_port
