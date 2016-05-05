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
KeyStoreCommands = Manager(usage="Performs action related to Keystore URLs")
OrgIDLimitsCommands = Manager(usage="Performs action related to Org-ID limits")
KeyStoreLimitsCommands = Manager(usage="Performs action related to "
                                       "KeyStore Url limits")
ApprovedPluginsCommands = Manager(usage="Performs actions related to approved "
                                        "deployment and workflow plugins.")


# OrgIds
@OrgIDCommands.option("--org-id", dest="org_id",
                      help="Adds Org-IDs to Score DB")
@OrgIDCommands.option("--info", dest="info",
                      help="Adds Org-IDs to Score DB")
@OrgIDCommands.option("--db-uri", dest="db_uri", default=None)
def add(org_id, db_uri=None, info=None):
    """Adds Org-ID."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not org_id:
        print("ERROR: Org-ID is required")
    else:
        org = models.AllowedOrgs(org_id, info=info)
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
        org = models.AllowedOrgs.find_by(org_id=org_id)
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
    print_utils.print_list(org_ids, ["id", "org_id",
                                     "info", "created_at"])


# OrgIDLimits
@OrgIDLimitsCommands.option("--org-id", dest="org_id")
@OrgIDLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@OrgIDLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@OrgIDLimitsCommands.option("--deployment-limits",
                            dest="deployment_limits", default=0)
@OrgIDLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def create(org_id, cloudify_host, cloudify_port,
           deployment_limits, db_uri=None):
    """Creates deployment limits pinned to specific
       Org-ID and specific Cloudify Manager
    """
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    if not cloudify_host or not cloudify_port:
        print("ERROR: Cloudify host and port are required.")
        return
    else:
        if not models.AllowedOrgs.find_by(org_id=org_id):
            print("ERROR: No such Org-ID.")
            return
        limit = models.OrgIDToCloudifyAssociationWithLimits(
            org_id,
            cloudify_host,
            cloudify_port,
            deployment_limits,
        )
        print_utils.print_dict(limit.to_dict())


@OrgIDLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists all Org-ID limits."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limits = models.OrgIDToCloudifyAssociationWithLimits.list()
    print_utils.print_list(limits, ["id", "org_id", "cloudify_host",
                                    "cloudify_port", "deployment_limits",
                                    "number_of_deployments",
                                    "created_at", "updated_at"])


@OrgIDLimitsCommands.option("--id", dest="id")
@OrgIDLimitsCommands.option("--org-id", dest="org_id")
@OrgIDLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@OrgIDLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@OrgIDLimitsCommands.option("--deployment-limits", dest="deployment_limits")
@OrgIDLimitsCommands.option("--number-of-deployments",
                            dest="number_of_deployments")
@OrgIDLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def update(**kwargs):
    """Updates Org-ID limits with given keys by its ID."""
    db_uri = kwargs.get("db_uri")
    update_kwargs = {}
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    limit_id = kwargs["id"]

    keys = ["org_id", "cloudify_host", "cloudify_port",
            "deployment_limits", "number_of_deployments"]

    for key in keys:
        if kwargs.get(key):
            update_kwargs.update({key: kwargs.get(key)})

    if (not models.AllowedOrgs.find_by(org_id=kwargs.get("org_id"))
            and not limit_id):
        print("ERROR: ID or existing Org-ID required.")
        return

    limit = models.OrgIDToCloudifyAssociationWithLimits.find_by(
        id=limit_id)
    if not limit:
        print("No such Org-ID limit entity.")
    else:
        limit.update(**update_kwargs)
        updated_limit = (
            models.OrgIDToCloudifyAssociationWithLimits.find_by(
                id=limit_id))
        print_utils.print_dict(updated_limit.to_dict())


@OrgIDLimitsCommands.option("--id", dest="id")
@OrgIDLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def delete(**kwargs):
    """Deletes Org-ID limit by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limit = models.OrgIDToCloudifyAssociationWithLimits.find_by(
        id=kwargs.get("id"))
    if not limit:
        print("ERROR: No such Org-ID limit entity.")
        return
    else:
        limit.delete()
        print("OK")


# ApprovedPlugins
@ApprovedPluginsCommands.option(
    "--name", dest="name", help="Approved plugin name.")
@ApprovedPluginsCommands.option("--source", dest="source",
                                help="Approved plugin source")
@ApprovedPluginsCommands.option("--type", dest="type",
                                help="Approved plugin type. "
                                "`deployment_plugin` or `workflow_plugins`")
@ApprovedPluginsCommands.option(
    "--from-file", dest="from_file",
    help="Full path to approved plugins description, "
         "expected to be a YAML file")
@ApprovedPluginsCommands.option("--db-uri", dest="db_uri", default=None)
def add(**kwargs):

    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    _name, _source, _type = (kwargs.get("name"),
                             kwargs.get("source"),
                             kwargs.get("type"))
    if not any([_name, _type]):
        _plugins = (models.ApprovedPlugins.
                    register_from_file(kwargs.get("from_file")))
        print_utils.print_list(_plugins, ['name', 'source', 'plugin_type'])
    else:
        print_utils.print_dict(
            models.ApprovedPlugins(_name, _source, _type).to_dict())


