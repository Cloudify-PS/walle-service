# Copyright (c) 2015 VMware. All rights reserved

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from score_api_server.cli import app
from score_api_server.db import models
from score_api_server.common import print_utils


db = app.db
flask_app = app.app

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)


OrgIDCommands = Manager(usage="Performs action related to Org-IDs")


@OrgIDCommands.option("--org-id", dest="org_id",
                      help="Adds Org-IDs to Score DB")
@OrgIDCommands.option("--db-uri", dest="db_uri", default=None)
def add(org_id, db_uri=None):
    """Adds Org-ID."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not org_id:
        print("ERROR: Org-ID is required")
    else:
        org = models.AllowedOrgs(org_id)
        org.save()
        print_utils.print_dict(org.to_dict())


@OrgIDCommands.option("--org-id", dest="org_id",
                      help="Deletes Org-ID from Score DB")
@OrgIDCommands.option("--db-uri", dest="db_uri", default=None)
def delete(org_id, db_uri=None):
    """Deletes Org-ID."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not org_id:
        print("ERROR: Org-ID is required")
    else:
        org = models.AllowedOrgs.find(org_id)
        if org:
            org.delete()
            print("OK")
        else:
            print("ERROR: Org-ID not found")


@OrgIDCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists Org-IDs."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    org_ids = models.AllowedOrgs.list()
    print_utils.print_list(org_ids, ["id", "org_id"])


manager.add_command('org-ids', OrgIDCommands)
manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
