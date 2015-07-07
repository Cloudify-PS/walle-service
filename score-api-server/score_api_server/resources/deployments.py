# Copyright (c) 2015 VMware. All rights reserved

import json

from cloudify_rest_client import exceptions

from flask.ext import restful
from flask import request, g, make_response

from score_api_server.common import util


class Deployments(restful.Resource):

    def update_quota(self, increment_or_decrement):
        g.current_org_id_limits = g.current_org_id_limits.update(
            number_of_deployments=(
                g.current_org_id_limits.number_of_deployments
                + increment_or_decrement))

    def can_do_deployment(self):
        if g.current_org_id_limits.deployment_limits == -1 or (
           g.current_org_id_limits.deployment_limits >
           g.current_org_id_limits.number_of_deployments):
            # When deployment limit set to -1 users
            # can deploy infinite number of blueprints.
            # Or deployment limits still greater than number of deployments
            return True
        else:
            return make_response("Deployment quota exceeded.", 403)

    def get(self, deployment_id=None):
        try:
            if deployment_id is not None:
                try:
                    result = g.cc.deployments.get(
                        util.add_org_prefix(deployment_id))
                    return util.remove_org_prefix(result)
                except exceptions.CloudifyClientError as e:
                    return make_response(str(e), e.status_code)
            else:
                deployments = g.cc.deployments.list()
                result = []
                for deployment in deployments:
                    if deployment.id.startswith(g.org_id + '_'):
                        result.append(util.remove_org_prefix(deployment))
                return result
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)

    def delete(self, deployment_id):
        try:
            cfy_dp_id = util.add_org_prefix(deployment_id)

            # necessary to validate that deployment exists
            self.get(deployment_id=cfy_dp_id)
            result = g.cc.deployments.delete(cfy_dp_id)

            self.update_quota(-1)
            return result

        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)

    def put(self, deployment_id):
        blueprint_id = request.json.get('blueprint_id')
        inputs = json.loads(request.json.get('inputs'))
        if self.can_do_deployment():
            try:
                self.update_quota(+1)
                g.cc.blueprints.get(util.add_org_prefix(blueprint_id))
                deployment = g.cc.deployments.create(
                    util.add_org_prefix(blueprint_id),
                    util.add_org_prefix(deployment_id),
                    inputs=inputs)
                return deployment
            except(exceptions.CloudifyClientError,
                   exceptions.MissingRequiredDeploymentInputError,
                   exceptions.UnknownDeploymentInputError) as e:
                self.update_quota(-1)
                return make_response(str(e), e.status_code)
