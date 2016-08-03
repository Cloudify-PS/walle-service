# Copyright (c) 2015 VMware. All rights reserved

from flask import g
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_restful_swagger import swagger

from cloudify_rest_client import exceptions

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class Executions(restful.Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Execution.__name__),
        nickname="list",
        notes="Returns a list of executions for the optionally provided "
              "deployment id.",
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment ID',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': None,
                     'paramType': 'query'}]
    )
    def get(self):
        logger.debug("Entering Execution.get method.")
        restricted = service_limit.cant_see_blueprints()
        if restricted:
            return restricted
        parser = reqparse.RequestParser()
        parser.add_argument('deployment_id', type=str, default='',
                            help='Deployment ID')
        parser.add_argument('status', action='append')
        parser.add_argument('_include', type=str, default='')
        parsed = parser.parse_args()
        try:
            _include = parsed['_include'].split(',')
            deployment_id = util.add_prefix_to_deployment(
                parsed['deployment_id'])
            logger.info("Listing executions for deployment %s .",
                        deployment_id)
            executions = g.cc.executions.list(deployment_id,
                                              _include=_include,
                                              status=parsed['status'])
            logger.info("Cloudify executions list: {0}.".format(
                str(executions)))
            executions.items = [util.remove_org_prefix(e) for e in executions
                                if g.tenant_id in e.get('deployment_id', "")]
            for ex in executions.items:
                if ex['workflow_id'].startswith('walle'):
                    ex['workflow_id'] = ex['workflow_id'][5:]

            return util.list_response_to_dict(executions)
        except exceptions.CloudifyClientError as e:
            return util.make_response_from_exception(e)

    @swagger.operation(
        responseClass=responses.Execution,
        nickname="startExecution",
        notes="Started a new execution of the given deployment and "
              "workflow ids.",
        parameters=[{'name': 'deployment_id',
                     'description': 'Deployment id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'workflow_id',
                     'description': 'Workflow id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'parameters',
                     'description': 'Parameters for execution',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'object',
                     'paramType': 'body'},
                    {'name': 'allow_custom_parameters',
                     'description': 'Custom parameters',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'boolean',
                     'paramType': 'body'},
                    {'name': 'force',
                     'description': 'Execution start force',
                     'required': False,
                     'allowMultiple': False,
                     'defaultValue': False,
                     'dataType': 'boolean',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "deployment_id": {"type": "string", "minLength": 1},
             "workflow_id": {"type": "string", "minLength": 1},
             "parameters": {"type": ["object", "null"]},
             "allow_custom_parameters": {"type": "string"},
             "force": {"type": "string"},
         },
         "required": ["deployment_id", "workflow_id"]}
    )
    def post(self, json):
        logger.debug("Entering Execution.post method.")
        restricted = service_limit.cant_see_blueprints()
        if restricted:
            return restricted
        try:
            def _walle_tosca_prefix():
                deployment_obj = g.cc.deployments.get(deployment_id)
                # check plugin version
                blueprint_id = deployment_obj['blueprint_id']
                blueprint_obj = g.cc.blueprints.get(blueprint_id)
                plan_dict = blueprint_obj['plan']
                deploy_dict = plan_dict['deployment_plugins_to_install']
                workflow_dict = plan_dict['workflow_plugins_to_install']
                for plugin in workflow_dict + deploy_dict:
                    # openstack and vcloud have support of 'walle' prefix
                    # so strictly use such prefix
                    if plugin['name'] in ('vcloud', 'openstack'):
                        return "walle"
                return ""

            deployment_id = util.add_org_prefix(json['deployment_id'])
            workflow_id = json['workflow_id']
            parameters = json.get('parameters')
            if not parameters:
                parameters = {}
            parameters['session_token'] = g.token
            if hasattr(g, 'org_url'):
                parameters['org_url'] = g.org_url
            if hasattr(g, 'keystore_url'):
                parameters['keystore_url'] = g.keystore_url
            if hasattr(g, 'openstack_region'):
                parameters['region'] = g.openstack_region
            if hasattr(g, 'tenant_name'):
                parameters['tenant_name'] = g.tenant_name
            allow_custom_parameters = True
            force = json.get('force', "False")
            force = "true" == force.lower()
            logger.info("Looking for deployment %s .", deployment_id)

            logger.info("Staring workflow %s for deployment %s.",
                        workflow_id, deployment_id)
            result = g.cc.executions.start(
                deployment_id, _walle_tosca_prefix() + workflow_id,
                parameters, allow_custom_parameters, force
            )
            logger.debug("Done. Exiting Executions.post method.")
            # cleanup result
            result['workflow_id'] = workflow_id
            result['parameters'] = json.get('parameters')
            result['allow_custom_parameters'] = json.get(
                'allow_custom_parameters'
            )
            return util.remove_org_prefix(result)
        except (exceptions.CloudifyClientError,
                exceptions.DeploymentEnvironmentCreationInProgressError,
                exceptions.DeploymentEnvironmentCreationPendingError) as e:
            # should we wait for deployment environment creation workflow?
            logger.error(str(e))
            response_code = (
                403 if isinstance(e, (
                    exceptions.DeploymentEnvironmentCreationInProgressError,
                    exceptions.DeploymentEnvironmentCreationPendingError))
                else e.status_code)
            return util.make_response_from_exception(e, response_code)


class ExecutionsId(restful.Resource):

    @swagger.operation(
        responseClass=responses.Execution,
        nickname="getById",
        notes="Returns the execution state by its id.",
        parameters=[{'name': 'execution_id',
                     'description': 'Execution ID',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': None,
                     'paramType': 'path'}]
    )
    def get(self, execution_id=None):
        logger.debug("Entering ExecutionsId.get method.")
        restricted = service_limit.cant_see_blueprints()
        if restricted:
            return restricted
        try:
            logger.info(
                "Seeking for executions by execution %s.",
                execution_id)
            result = g.cc.executions.get(execution_id)
            if (result['workflow_id'] and
                    result['workflow_id'].startswith("walle")):
                result['workflow_id'] = result['workflow_id'][5:]
            logger.debug("Done. Exiting ExecutionsId.get method.")
            return util.remove_org_prefix(result)
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)

    @swagger.operation(
        responseClass=responses.Execution,
        nickname="modify_state",
        notes="Modifies a running execution state (currently, only cancel"
              " and force-cancel are supported)",
        parameters=[{'name': 'force',
                     'description': 'if flag set to "true"'
                     ' "force-cancel" will be used',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'boolean',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "force": {"type": "string"}}}
    )
    def post(self, json, execution_id=None):
        logger.debug("Entering Execution.put method.")
        restricted = service_limit.cant_see_blueprints()
        if restricted:
            return restricted
        try:
            force = json.get('force', "False")
            force = "true" == force.lower()
            self.get(execution_id=execution_id)
            result = g.cc.executions.cancel(execution_id, force)
            if (result['workflow_id'] and
                    result['workflow_id'].startswith("walle")):
                result['workflow_id'] = result['workflow_id'][5:]
            logger.debug("Done. Exiting Executions.put method.")
            return util.remove_org_prefix(result)
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)
