# Copyright (c) 2015 VMware. All rights reserved

import flask

from flask import request, g, make_response
from flask.ext import restful
from flask.ext.restful import reqparse

from cloudify_rest_client import exceptions

from score_api_server.common import util

app = flask.Flask(__name__)
parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')


class Executions(restful.Resource):

    def get(self, execution_id=None):
        app.logger.debug("Entering Execution.get method.")
        args = parser.parse_args()
        try:
            deployment_id = util.add_org_prefix(args['deployment_id'])
            app.logger.info("Checking if deployment %s exists.",
                            deployment_id)
            g.cc.deployments.get(deployment_id)
            if not execution_id:
                app.logger.info(
                    "Listing all executions for deployment %s .",
                    deployment_id)
                executions = g.cc.executions.list(
                    deployment_id=deployment_id)
                return executions
            else:
                app.logger.info(
                    "Seeking for executions by deployment %s.",
                    deployment_id)
                result = g.cc.executions.get(execution_id)
                app.logger.debug("Done. Exiting Executions.get method.")
                return result
        except exceptions.CloudifyClientError as e:
            app.logger.error(str(e))
            return make_response(str(e), e.status_code)

    def post(self):
        app.logger.debug("Entering Execution.post method.")
        deployment_id = util.add_org_prefix(request.json.get('deployment_id'))
        try:
            workflow_id = request.json.get('workflow_id')
            app.logger.info("Looking for deployment %s .", deployment_id)
            g.cc.deployments.get(deployment_id)
            app.logger.info("Staring workflow %s for deployment %s.",
                            workflow_id, deployment_id)
            result = g.cc.executions.start(deployment_id, workflow_id)
            app.logger.debug("Done. Exiting Executions.post method.")
            return result
        except (exceptions.CloudifyClientError,
                exceptions.DeploymentEnvironmentCreationInProgressError,
                exceptions.DeploymentEnvironmentCreationPendingError) as e:
            # should we wait for deployment environment creation workflow?
            app.logger.error(str(e))
            return make_response(str(e), 403)

    def put(self):
        app.logger.debug("Entering Execution.put method.")
        execution_id = request.json.get('execution_id')
        try:
            force = request.json.get('force')
            self.get(execution_id=execution_id)
            result = g.cc.executions.cancel(execution_id, force)
            app.logger.debug("Done. Exiting Executions.put method.")
            return result
        except exceptions.CloudifyClientError as e:
            app.logger.error(str(e))
            return make_response(str(e), e.status_code)
