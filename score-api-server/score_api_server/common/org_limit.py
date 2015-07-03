# Copyright (c) 2015 VMware. All rights reserved

from flask import g


def get_current_limit():
    """get current limit for organizations
       returns AllowedOrgs,
       if this organization disabled or not exist return None
       if deployments_limit == 0:
            you can create any amount of deployments
    """
    from score_api_server.db.models import AllowedOrgs
    org = AllowedOrgs.query.filter_by(org_id=g.org_id).first()
    if org:
        return org
