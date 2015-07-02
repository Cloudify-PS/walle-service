# Copyright (c) 2015 VMware. All rights reserved

import uuid
from score_api_server.cli import app

db = app.db


class AllowedOrgs(db.Model):
    __tablename__ = 'allowed_org_ids'

    id = db.Column(db.String(), primary_key=True)
    org_id = db.Column(db.String(), unique=True)

    def __init__(self, org_id):
        self.id = str(uuid.uuid4())
        self.org_id = org_id

    def __repr__(self):
        return '#{}: Allowed {}'.format(
            self.id, self.org_id
        )

    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id
        }

    @classmethod
    def find(cls, org_id):
        org = cls.query.filter_by(org_id=org_id).first()
        return org if org else None

    def save(self):
        app.db.session.add(self)
        app.db.session.commit()

    def delete(self):
        app.db.session.delete(self)
        app.db.session.commit()

    @classmethod
    def list(cls):
        return cls.query.all()
