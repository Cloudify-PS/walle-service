# Copyright (c) 2015 VMware. All rights reserved

import yaml

from walle_api_server.db import base

# uuid size
ID_SIZE = 36
# size of name fileds
# look to limit in openstack
# keystone "project" table
# keystone/common/sql/migrate_repo/versions/067_kilo.py#L95
NAME_SIZE = 64
# look to limit in openstack
# keystone "endpoint" table, we dont have any limits,
# but for 2048 must be enough
# keystone/common/sql/migrate_repo/versions/067_kilo.py#L65
URL_SIZE = 2048
# size for hash fields
MD5_SIZE = 32
# description size
DESCRIPTION_SIZE = 1024
# type size, some string that can describe object type
TYPE_SIZE = 32
# version string
VERSION_SIZE = 16
# Table version, for renerate all tables at once, use some value before
# regenerate all tables
TABLES_VERSION = ""


class Endpoint(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'endpoints' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    endpoint = base.db.Column(base.db.String(URL_SIZE))
    type = base.db.Column(base.db.String(TYPE_SIZE))
    version = base.db.Column(base.db.String(VERSION_SIZE))
    description = base.db.Column(base.db.String(DESCRIPTION_SIZE))
    created_at = base.db.Column(base.db.DateTime())
    associations = base.db.relationship(
        'Tenant', backref='endpoint',
        lazy='dynamic'
    )

    def __init__(self, endpoint, type=None, version=None, description=None):
        self.endpoint = endpoint
        self.type = type if type else "openstack"
        self.version = version if version else "any"
        self.description = description if description else ""
        super(Endpoint, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {} for {}'.format(
            self.id, self.endpoint, self.type
        )

    def to_dict(self):
        return {
            "id": self.id,
            "endpoint": self.endpoint,
            "type": self.type,
            "version": self.version,
            "description": self.description,
            "created_at": str(self.created_at),
        }


# Rights/group/role for tenant
class Rights(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'rights' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    name = base.db.Column(base.db.String(NAME_SIZE))
    description = base.db.Column(base.db.String(DESCRIPTION_SIZE))
    created_at = base.db.Column(base.db.DateTime())
    updated_at = base.db.Column(base.db.DateTime())

    def __init__(self, name, description=None):
        self.name = name
        self.description = description if description else ""
        super(Rights, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: {} can be used for {}'.format(
            self.id, self.name, self.description
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


# Users with some special rights, like admin,
# can be not admin in endpoint rights system
class UserRights(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'user_rights' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    user_id = base.db.Column(
        base.db.String(ID_SIZE))
    rights_id = base.db.Column(
        base.db.String(ID_SIZE),
        base.db.ForeignKey('rights' + TABLES_VERSION + '.id')
    )

    right = base.db.relationship("Rights")

    created_at = base.db.Column(base.db.DateTime())
    updated_at = base.db.Column(base.db.DateTime())

    def __init__(self, user_id, rights_id):
        self.user_id = user_id
        self.rights_id = rights_id
        super(UserRights, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {} for {}'.format(
            self.id, self.rights_id, self.user_id
        )

    def to_dict(self):
        return {
            "id": self.id,
            "rights_id": self.rights_id,
            "user_id": self.user_id
        }


# Common users without any special rights, used only for create
# relations between tenant user and cloudify manager host plus limits
class Tenant(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'tenants' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    tenant_name = base.db.Column(base.db.String(NAME_SIZE))
    tenant_id = base.db.Column(base.db.String(NAME_SIZE))
    description = base.db.Column(base.db.String(DESCRIPTION_SIZE))
    endpoint_id = base.db.Column(
        base.db.String(ID_SIZE),
        base.db.ForeignKey('endpoints' + TABLES_VERSION + '.id')
    )
    cloudify_host = base.db.Column(base.db.String(URL_SIZE))
    cloudify_port = base.db.Column(base.db.Integer())
    created_at = base.db.Column(base.db.DateTime())
    updated_at = base.db.Column(base.db.DateTime())
    associations = base.db.relationship(
        'Limit', backref='tenant',
        lazy='dynamic'
    )

    def __init__(self, endpoint_id, tenant_name, cloudify_host,
                 cloudify_port, description=None):
        self.endpoint_id = endpoint_id
        self.tenant_name = tenant_name
        self.cloudify_host = cloudify_host
        self.cloudify_port = cloudify_port
        self.description = description if description else ""
        super(Tenant, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {} for {}'.format(
            self.id, self.endpoint_id, self.tenant_name
        )

    def to_dict(self):
        return {
            "id": self.id,
            "endpoint_id": self.endpoint_id,
            "tenant_name": self.tenant_name,
            "endpoint": self.endpoint.endpoint if self.endpoint else "",
            "type": self.endpoint.type if self.endpoint else "",
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "cloudify_host": self.cloudify_host,
            "cloudify_port": self.cloudify_port,
            "description": self.description
        }


class Limit(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'limits' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    tenant_id = base.db.Column(
        base.db.String(ID_SIZE),
        base.db.ForeignKey('tenants' + TABLES_VERSION + '.id')
    )
    soft = base.db.Column(base.db.Integer())
    hard = base.db.Column(base.db.Integer())
    value = base.db.Column(base.db.Integer())
    type = base.db.Column(base.db.String(TYPE_SIZE))
    created_at = base.db.Column(base.db.DateTime())
    updated_at = base.db.Column(base.db.DateTime())

    def __init__(self, tenant_id, soft=0, hard=0, type=None, value=0):
        self.tenant_id = tenant_id
        self.soft = soft
        self.hard = hard
        self.type = type if type else "deployments"
        self.value = value
        super(Limit, self).__init__()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "soft": self.soft,
            "hard": self.hard,
            "type": self.type,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "value": self.value
        }


class ApprovedPlugins(base.BaseDatabaseModel,
                      base.db.Model):

    __tablename__ = 'approved_plugins' + TABLES_VERSION

    id = base.db.Column(base.db.String(ID_SIZE), primary_key=True)
    name = base.db.Column(base.db.String(NAME_SIZE))
    source = base.db.Column(base.db.String(URL_SIZE))
    plugin_type = base.db.Column(base.db.String(TYPE_SIZE))

    def __init__(self, name, source, plugin_type):
        """Creates an approved plugin entity for blueprints
           security validation
        :param name: approved plugin name
        :type name: basestring
        :param source: approved plugin source
        :type source: basestring
        :param type: approved plugin type
        :type type: basestring
        """
        self.name = name
        self.source = (None if not source and source != '' else source)
        self.plugin_type = plugin_type
        super(ApprovedPlugins, self).__init__()
        self.save()

    @classmethod
    def _register_plugin(cls, list_of_plugins, _type):
        _plugins = []
        for plugin in list_of_plugins:
            _name = plugin.keys()[0]
            _sources = plugin[_name]['source']
            _type = _type
            for _source in _sources:
                _plugins.append(cls(
                    _name, _source, _type))
        return _plugins

    @classmethod
    def register_from_file(cls, from_file):
        _plugins = []
        with open(from_file) as f:
            a_p = yaml.load(f.read())
            d_ps, w_ps = (a_p.get("deployment_plugins"),
                          a_p.get("workflow_plugins"))

            _plugins.extend(
                cls._register_plugin(d_ps, "deployment_plugins"))
            _plugins.extend(
                cls._register_plugin(w_ps, "workflow_plugins"))

            return _plugins

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "plugin_type": self.plugin_type
        }
