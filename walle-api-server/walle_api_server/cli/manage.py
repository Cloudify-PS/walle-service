# Copyright (c) 2015 VMware. All rights reserved

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from walle_api_server.cli import app
from walle_api_server.db import models
from walle_api_server.common import print_utils
from walle_api_server.common import manage_limits


db = app.db
flask_app = app.app

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)


EndpointCommands = Manager(usage="Performs action related to "
                           "Endpoints URLs")
TenantCommands = Manager(usage="Performs action related to "
                         "tenants")
RightsCommands = Manager(usage="Performs action related to "
                         "create new user role")
TenantRightsCommands = Manager(usage="Performs action related to "
                               "create new role to tenant")
LimitCommands = Manager(usage="Performs action related to "
                        "tenants limits")
ApprovedPluginsCommands = Manager(usage="Performs actions related to approved "
                                  "deployment and workflow plugins.")
AdminsCommands = Manager(usage="Performs actions related to walle "
                         "administrators")


# ApprovedPlugins
@ApprovedPluginsCommands.option("--name", dest="name",
                                help="Approved plugin name.")
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


# Endpoint URLs
@EndpointCommands.option("--endpoint-url", dest="endpoint_url",
                         help="Adds endpoint-url to Walle DB")
@EndpointCommands.option("--type", dest="type",
                         help="Endpoint type, e.g. openstack")
@EndpointCommands.option("--version", dest="version",
                         help="Endpoint version")
@EndpointCommands.option("--description", dest="description",
                         help="Some more information about andpoint")
@EndpointCommands.option("--db-uri", dest="db_uri", default=None)
def add(endpoint_url, type, version, description, db_uri=None):
    """Adds endpoint-url."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.endpoint_add(
        endpoint_url, type, version, description
    )
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print(value)


@EndpointCommands.option("--endpoint-url", dest="endpoint-url",
                         help="delete endpoint-url from Walle DB")
@EndpointCommands.option("--type", dest="type",
                         help="Endpoint type, e.g. openstack")
@EndpointCommands.option("--db-uri", dest="db_uri", default=None)
def delete(endpoint_url, type, db_uri=None):
    """Deletes endpoint."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.endpoint_delete(endpoint_url, type)
    print(value)


@EndpointCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists service-urls."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.endpoint_list()
    print_utils.print_list(
        value, ["id", "endpoint", "type", "version", "description",
                "created_at"]
    )


# Tenants
@TenantCommands.option("--endpoint-url", dest="endpoint_url",
                       help="Endpoint url")
@TenantCommands.option("--type", dest="type",
                       help="Endpoint type, e.g. openstack")
@TenantCommands.option("--tenant", dest="tenant_name",
                       help="Adds tenant to Walle DB")
@TenantCommands.option("--cloudify-host", dest="cloudify_host")
@TenantCommands.option("--cloudify-port", dest="cloudify_port")
@TenantCommands.option("--description", dest="description",
                       help="Some more information about andpoint")
@TenantCommands.option("--db-uri", dest="db_uri", default=None)
def add(endpoint_url, type, tenant_name, cloudify_host, cloudify_port,
        description, db_uri=None):
    """Creates tenant pinned to specific
       endpoint-url and specific Cloudify Manager
    """
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.tenant_add(
        endpoint_url, type, tenant_name, cloudify_host, cloudify_port,
        description
    )
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print(value)


@TenantCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists all tenants."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.tenant_list()
    print_utils.print_list(
        value, ["id", "tenant_name", "endpoint", "created_at",
                "updated_at", "cloudify_host", "description"]
    )


@TenantCommands.option("--id", dest="id")
@TenantCommands.option("--endpoint-id", dest="endpoint_id")
@TenantCommands.option("--tenant", dest="tenant_name",
                       help="Adds tenant to Walle DB")
@TenantCommands.option("--cloudify-host", dest="cloudify_host")
@TenantCommands.option("--cloudify-port", dest="cloudify_port")
@TenantCommands.option("--description", dest="description",
                       help="Some more information about andpoint")
@TenantCommands.option("--db-uri", dest="db_uri", default=None)
def update(**kwargs):
    """Updates service-url limits with given keys by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.tenant_update(**kwargs)
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print (value)


@TenantCommands.option("--id", dest="id")
@TenantCommands.option("--db-uri", dest="db_uri", default=None)
def delete(id, db_uri=None):
    """Deletes tenant by its ID."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.tenant_delete(id)
    print(value)


# Tenants limit
@LimitCommands.option("--endpoint-url", dest="endpoint_url",
                      help="Endpoint url")
@LimitCommands.option("--type", dest="type",
                      help="Endpoint type, e.g. openstack")
