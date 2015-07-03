# Copyright (c) 2015 VMware. All rights reserved

from flask import g, abort, make_response


def check_org_id():
    """Checks Org-ID for existence."""
    from score_api_server.db.models import AllowedOrgs
    org = AllowedOrgs.find_by(org_id=g.org_id)
    if org:
        return org


def get_org_id_limits():
    """Gets Cloudify credentials and current Org-ID limits."""
    from score_api_server.db.models import (
        OrgIDToCloudifyAssociationWithLimits)
    return OrgIDToCloudifyAssociationWithLimits.find_by(
        org_id=g.org_id)
