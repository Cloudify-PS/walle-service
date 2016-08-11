# Copyright (c) 2015 VMware. All rights reserved

from flask_restful_swagger import swagger

from walle_api_server.resources import blueprints
from walle_api_server.resources import deployments
from walle_api_server.resources import executions
from walle_api_server.resources import events
from walle_api_server.resources import login_vcloud
from walle_api_server.resources import login_openstack
from walle_api_server.resources import login_walle
from walle_api_server.resources import endpoints
from walle_api_server.resources import plugins
from walle_api_server.resources import tenants
from walle_api_server.resources import tenantlimits
from walle_api_server.resources import service
from walle_api_server.resources import nodes
from walle_api_server.resources import backend


def setup_resources(api):
    api = swagger.docs(api,
                       apiVersion='0.1')
    _set_versioned_urls(api, blueprints.Blueprints, '/blueprints')
    _set_versioned_urls(api, blueprints.BlueprintsId,
                        '/blueprints/<string:blueprint_id>')
    _set_versioned_urls(api, blueprints.BlueprintArchive,
                        '/blueprints/<string:blueprint_id>/archive')
    _set_versioned_urls(api, deployments.Deployments, '/deployments')
    _set_versioned_urls(api, deployments.DeploymentsId,
                        '/deployments/<string:deployment_id>')
    _set_versioned_urls(api, deployments.DeploymentOutputs,
                        '/deployments/<string:deployment_id>/outputs')
    _set_versioned_urls(api, deployments.DeploymentsUpdates,
                        '/deployment-updates')
    _set_versioned_urls(api, executions.Executions, '/executions')
    _set_versioned_urls(api, executions.ExecutionsId,
                        '/executions/<string:execution_id>')
    _set_versioned_urls(api, events.Events, '/events')
    _set_versioned_urls(api, service.Status, '/status')
    _set_versioned_urls(api, service.Maintenance, '/maintenance')
    _set_versioned_urls(api, service.Version, '/version')
    _set_versioned_urls(api, service.Context, '/provider/context')
    _set_versioned_urls(api, nodes.Nodes, '/nodes')
    _set_versioned_urls(api, nodes.NodeInstances, '/node-instances')
    _set_versioned_urls(api, login_vcloud.LoginVcloud, '/login_vcloud')
    _set_versioned_urls(api, login_openstack.LoginOpenStack, '/login_openstack')

    # backend part
    api.add_resource(blueprints.BlueprintsUpload, '/backend/blueprints/upload')
    api.add_resource(backend.Ui, '/backend/versions/ui')
    api.add_resource(backend.Logined, '/backend/isLoggedIn')
    api.add_resource(backend.Latest, '/backend/version/latest')
    api.add_resource(backend.Logout, '/backend/logout')

    # admin part, you must have rights for do operation from this section
    # look to rights table, partial copy of manage section
    _set_versioned_urls(api, endpoints.Endpoints, '/endpoints')
    _set_versioned_urls(api, endpoints.EndpointsId, '/endpoints/<string:id>/')
    _set_versioned_urls(api, tenants.Tenants, '/tenants')
    _set_versioned_urls(api, tenants.TenantsId, '/tenants/<string:id>')
    _set_versioned_urls(api, tenantlimits.Limits, '/limits')
    _set_versioned_urls(api, tenantlimits.LimitsId, '/limits/<string:id>')

    # walle admin part, will check walle auth
    _set_versioned_urls(api, login_walle.LoginWalle, '/login_walle')
    _set_versioned_urls(api, plugins.ApprovedPlugins,
                        '/manage/approved_plugins')
    _set_versioned_urls(api, plugins.ApprovedPluginsFromFile,
                        '/manage/approved_plugins/from_file')
    _set_versioned_urls(api, plugins.ApprovedPluginsId,
                        '/manage/approved_plugins/<string:name>')


def _set_versioned_urls(api, resource, suffix):
    api.add_resource(resource, '/api/v2.1' + suffix)