@LimitCommands.option("--tenant", dest="tenant_name",
                      help="Adds tenant to Walle DB")
@LimitCommands.option("--limit-type", dest="limit_type",
                      help="Limit type, e.g.: deploymnets, ram, cpu")
@LimitCommands.option("--soft", dest="soft",
                      help="Soft limit")
@LimitCommands.option("--hard", dest="hard",
                      help="Soft limit")
@LimitCommands.option("--db-uri", dest="db_uri", default=None)
def add(endpoint_url, type, tenant_name, limit_type, soft, hard, db_uri=None):
    """Creates tenant limits"""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.limit_add(
        endpoint_url, type, tenant_name, limit_type, soft, hard
    )
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print(value)


@LimitCommands.option("--db-uri", dest="db_uri", default=None)
def list(**kwargs):
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.limit_list()
    print_utils.print_list(
        value, ["id", "tenant", "soft", "hard", "type", "created_at",
                "updated_at", "value"]
    )


@LimitCommands.option("--id", dest="id")
@LimitCommands.option("--tenant-id", dest="tenant_id")
@LimitCommands.option("--limit-type", dest="type",
                      help="Limit type, e.g.: deployments, ram, cpu")
@LimitCommands.option("--soft", dest="soft",
                      help="Soft limit")
@LimitCommands.option("--hard", dest="hard",
                      help="Soft limit")
@LimitCommands.option("--db-uri", dest="db_uri", default=None)
def update(**kwargs):
    """Updates service-url limits with given keys by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.limit_update(**kwargs)
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print (value)


@LimitCommands.option("--id", dest="id")
@LimitCommands.option("--db-uri", dest="db_uri", default=None)
def delete(**kwargs):
    """Deletes limit by its ID."""
    db_uri = kwargs.get("db_uri")
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.limit_delete(id)
    print(value)


# Administrators
@AdminsCommands.option("--user", dest="user",
                       help="Adds walle admins to Walle DB")
@AdminsCommands.option("--password", dest="password",
                       help="Adds walle admins to Walle DB")
@AdminsCommands.option("--db-uri", dest="db_uri", default=None)
def add(user, password, db_uri=None):
    """Adds walle administrator."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    if not user or not password:
        print("ERROR: user and password are required")
    else:
        admin = models.WalleAdministrators(user, password)
        print_utils.print_dict(admin.to_dict())


@AdminsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists administrators"""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    admins = models.WalleAdministrators.list()
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
    models.WalleAdministrators.find_by(name=user).delete()


# Rights
@RightsCommands.option("--name", dest="name",
                       help="Adds new role/right")
@RightsCommands.option("--description", dest="description",
                       help="Some short description about role", default=None)
@RightsCommands.option("--db-uri", dest="db_uri", default=None)
def add(name, description, db_uri=None):
    """Adds walle role."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.rights_add(name, description)
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print (value)


@RightsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists avaible roles."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.rights_list()
    print_utils.print_list(
        value, ["id", "name", "description", "created_at"]
    )


@RightsCommands.option("--id", dest="id",
                         help="Rights by id")
@RightsCommands.option("--db-uri", dest="db_uri", default=None)
def delete(id, db_uri=None):
    """Deletes endpoint."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.rights_delete(id)
    print(value)


# Tenant Rights
@TenantRightsCommands.option("--tenant-id", dest="tenant",
                       help="Tenant id")
@TenantRightsCommands.option("--right-id", dest="right",
                       help="Rights Id")
@TenantRightsCommands.option("--db-uri", dest="db_uri", default=None)
def add(tenant, right, db_uri=None):
    """Adds walle role."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    status, value = manage_limits.tenant_rights_add(tenant, right)
    if status:
        print_utils.print_dict(value.to_dict())
    else:
        print (value)


@TenantRightsCommands.option("--db-uri", dest="db_uri", default=None)
def list(db_uri=None):
    """Lists avaible tenant/roles."""

    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.tenant_rights_list()
    print_utils.print_list(
        value, ["id", "rights_id", "tenant_id"]
    )


@TenantRightsCommands.option("--id", dest="id",
                         help="Delete Tenant/Right record by id")
@TenantRightsCommands.option("--db-uri", dest="db_uri", default=None)
def delete(id, db_uri=None):
    """Deletes endpoint."""
    if db_uri:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    _, value = manage_limits.tenant_rights_delete(id)
    print(value)


manager.add_command('approved-plugins', ApprovedPluginsCommands)
manager.add_command('endpoints', EndpointCommands)
manager.add_command('tenants', TenantCommands)
manager.add_command('rights', RightsCommands)
manager.add_command('tenantrights', TenantRightsCommands)
manager.add_command('limits', LimitCommands)
manager.add_command('users', AdminsCommands)
manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
