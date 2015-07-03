# Copyright (c) 2015 VMware. All rights reserved

from score_api_server.db import base


class AllowedOrgs(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'allowed_org_ids'

    id = base.db.Column(base.db.String(), primary_key=True)
    org_id = base.db.Column(base.db.String(), unique=True)
    info = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())

    def __init__(self, org_id, info=None):
        self.org_id = org_id
        self.info = info if info else ""
        super(AllowedOrgs, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {}'.format(
            self.id, self.org_id
        )

    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id,
            "info": self.info,
            "created_at": self.created_at,
        }


class OrgIDToCloudifyAssociationWithLimits(base.BaseDatabaseModel,
                                           base.db.Model):
    __tablename__ = 'org_id_to_cloudify_with_limits'

    id = base.db.Column(base.db.String(), primary_key=True)
    org_id = base.db.Column(base.db.String(), unique=True)
    deployment_limits = base.db.Column(base.db.Integer())
    number_of_deployments = base.db.Column(base.db.Integer())
    cloudify_host = base.db.Column(base.db.String())
    cloudify_port = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())
    updated_at = base.db.Column(base.db.String())

    def __init__(self, org_id, cloudify_host,
                 cloudify_port, deployment_limits=0):
        self.org_id = org_id
        self.cloudify_host = cloudify_host
        self.cloudify_port = cloudify_port
        self.deployment_limits = deployment_limits
        self.number_of_deployments = 0
        super(OrgIDToCloudifyAssociationWithLimits, self).__init__()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id,
            "deployment_limits": self.deployment_limits,
            "number_of_deployments": self.number_of_deployments,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "cloudify_host": self.cloudify_host,
            "cloudify_port": self.cloudify_port
        }
