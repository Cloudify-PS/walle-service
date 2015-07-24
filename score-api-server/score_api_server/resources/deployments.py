# Copyright (c) 2015 VMware. All rights reserved

import json


from cloudify_rest_client import exceptions

from flask.ext import restful
from flask import request, g, make_response
from flask_restful_swagger import swagger

from score_api_server.common import util
from score_api_server.resources import responses

logger = util.setup_logging(__name__)


class Deployments(restful.Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Deployment.__name__),
        nickname="list",
        notes="Returns a list of existing deployments.",
    )
    def get(self):
        logger.debug("Entering Deployments.get method.")
        try:
            logger.info("Listing all deployments.")
            deployments = g.cc.deployments.list()
            result = []
            for deployment in deployments:
                if deployment.id.startswith(g.org_id + '_'):
                    result.append(util.remove_org_prefix(deployment))
            logger.debug("Done. Exiting Deployments.get method.")
            return result
        except exceptions.CloudifyClientError as e:
            return util.make_response_from_exception(e)


class DeploymentsId(restful.Resource):

    def update_quota(self, increment_or_decrement):
        logger.debug("Entering Deployments.update_qouta method.")
        g.current_org_id_limits = g.current_org_id_limits.update(
            number_of_deployments=(
                g.current_org_id_limits.number_of_deployments
                + increment_or_decrement))
        logger.debug("Done. Exiting Deployments.update_qouta method.")

    def can_do_deployment(self):
        logger.debug(
            "Entering Deployments.can_do_deployment method.")
        if g.current_org_id_limits.deployment_limits == -1 or (
           g.current_org_id_limits.deployment_limits >
           g.current_org_id_limits.number_of_deployments):
            # When deployment limit set to -1 users
            # can deploy infinite number of blueprints.
            # Or deployment limits still greater than number of deployments
            logger.info(
                "Success. Deployment can be done for Org-ID:%s .", g.org_id)
            logger.debug(
                "Done. Exiting Deployments.can_do_deployment method.")
            return True
        else:
            logger.debug("Deployment quota exceeded for Org-ID:%s.",
                         g.org_id)
            return make_response("Deployment quota exceeded.", 403)

    @swagger.operation(
        responseClass=responses.Deployment,
        nickname="getById",
        notes="Returns a deployment by its ID.",
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}]
    )
    def get(self, deployment_id=None):
        logger.debug("Entering DeploymentsId.get method.")
        try:
            logger.info("Seeking for deplyment %s .",
                        deployment_id)
            result = g.cc.deployments.get(util.add_org_prefix(deployment_id))
            logger.info("Deployment found.")
            return util.remove_org_prefix(result)
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)

    @swagger.operation(
        responseClass=responses.Deployment,
        nickname="deleteById",
        notes="Deletes a deployment by its ID.",
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}]
    )
    def delete(self, deployment_id):
        logger.debug("Entering Deployments.delete method.")
        try:
            cfy_dp_id = util.add_org_prefix(deployment_id)

            # necessary to validate that deployment exists
            logger.info("Checking if deployment %s exists.",
                        deployment_id)
            self.get(deployment_id=cfy_dp_id)
            logger.info("Deleting deployment %s.", deployment_id)
            result = g.cc.deployments.delete(cfy_dp_id)
            self.update_quota(-1)
            logger.debug("Done. Exiting Deployments.delete method.")
            return util.remove_org_prefix(result)
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)

    @swagger.operation(
        responseClass=responses.Deployment,
        nickname="createDeployment",
        notes="Created a new deployment of the given blueprint.",
        parameters=[{'name': 'blueprint_id',
                     'description': 'Blueprint ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'inputs',
                     'description': 'Deployment inputs',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}],
        consumes=[
            "application/json"
        ]
    )
    def put(self, deployment_id):
        logger.debug("Entering Deployments.put method.")
        blueprint_id = request.json.get('blueprint_id')
        inputs = json.loads(request.json.get('inputs'))
        if self.can_do_deployment():
            try:
                logger.info("Updating quota for Org-ID %s.",
                            g.org_id)
                self.update_quota(+1)
                logger.info("Checking if blueprint %s exists.",
                            blueprint_id)
                g.cc.blueprints.get(util.add_org_prefix(blueprint_id))
                deployment = g.cc.deployments.create(
                    util.add_org_prefix(blueprint_id),
                    util.add_org_prefix(deployment_id),
                    inputs=inputs)
                logger.debug("Done. Exiting Deployments.put method.")
                return util.remove_org_prefix(deployment)
            except(exceptions.CloudifyClientError,
                   exceptions.MissingRequiredDeploymentInputError,
                   exceptions.UnknownDeploymentInputError) as e:
                logger.error(str(e))
                logger.error("Decreasing quota.")
                self.update_quota(-1)
                return util.make_response_from_exception(e)
