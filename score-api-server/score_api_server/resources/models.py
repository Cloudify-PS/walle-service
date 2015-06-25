from app import db


class UsedOrgs(db.Model):
    __tablename__ = 'used_orgs'

    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.String(), unique=True)
    # current amount of deployments
    deployments_count = db.Column(db.Integer)

    def __init__(self, org_id, deployments_count):
        self.org_id = org_id
        self.deployments_count = deployments_count

    def __repr__(self):
        return '#{}: {} used  {}'.format(
            self.id, self.org_id, self.deployments_count
        )


class AllowedOrgs(db.Model):
    __tablename__ = 'allowed_orgs'

    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.String(), unique=True)
    # limit for deploymnets, if 0 - unlimited
    deployments_limit = db.Column(db.Integer)

    def __init__(self, org_id, deployments_limit):
        self.org_id = org_id
        self.deployments_limit = deployments_limit

    def __repr__(self):
        return '#{}: Allowed {} up to {}'.format(
            self.id, self.org_id, self.deployments_limit
        )
