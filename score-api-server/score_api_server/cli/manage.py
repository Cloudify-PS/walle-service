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


ServiceUrlCommands = Manager(usage="Performs action related to "
                                   "Keystore(service) URLs")
ServiceUrlLimitsCommands = Manager(usage="Performs action related to "
                                         "KeyStore(service) Url limits")
ApprovedPluginsCommands = Manager(usage="Performs actions related to approved "
                                        "deployment and workflow plugins.")
AdminsCommands = Manager(usage="Performs actions related to score "
                               "administrators")


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


# Service Urls
@ServiceUrlCommands.option("--service-url", dest="service_url",
                           help="Adds service-urls to Score DB")
@ServiceUrlCommands.option("--tenant", dest="tenant",
                           help="Adds tenant to Score DB")
@ServiceUrlCommands.option("--info", dest="info",
                           help="Adds service-urls to Score DB")
@ServiceUrlCommands.option("--db-uri", dest="db_uri", default=None)
def add(service_url, tenant, db_uri=None, info=None):
    """Adds service-url."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not service_url or not tenant:
        print("ERROR: service-url/tenant is required")
    else:
        org = models.AllowedServiceUrl(service_url, tenant, info=info)
        print_utils.print_dict(org.to_dict())


@ServiceUrlCommands.option("--service-url", dest="service_url",
                           help="Deletes service-url from Score DB")
@ServiceUrlCommands.option("--tenant", dest="tenant",
                           help="Deletes tenant to Score DB")
@ServiceUrlCommands.option("--db-uri", dest="db_uri", default=None)
def delete(service_url, tenant, db_uri=None):
    """Deletes service-url."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not service_url or not tenant:
        print("ERROR: service-url/tenant is required")
    else:
        org = models.AllowedServiceUrl.find_by(service_url=service_url,
                                               tenant=tenant)
        if org:
            org.delete()
            print("OK")
        else:
            print("ERROR: service-url not found")


@ServiceUrlCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists service-urls."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    service_urls = models.AllowedServiceUrl.list()
    print_utils.print_list(
        service_urls, ["id", "service_url", "tenant", "info", "created_at"]
    )


# ServiceUrl Limits
@ServiceUrlLimitsCommands.option("--service-url", dest="service_url")
@ServiceUrlLimitsCommands.option("--tenant", dest="tenant",
                                 help="Adds tenant to Score DB")
@ServiceUrlLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@ServiceUrlLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@ServiceUrlLimitsCommands.option("--deployment-limits",
                                 dest="deployment_limits", default=0)
@ServiceUrlLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def add(service_url, tenant, cloudify_host, cloudify_port, deployment_limits,
        db_uri=None):
    """Creates deployment limits pinned to specific
       service-url and specific Cloudify Manager
    """
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    if not cloudify_host or not cloudify_port:
        print("ERROR: Cloudify host and port are required.")
        return
    else:
        service = models.AllowedServiceUrl.find_by(service_url=service_url,
                                                   tenant=tenant)
        if not service:
            print("ERROR: No such service-url/tenant.")
            return
        limit = models.ServiceUrlToCloudifyAssociationWithLimits(
            service.id,
            cloudify_host,
            cloudify_port,
            deployment_limits,
        )
        print_utils.print_dict(limit.to_dict())


@ServiceUrlLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists all service-url limits."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limits = models.ServiceUrlToCloudifyAssociationWithLimits.list()
    print_utils.print_list(limits, ["id", "serviceurl_id", "cloudify_host",
                                    "cloudify_port", "deployment_limits",
                                    "number_of_deployments",
                                    "created_at", "updated_at"])


@ServiceUrlLimitsCommands.option("--id", dest="id")
@ServiceUrlLimitsCommands.option("--service-id", dest="serviceurl_id")
@ServiceUrlLimitsCommands.option("--cloudify-host", dest="cloudify_host")
@ServiceUrlLimitsCommands.option("--cloudify-port", dest="cloudify_port")
@ServiceUrlLimitsCommands.option("--deployment-limits",
                                 dest="deployment_limits")
@ServiceUrlLimitsCommands.option("--number-of-deployments",
                                 dest="number_of_deployments")
@ServiceUrlLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def update(**kwargs):
    """Updates service-url limits with given keys by its ID."""
    db_uri = kwargs.get("db_uri")
    update_kwargs = {}
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    limit_id = kwargs["id"]

    keys = ["serviceurl_id", "cloudify_host", "cloudify_port",
            "deployment_limits", "number_of_deployments"]

    for key in keys:
        if kwargs.get(key):
            update_kwargs.update({key: kwargs.get(key)})

    if (not models.AllowedServiceUrl.find_by(
            serviceurl_id=kwargs.get("serviceurl_id"))
            and not limit_id):
        print("ERROR: ID or existing service-url required.")
        return

    limit = models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
        id=limit_id)
    if not limit:
        print("No such service-url limit entity.")
    else:
        limit.update(**update_kwargs)
        updated_limit = (
            models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
                id=limit_id))
        print_utils.print_dict(updated_limit.to_dict())


@ServiceUrlLimitsCommands.option("--id", dest="id")
@ServiceUrlLimitsCommands.option("--db-uri", dest="db_uri", default=None)
def delete(**kwargs):
    """Deletes service-url limit by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    limit = models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
        id=kwargs.get("id"))
    if not limit:
        print("ERROR: No such service-url limit entity.")
        return
    else:
        limit.delete()
        print("OK")


# Administrators
@AdminsCommands.option("--user", dest="user",
                       help="Adds score admins to Score DB")
@AdminsCommands.option("--password", dest="password",
                       help="Adds score admins to Score DB")
@AdminsCommands.option("--db-uri", dest="db_uri", default=None)
def add(user, password, db_uri=None):
    """Adds score administrator."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not user or not password:
        print("ERROR: user and password are required")
    else:
        admin = models.ScoreAdministrators(user, password)
        print_utils.print_dict(admin.to_dict())


@AdminsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists administrators"""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    admins = models.ScoreAdministrators.list()
    print_utils.print_list(
        admins, ["id", "name", "password", "token", "expire"]
    )


@AdminsCommands.option("--db-uri", dest="db_uri", default=None)
@AdminsCommands.option("--user", dest="name", help="User name")
def delete(**kwargs):
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    user = kwargs.get("user")
    if not user:
        print("ERROR: user is required")
        return
    models.ScoreAdministrators.find_by(name=user).delete()


manager.add_command('approved-plugins', ApprovedPluginsCommands)
manager.add_command('service-urls', ServiceUrlCommands)
manager.add_command('service-url-limits', ServiceUrlLimitsCommands)
manager.add_command('users', AdminsCommands)
manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
