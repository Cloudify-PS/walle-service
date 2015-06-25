from flask import g
import warnings


def get_current_usage():
    """return list of deployments"""
    from score_api_server.resources.models import UsedOrgs
    org_usage = UsedOrgs.query.filter_by(org_id=g.org_id).first()
    if org_usage:
        return org_usage
    return UsedOrgs(g.org_id, 0)


def get_current_limit():
    """get current limit for organizations
       returns AllowedOrgs,
       if this organization disabled or not exist return None
       if deployments_limit == 0:
            you can create any amount of deployments
    """
    from score_api_server.resources.models import AllowedOrgs
    org = AllowedOrgs.query.filter_by(org_id=g.org_id).first()
    if org and org.deployments_limit >= 0:
        return org
    return None


def decrement():
    """decrement count of deployments for curent organization"""
    from app import db
    org_usage = get_current_usage()
    if org_usage.deployments_count <= 0:
        warnings.warn("something going wrong, we have negative installation")
        return
    org_usage.deployments_count = org_usage.deployments_count - 1
    db.session.add(org_usage)
    db.session.commit()


def increment():
    """increment count of deployments for curent organization"""
    from app import db
    org_limit = get_current_limit()
    if not org_limit:
        return False
    org_usage = get_current_usage()
    if org_limit.deployments_limit:
        if org_limit.deployments_limit >= org_usage.deployments_count:
            return False
    org_usage.deployments_count = org_usage.deployments_count + 1
    db.session.add(org_usage)
    db.session.commit()
    return True
