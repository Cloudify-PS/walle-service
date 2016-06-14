# Copyright (c) 2015 VMware. All rights reserved

from flask_restful_swagger import swagger

from score_api_server.resources import blueprints
from score_api_server.resources import deployments
from score_api_server.resources import executions
from score_api_server.resources import events
from score_api_server.resources import status
from score_api_server.resources import login_vcloud
from score_api_server.resources import login_openstack
from score_api_server.resources import login_score
from score_api_server.resources import manage


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
    api.add_resource(executions.Executions, '/executions')
    api.add_resource(executions.ExecutionsId,
                     '/executions/<string:execution_id>')
    api.add_resource(events.Events, '/events')
    api.add_resource(status.Status, '/status')
    api.add_resource(login_vcloud.LoginVcloud, '/login_vcloud')
    api.add_resource(login_openstack.LoginOpenStack, '/login_openstack')
    api.add_resource(login_score.LoginScore, '/login_score')
    api.add_resource(manage.OrgIds, '/manage/org_ids')
    api.add_resource(manage.OrgIdsId, '/manage/org_ids/<string:org_id>')
    api.add_resource(manage.OrgIdLimits, '/manage/org_id_limits')
    api.add_resource(manage.OrgIdLimitsId,
                     '/manage/org_id_limits/<string:id>')
    api.add_resource(manage.KeystoreUrls, '/manage/keystore_urls')
    api.add_resource(manage.KeystoreUrlsId,
                     '/manage/keystore_urls/<string:keystore_url>')
    api.add_resource(manage.KeyStoreUrlLimits,
                     '/manage/keystore_url_limits')
    api.add_resource(manage.KeyStoreUrlLimitsId,
                     '/manage/keystore_url_limits/<string:id>')
    api.add_resource(manage.ApprovedPlugins, '/manage/approved_plugins')
    api.add_resource(manage.ApprovedPluginsFromFile,
                     '/manage/approved_plugins/from_file')
    api.add_resource(manage.ApprovedPluginsId,
                     '/manage/approved_plugins/<string:name>')
