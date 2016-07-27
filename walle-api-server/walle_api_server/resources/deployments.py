# Copyright (c) 2015 VMware. All rights reserved

from cloudify_rest_client import exceptions

from flask.ext import restful
from flask import g, request
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

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
            deployments = g.proxy.get(request)
            util.filter_response(deployments, "id")
            logger.debug("Done. Exiting Deployments.get method.")
            return deployments
        except exceptions.CloudifyClientError as e:
            return util.make_response_from_exception(e)


class DeploymentsId(restful.Resource):

    def update_quota(self, increment_or_decrement):
        logger.debug("Entering Deployments.update_qouta method.")
        current_account_limits = service_limit.get_tenant_limit(
            g.current_tenant.id, service_limit.DEPLOYMENT_LIMIT
        )
        if current_account_limits:
            current_account_limits = current_account_limits.update(
                value=(
                    current_account_limits.value +
                    increment_or_decrement))
            current_account_limits.save()
        logger.debug("Done. Exiting Deployments.update_qouta method.")

    def can_do_deployment(self):
        logger.debug(
            "Entering Deployments.can_do_deployment method.")
        current_account_limits = service_limit.get_tenant_limit(
            g.current_tenant.id, service_limit.DEPLOYMENT_LIMIT
        )
        if current_account_limits:
            if current_account_limits.hard == -1 or (
               current_account_limits.hard >
               current_account_limits.value):
                # When deployment limit set to -1 users
                # can deploy infinite number of blueprints.
                # Or deployment limits still greater than number of deployments
                logger.info(
                    "Success. Deployment can be done for Org-ID:%s .",
                    g.tenant_id
                )
                logger.debug(
                    "Done. Exiting Deployments.can_do_deployment method."
                )
                return True

        logger.debug("Deployment quota exceeded for Org-ID:%s.",
                     g.tenant_id)
        raise exceptions.CloudifyClientError(
            "Deployment quota exceeded.", status_code=403
        )

    @swagger.operation(
        responseClass=responses.Deployment,
        nickname="getById",
        notes="Returns a deployment by its ID.",
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def get(self, deployment_id=None):
        logger.debug("Entering DeploymentsId.get method.")
        try:
            logger.info("Seeking for deplyment %s .",
                        deployment_id)
            _include = request.args.get("_include", "").split(",")
            result = g.cc.deployments.get(util.add_org_prefix(deployment_id),
                                          _include=_include)
            logger.info("Cloudify deployment get: {0}.".format(str(result)))
            filtere_workflows = []
            for _workflow in result['workflows']:
                if not _workflow['name'].startswith('walle'):
                    if _workflow['parameters'].get('session_token'):
                        del _workflow['parameters']['session_token']
                    if _workflow['parameters'].get('org_url'):
                        del _workflow['parameters']['org_url']
                    if _workflow['parameters'].get('keystore_url'):
                        del _workflow['parameters']['keystore_url']
                    if _workflow['parameters'].get('region'):
                        del _workflow['parameters']['region']
                    filtere_workflows.append(_workflow)

            result['workflows'] = filtere_workflows
            logger.debug("Done. Exiting DeploymentsId.get method.")
            return util.remove_org_prefix(result)
        except exceptions.CloudifyClientError as e:
            logger.exception(str(e))
            logger.debug("Done. Exiting DeploymentsId.get method.")
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
                     'paramType': 'path'},
                    {'name': 'ignore_live_nodes',
                     'description': 'Ignore Live nodes',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'boolean',
                     'paramType': 'query'}]
    )
    def delete(self, deployment_id=None):
        logger.debug("Entering Deployments.delete method.")
        try:
            parser = restful.reqparse.RequestParser()
            parser.add_argument('ignore_live_nodes',
                                type=bool, default=False,
                                help='ignore live nodes')
            arguments = parser.parse_args()
            ignore_live_nodes = arguments['ignore_live_nodes']
            cfy_dp_id = util.add_org_prefix(deployment_id)
            # necessary to validate that deployment exists
            logger.info("Checking if deployment %s exists.",
                        deployment_id)
            self.get(deployment_id=deployment_id)
            logger.info("Deleting deployment %s.", deployment_id)
            result = g.cc.deployments.delete(cfy_dp_id, ignore_live_nodes)
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
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'blueprint_id',
                     'description': 'Blueprint ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'inputs',
                     'description': 'Deployment inputs',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "blueprint_id": {"type": "string", "minLength": 1},
             "inputs": {"type": ["object", "null"]}
         },
         "required": ["blueprint_id"]}
    )
    def put(self, json, deployment_id=None):
        logger.debug("Entering Deployments.put method.")
        blueprint_id = json['blueprint_id']
        inputs = json.get('inputs')
        try:
            if self.can_do_deployment():
                logger.info("Updating quota for Org-ID %s.",
                            g.tenant_id)
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


class DeploymentOutputs(restful.Resource):

    @swagger.operation(
        responseClass=responses.DeploymentOutputs,
        nickname="output",
        notes="Gets a specific deployment outputs.",
    )
    def get(self, deployment_id):
        logger.debug("Entering DeploymentOutputs.get method.")
        try:
            logger.info("Output of the deployment.")
            output = g.cc.deployments.outputs.get(
                util.add_org_prefix(deployment_id))
            logger.debug("Done. Exiting DeploymentOutputs.get method.")
            return util.remove_org_prefix(output)
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)


class DeploymentsUpdates(restful.Resource):

    def get(self):
        logger.debug("Entering DeploymentsUpdates.get method.")
        result = g.proxy.get(request)
        logger.debug("Done. Exiting Events.get method.")
        return util.remove_org_prefix(result)
