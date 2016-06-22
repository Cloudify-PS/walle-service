# Copyright (c) 2015 VMware. All rights reserved

import yaml

from walle_api_server.db import base


class ScoreAdministrators(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'score_admins'

    id = base.db.Column(base.db.String(), primary_key=True)
    name = base.db.Column(base.db.String(), unique=True)
    password = base.db.Column(base.db.String())
    token = base.db.Column(base.db.String())
    expire = base.db.Column(base.db.String())

    def __init__(self, name, password, token='', expire=''):
        self.name = name
        self.password = password
        self.token = token
        self.expire = expire
        super(ScoreAdministrators, self).__init__()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "token": self.token,
            "expire": self.expire
        }


class AllowedServiceUrl(base.BaseDatabaseModel, base.db.Model):
    __tablename__ = 'allowed_service_urls'

    id = base.db.Column(base.db.String(), primary_key=True)
    service_url = base.db.Column(base.db.String())
    tenant = base.db.Column(base.db.String())
    info = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())
    associations = base.db.relationship(
        'ServiceUrlToCloudifyAssociationWithLimits', backref='service',
        lazy='dynamic'
    )

    def __init__(self, service_url, tenant, info=None):
        self.service_url = service_url
        self.tenant = tenant
        self.info = info if info else ""
        super(AllowedServiceUrl, self).__init__()
        self.save()

    def __repr__(self):
        return '#{}: Allowed {} for {}'.format(
            self.id, self.service_url, self.tenant
        )

    def to_dict(self):
        return {
            "id": self.id,
            "service_url": self.service_url,
            "tenant": self.tenant,
            "info": self.info,
            "created_at": self.created_at,
        }


class ServiceUrlToCloudifyAssociationWithLimits(base.BaseDatabaseModel,
                                                base.db.Model):
    __tablename__ = 'service_url_to_cloudify_with_limits'

    id = base.db.Column(base.db.String(), primary_key=True)
    deployment_limits = base.db.Column(base.db.Integer())
    number_of_deployments = base.db.Column(base.db.Integer())
    cloudify_host = base.db.Column(base.db.String())
    cloudify_port = base.db.Column(base.db.String())
    created_at = base.db.Column(base.db.String())
    updated_at = base.db.Column(base.db.String())
    serviceurl_id = base.db.Column(
        base.db.Integer,
        base.db.ForeignKey('allowed_service_urls.id')
    )

    def __init__(self, serviceurl_id, cloudify_host,
                 cloudify_port, deployment_limits=0):
        self.serviceurl_id = serviceurl_id
        self.cloudify_host = cloudify_host
        self.cloudify_port = cloudify_port
        self.deployment_limits = deployment_limits
        self.number_of_deployments = 0
        super(ServiceUrlToCloudifyAssociationWithLimits, self).__init__()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "serviceurl_id": self.serviceurl_id,
            "service_tenant": self.service.tenant,
            "service_url": self.service.service_url,
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
