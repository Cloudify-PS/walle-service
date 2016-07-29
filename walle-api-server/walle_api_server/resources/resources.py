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
from walle_api_server.resources import manage


def setup_resources(api):
    api = swagger.docs(api,
                       apiVersion='0.1',
                       basePath='http://172.17.0.2:8001')
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
    api.add_resource(executions.Executions, '/executions')
    api.add_resource(executions.ExecutionsId,
                     '/executions/<string:execution_id>')
    api.add_resource(events.Events, '/events')
    api.add_resource(status.Status, '/status')
    api.add_resource(login_vcloud.LoginVcloud, '/login_vcloud')
    api.add_resource(login_openstack.LoginOpenStack, '/login_openstack')
    api.add_resource(login_walle.LoginWalle, '/login_walle')
    api.add_resource(manage.Endpoints, '/manage/endpoints')
    api.add_resource(manage.EndpointsId,
                     '/manage/endpoints/<string:id>/')
    api.add_resource(manage.Tenants,
                     '/manage/tenants')
    api.add_resource(manage.TenantsId,
                     '/manage/tenants/<string:id>')
    api.add_resource(manage.Limits,
                     '/manage/limits')
    api.add_resource(manage.LimitsId,
                     '/manage/limits/<string:id>')
    api.add_resource(manage.ApprovedPlugins, '/manage/approved_plugins')
    api.add_resource(manage.ApprovedPluginsFromFile,
                     '/manage/approved_plugins/from_file')
    api.add_resource(manage.ApprovedPluginsId,
                     '/manage/approved_plugins/<string:name>')