@ApprovedPluginsCommands.option("--db-uri", dest="db_uri", default=None)
def list(**kwargs):
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    plugins = models.ApprovedPlugins.list()
    print_utils.print_list(
        plugins, ['name', 'source', 'plugin_type'])


@ApprovedPluginsCommands.option("--db-uri", dest="db_uri", default=None)
@ApprovedPluginsCommands.option("--name", dest="name",
                                help="Approved plugin name")
def delete(**kwargs):
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    name = kwargs.get("name")
    models.ApprovedPlugins.find_by(name=name).delete()


# KeyStore Urls
@KeyStoreCommands.option("--keystore-url", dest="keystore_url",
                         help="Adds keystore-urls to Score DB")
@KeyStoreCommands.option("--info", dest="info",
                         help="Adds keystore-urls to Score DB")
@KeyStoreCommands.option("--db-uri", dest="db_uri", default=None)
def add(keystore_url, db_uri=None, info=None):
    """Adds keystore-url."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not keystore_url:
        print("ERROR: keystore-url is required")
    else:
        org = models.AllowedKeyStoreUrl(keystore_url, info=info)
        print_utils.print_dict(org.to_dict())


@KeyStoreCommands.option("--keystore-url", dest="keystore_url",
                         help="Deletes keystore-url from Score DB")
@KeyStoreCommands.option("--db-uri", dest="db_uri", default=None)
def delete(keystore_url, db_uri=None):
    """Deletes keystore-url."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not keystore_url:
        print("ERROR: keystore-url is required")
    else:
        org = models.AllowedKeyStoreUrl.find_by(keystore_url=keystore_url)
        if org:
            org.delete()
            print("OK")
        else:
            print("ERROR: keystore-url not found")


@KeyStoreCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists keystore-urls."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    keystore_urls = models.AllowedKeyStoreUrl.list()
    print_utils.print_list(
        keystore_urls, ["id", "keystore_url", "info", "created_at"]
    )


# KeyStoreLimits
@KeyStoreLimitsCommands.option("--keystore-url", dest="keystore_url")
@KeyStoreLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@KeyStoreLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@KeyStoreLimitsCommands.option("--deployment-limits",
                               dest="deployment_limits", default=0)
@KeyStoreLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def create(keystore_url, cloudify_host, cloudify_port,
           deployment_limits, db_uri=None):
    """Creates deployment limits pinned to specific
       keystore-url and specific Cloudify Manager
    """
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    if not cloudify_host or not cloudify_port:
        print("ERROR: Cloudify host and port are required.")
        return
    else:
        if not models.AllowedKeyStoreUrl.find_by(keystore_url=keystore_url):
            print("ERROR: No such keystore-url.")
            return
        limit = models.KeyStoreUrlToCloudifyAssociationWithLimits(
            keystore_url,
            cloudify_host,
            cloudify_port,
            deployment_limits,
        )
        print_utils.print_dict(limit.to_dict())


@KeyStoreLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists all keystore-url limits."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limits = models.KeyStoreUrlToCloudifyAssociationWithLimits.list()
    print_utils.print_list(limits, ["id", "keystore_url", "cloudify_host",
                                    "cloudify_port", "deployment_limits",
                                    "number_of_deployments",
                                    "created_at", "updated_at"])


@KeyStoreLimitsCommands.option("--id", dest="id")
@KeyStoreLimitsCommands.option("--keystore-url", dest="keystore_url")
@KeyStoreLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@KeyStoreLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@KeyStoreLimitsCommands.option("--deployment-limits",
                               dest="deployment_limits")
@KeyStoreLimitsCommands.option("--number-of-deployments",
                               dest="number_of_deployments")
@KeyStoreLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def update(**kwargs):
    """Updates keystore-url limits with given keys by its ID."""
    db_uri = kwargs.get("db_uri")
    update_kwargs = {}
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    limit_id = kwargs["id"]

    keys = ["keystore_url", "cloudify_host", "cloudify_port",
            "deployment_limits", "number_of_deployments"]

    for key in keys:
        if kwargs.get(key):
            update_kwargs.update({key: kwargs.get(key)})

    if (not models.AllowedKeyStoreUrl.find_by(
            keystore_url=kwargs.get("keystore_url"))
            and not limit_id):
        print("ERROR: ID or existing keystore-url required.")
        return

    limit = models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
        id=limit_id)
    if not limit:
        print("No such keystore-url limit entity.")
    else:
        limit.update(**update_kwargs)
        updated_limit = (
            models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
                id=limit_id))
        print_utils.print_dict(updated_limit.to_dict())


@KeyStoreLimitsCommands.option("--id", dest="id")
@KeyStoreLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def delete(**kwargs):
    """Deletes keystore-url limit by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limit = models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
        id=kwargs.get("id"))
    if not limit:
        print("ERROR: No such keystore-url limit entity.")
        return
    else:
        limit.delete()
        print("OK")


manager.add_command('approved-plugins', ApprovedPluginsCommands)
manager.add_command('org-ids', OrgIDCommands)
manager.add_command('keystore-urls', KeyStoreCommands)
manager.add_command('org-id-limits', OrgIDLimitsCommands)
manager.add_command('keystore-url-limits', KeyStoreLimitsCommands)
manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
