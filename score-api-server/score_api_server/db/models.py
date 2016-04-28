# Copyright (c) 2015 VMware. All rights reserved

import yaml

from score_api_server.db import base

class AllowedKeyStoreUrl(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'allowed_ketstore_urls'

    id = base.db.Column(base.db.String(), primary_key=True)
    keystore_url = base.db.Column(base.db.String(), unique=True)
    info = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())

    def __init__(self, keystore_url, info=None):
        self.keystore_url = keystore_url
        self.info = info if info else ""
        super(AllowedKeyStoreUrl, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {}'.format(
            self.id, self.keystore_url
        )

    def to_dict(self):
        return {
            "id": self.id,
            "keystore_url": self.keystore_url,
            "info": self.info,
            "created_at": self.created_at,
        }

class KeyStoreUrlToCloudifyAssociationWithLimits(base.BaseDatabaseModel,
                                           base.db.Model):
    __tablename__ = 'keystore_url_to_cloudify_with_limits'

    id = base.db.Column(base.db.String(), primary_key=True)
    keystore_url = base.db.Column(base.db.String(), unique=True)
    deployment_limits = base.db.Column(base.db.Integer())
    number_of_deployments = base.db.Column(base.db.Integer())
    cloudify_host = base.db.Column(base.db.String())
    cloudify_port = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())
    updated_at = base.db.Column(base.db.String())

    def __init__(self, keystore_url, cloudify_host,
                 cloudify_port, deployment_limits=0):
        self.keystore_url = keystore_url
        self.cloudify_host = cloudify_host
        self.cloudify_port = cloudify_port
        self.deployment_limits = deployment_limits
        self.number_of_deployments = 0
        super(KeyStoreUrlToCloudifyAssociationWithLimits, self).__init__()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "keystore_url": self.keystore_url,
            "deployment_limits": self.deployment_limits,
            "number_of_deployments": self.number_of_deployments,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "cloudify_host": self.cloudify_host,
            "cloudify_port": self.cloudify_port
        }


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


class ApprovedPlugins(base.BaseDatabaseModel,
                      base.db.Model):

    __tablename__ = 'approved_plugins'

    id = base.db.Column(base.db.String(), primary_key=True)
    name = base.db.Column(base.db.String())
    source = base.db.Column(base.db.String())
    plugin_type = base.db.Column(base.db.String())

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
        self.source = (None if not source
                       and source != ''
                       else source)
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
