# Copyright (c) 2015 VMware. All rights reserved

from flask import request, g, make_response
from flask.ext import restful
from flask.ext.restful import reqparse

from cloudify_rest_client import exceptions

from score_api_server.common import util

parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')


class Executions(restful.Resource):

    def get(self, execution_id=None):
        args = parser.parse_args()
        try:
            deployment_id = util.add_org_prefix(args['deployment_id'])
            g.cc.deployments.get(deployment_id)
            if not execution_id:
                executions = g.cc.executions.list(deployment_id=deployment_id)
                return executions
            else:
                return g.cc.executions.get(execution_id)
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)

    def post(self):
        deployment_id = util.add_org_prefix(request.json.get('deployment_id'))
        try:
            workflow_id = request.json.get('workflow_id')

            result = g.cc.executions.start(deployment_id, workflow_id)
            return result
        except (exceptions.CloudifyClientError,
                exceptions.DeploymentEnvironmentCreationInProgressError,
                exceptions.DeploymentEnvironmentCreationPendingError) as e:
            # should we wait for deployment environment creation workflow?
            return make_response(str(e), 403)

    def put(self):
        execution_id = request.json.get('execution_id')
        try:
            force = request.json.get('force')
            self.get(execution_id=execution_id)
            result = g.cc.executions.cancel(execution_id, force)
            return result
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)
