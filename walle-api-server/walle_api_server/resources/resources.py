# Copyright (c) 2015 VMware. All rights reserved

from flask_restful_swagger import swagger

from walle_api_server.resources import blueprints
from walle_api_server.resources import deployments
from walle_api_server.resources import executions
from walle_api_server.resources import events
from walle_api_server.resources import status
from walle_api_server.resources import login_vcloud
from walle_api_server.resources import login_openstack
from walle_api_server.resources import login_walle
from walle_api_server.resources import endpoints
from walle_api_server.resources import plugins
from walle_api_server.resources import tenants
from walle_api_server.resources import tenantlimits
from walle_api_server.resources import service
from walle_api_server.resources import nodes


def setup_resources(api):
    api = swagger.docs(api,
                       apiVersion='0.1',
                       basePath='http://localhost:5000')
    api.add_resource(blueprints.Blueprints, '/blueprints')
    api.add_resource(blueprints.BlueprintsId,
                     '/blueprints/<string:blueprint_id>')
    api.add_resource(blueprints.BlueprintArchive,
                     '/blueprints/<string:blueprint_id>/archive')
    api.add_resource(deployments.Deployments, '/deployments')
    api.add_resource(deployments.DeploymentsId,
                     '/deployments/<string:deployment_id>')
    api.add_resource(deployments.DeploymentOutputs,
                     '/deployments/<string:deployment_id>/outputs')
    api.add_resource(deployments.DeploymentsUpdates, '/deployment-updates')
    api.add_resource(executions.Executions, '/executions')
    api.add_resource(executions.ExecutionsId,
                     '/executions/<string:execution_id>')
    api.add_resource(events.Events, '/events')
    api.add_resource(status.Status, '/status')
    api.add_resource(login_vcloud.LoginVcloud, '/login_vcloud')
    api.add_resource(login_openstack.LoginOpenStack, '/login_openstack')

    # admin part, you must have rights for do operation from this section
    # look to rights table, partial copy of manage section
    api.add_resource(endpoints.Endpoints, '/endpoints')
    api.add_resource(endpoints.EndpointsId, '/endpoints/<string:id>/')
    api.add_resource(tenants.Tenants, '/tenants')
    api.add_resource(tenants.TenantsId, '/tenants/<string:id>')
    api.add_resource(tenantlimits.Limits, '/limits')
    api.add_resource(tenantlimits.LimitsId, '/limits/<string:id>')

    # walle admin part, will check walle auth
    api.add_resource(login_walle.LoginWalle, '/login_walle')
    api.add_resource(plugins.ApprovedPlugins, '/manage/approved_plugins')
    api.add_resource(plugins.ApprovedPluginsFromFile,
                     '/manage/approved_plugins/from_file')
    api.add_resource(plugins.ApprovedPluginsId,
                     '/manage/approved_plugins/<string:name>')
    api.add_resource(service.Maintenance, '/maintenance')
    api.add_resource(nodes.Nodes, '/nodes')
    api.add_resource(nodes.NodeInstances, '/node-instances')
