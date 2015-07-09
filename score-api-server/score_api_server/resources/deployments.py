# Copyright (c) 2015 VMware. All rights reserved

import json
import flask

from cloudify_rest_client import exceptions

from flask.ext import restful
from flask import request, g, make_response

from score_api_server.common import util

app = flask.Flask(__name__)


class Deployments(restful.Resource):

    def update_quota(self, increment_or_decrement):
        app.logger.debug("Entering Deployments.update_qouta method.")
        g.current_org_id_limits = g.current_org_id_limits.update(
            number_of_deployments=(
                g.current_org_id_limits.number_of_deployments
                + increment_or_decrement))
        app.logger.debug("Done. "
                         "Exiting Deployments.update_qouta method.")

    def can_do_deployment(self):
        app.logger.debug(
            "Entering Deployments.can_do_deployment method.")
        if g.current_org_id_limits.deployment_limits == -1 or (
           g.current_org_id_limits.deployment_limits >
           g.current_org_id_limits.number_of_deployments):
            # When deployment limit set to -1 users
            # can deploy infinite number of blueprints.
            # Or deployment limits still greater than number of deployments
            app.logger.info(
                "Success. Deployment can be done for Org-ID:%s .", g.org_id)
            app.logger.debug(
                "Done. Exiting Deployments.can_do_deployment method.")
            return True
        else:
            app.logger.debug("Deployment quota exceeded for Org-ID:%s.",
                             g.org_id)
            return make_response("Deployment quota exceeded.", 403)

    def get(self, deployment_id=None):
        app.logger.debug("Entering Deployments.get method.")
        try:
            if deployment_id is not None:
                app.logger.info("Seeking for deplyment %s .",
                                deployment_id)
                result = g.cc.deployments.get(
                    util.add_org_prefix(deployment_id))
                app.logger.info("Deployment found.")
                return util.remove_org_prefix(result), 200
            else:
                app.logger.info("Listing all deployments.")
                deployments = g.cc.deployments.list()
                result = []
                for deployment in deployments:
                    if deployment.id.startswith(g.org_id + '_'):
                        result.append(util.remove_org_prefix(deployment))
                app.logger.debug(
                    "Done. Exiting Deployments.get method.")
                return result, 200
        except exceptions.CloudifyClientError as e:
            app.logger.error(str(e))
            return make_response(str(e), e.status_code)

    def delete(self, deployment_id):
        app.logger.debug("Entering Deployments.delete method.")
        try:
            cfy_dp_id = util.add_org_prefix(deployment_id)

            # necessary to validate that deployment exists
            app.logger.info("Checking if deployment %s exists.",
                            deployment_id)
            self.get(deployment_id=cfy_dp_id)
            app.logger.info("Deleting deployment %s.", deployment_id)
            result = g.cc.deployments.delete(cfy_dp_id)
            self.update_quota(-1)
            app.logger.debug("Done. Exiting Deployments.delete method.")
            return result, 202

        except exceptions.CloudifyClientError as e:
            app.logger.error(str(e))
            return make_response(str(e), e.status_code)

    def put(self, deployment_id):
        app.logger.debug("Entering Deployments.put method.")
        blueprint_id = request.json.get('blueprint_id')
        inputs = json.loads(request.json.get('inputs'))
        if self.can_do_deployment():
            try:
                app.logger.info("Updating quota for Org-ID %s.",
                                g.org_id)
                self.update_quota(+1)
                app.logger.info("Checking if blueprint %s exists.",
                                blueprint_id)
                g.cc.blueprints.get(util.add_org_prefix(blueprint_id))
                deployment = g.cc.deployments.create(
                    util.add_org_prefix(blueprint_id),
                    util.add_org_prefix(deployment_id),
                    inputs=inputs)
                app.logger.debug("Done. Exiting Deployments.put method.")
                return deployment, 201
            except(exceptions.CloudifyClientError,
                   exceptions.MissingRequiredDeploymentInputError,
                   exceptions.UnknownDeploymentInputError) as e:
                app.logger.error(str(e))
                app.logger.error("Decreasing quota.")
                self.update_quota(-1)
                return make_response(str(e), e.status_code)
