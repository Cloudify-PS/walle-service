# Copyright (c) 2015 VMware. All rights reserved

from flask_restful_swagger import swagger

from score_api_server.resources import blueprints
from score_api_server.resources import deployments
from score_api_server.resources import executions
from score_api_server.resources import events
from score_api_server.resources import status
from score_api_server.resources import login
from score_api_server.resources import vcloud_instances


def setup_resources(api):
    api = swagger.docs(api,
                       apiVersion='0.1',
                       basePath='http://localhost:8100')
    api.add_resource(blueprints.Blueprints, '/blueprints')
    api.add_resource(blueprints.BlueprintsId,
                     '/blueprints/<string:blueprint_id>')
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
    api.add_resource(login.Login, '/login')
    api.add_resource(vcloud_instances.VCAInstances, '/instances')
