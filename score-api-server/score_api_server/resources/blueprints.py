# Copyright (c) 2015 VMware. All rights reserved

import os
import yaml
import tempfile
import tarfile
import shutil
import os.path

from flask.ext import restful
from flask import request, g, make_response
from flask_restful_swagger import swagger

from cloudify_rest_client import exceptions
from dsl_parser import parser
from dsl_parser import exceptions as dsl_exceptions

from score_api_server.common import util
from score_api_server.resources import responses


# Chunk is handled by gunicorn
def decode(input_stream, buffer_size=8192):
    while True:
        read_buffer = input_stream.read(buffer_size)
        yield read_buffer
        if len(read_buffer) < buffer_size:
            return

logger = util.setup_logging(__name__)


class Blueprints(restful.Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.BlueprintState.__name__),
        nickname="list",
        notes="Returns a list of uploaded blueprints."
    )
    def get(self):
        logger.debug("Entering Blueprints.get method.")
        try:
            logger.info("Listing all blueprints.")
            blueprints = g.cc.blueprints.list()
            result = []
            for blueprint in blueprints:
                if blueprint.id.startswith(g.org_id + '_'):
                    result.append(util.remove_org_prefix(blueprint))
            logger.debug("Done. Exiting Blueprints.get method.")
            return result
        except exceptions.CloudifyClientError as e:
            logger.exception(str(e))
            return util.make_response_from_exception(e)


# TODO(???): download blueprint
class BlueprintsId(restful.Resource):

    def filter_validation_exception(self, e):
        if str(e).startswith("Failed on import"):
            root_message = "Invalid types import - {0}. ".format(
                e.failed_import)
            if not e.failed_import.startswith("http"):
                return (
                    root_message +
                    "Unable to access types definition file."
                    "Please note that relative paths is not allowed.")
            else:
                return (
                    root_message +
                    "Unable to access remote types definition file."
                )
        else:
            return e.message

    def validation_groups_policies(self, blueprint_plan):
        logger.info("Running groups, policy types and policy "
                    "triggers validation.")
        groups, p_types, p_triggers = (blueprint_plan['groups'],
                                       blueprint_plan['policy_types'],
                                       blueprint_plan['policy_triggers'])
        if groups or p_triggers or p_types:
            raise Exception(
                "Blueprint is invalid due to presence of groups, "
                "policy types and policy triggers. Groups: {0}."
                " Policy types: {1}. Policy triggers: {2}.".format(
                    groups, p_types, p_triggers)
            )

    def validate_imports(self, blueprint_path):
        with open(blueprint_path) as bp:
            imports = yaml.load(bp.read())['imports']
            for _import in imports:
                if _import.startswith("file:"):
                    raise exceptions.CloudifyClientError(
                        "Invalid types import - {0}".format(
                            _import)
                    )

    def validate_plugins(self, blueprint_plan):
        logger.debug("Entering Blueprints.validate_plugins method.")
        logger.info("Running blueprint plugins validation checks.")
        from score_api_server.db import models

        def _validate_plugins_with_type(plugins, _type):
            for plugin in plugins:
                name, source, install_arguments = (plugin['name'],
                                                   plugin['source'],
                                                   plugin['install_arguments'])

                if not models.ApprovedPlugins.find_by(
                        name=name,
                        source=source if source else '',
                        plugin_type=_type) or install_arguments:

                    raise exceptions.CloudifyClientError(
                        "Forbidden. Blueprint plugin {0} with source {1} "
                        "is not approved".format(name, source))

        deployment_plugins = blueprint_plan['deployment_plugins_to_install']
        workflow_plugins = blueprint_plan['workflow_plugins_to_install']

        _validate_plugins_with_type(deployment_plugins, "deployment_plugins")
        _validate_plugins_with_type(workflow_plugins, "workflow_plugins")

        logger.info("Validation finished succesfuly.")
        logger.debug("Exiting Blueprints.validate_plugins method.")

    def validate_blueprint_on_security_breaches(
            self, bluerpint_name, blueprint_directory):
        logger.debug(
            "Entering BlueprintsId.validate_blueprint_"
            "on_security_breaches method.")
        logger.info("Staring validating checks for blueprint: {0}. "
                    "Blueprint directory: {1}."
                    .format(bluerpint_name, blueprint_directory))
        blueprint_path = os.path.join(blueprint_directory,
                                      bluerpint_name)

        try:
            logger.info("Running basic blueprints validation.")

            self.validate_imports(blueprint_path)

            blueprint_plan = parser.parse_from_path(blueprint_path)
            logger.debug("Blueprint plan: %s" % str(blueprint_plan))

            self.validation_groups_policies(blueprint_plan)

            logger.info("Running deployment/workflow plugins validation.")
            self.validate_plugins(blueprint_plan)

            logger.info("Success on basic blueprints validation.")

            logger.debug(
                "Done. Exiting BlueprintsId.validate_blueprint_"
                "on_security_breaches method.")
        except (Exception,
                dsl_exceptions.DSLParsingException,
                dsl_exceptions.MissingRequiredInputError,
                dsl_exceptions.UnknownInputError,
                dsl_exceptions.FunctionEvaluationError,
                dsl_exceptions.DSLParsingLogicException,
                dsl_exceptions.DSLParsingFormatException) as e:
            logger.exception(str(e))
            logger.debug(
                "Done. Exiting BlueprintsId.validate_blueprint_"
                "on_security_breaches method.")
            raise exceptions.CloudifyClientError(
                "{0}. Blueprint: {1}.".format(
                    self.filter_validation_exception(e),
                    bluerpint_name),
                status_code=403)

        logger.debug(
            "Done. Exiting BlueprintsId.validate_blueprint_"
            "on_security_breaches method.")

    @swagger.operation(
        responseClass=responses.BlueprintState,
        nickname="getById",
        notes="Returns a blueprint by its ID.",
        parameters=[{'name': 'blueprint_id',
                     'description': 'Blueprint ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}]
    )
    def get(self, blueprint_id=None):
        logger.debug("Entering BlueprintsId.get method.")
        try:
            logger.info("Seeking for blueprint: %s.",
                        blueprint_id)
            return g.cc.blueprints.get(
                util.add_org_prefix(blueprint_id))
        except exceptions.CloudifyClientError as e:
            logger.exception(str(e))
            return util.make_response_from_exception(e)

    @swagger.operation(
        responseClass=responses.BlueprintState,
        nickname="upload",
        notes="Uploads the tar.gz archive of the folder which contains "
              "blueprint file. "
              "Request body must be contains only gzipped archive.",
        parameters=[{'name': 'blueprint_id',
                     'description': 'Blueprint ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'application_file_name',
                     'description': 'Name of blueprint tar gzipped file',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}],
        consumes=[
            "application/octet-stream"
        ]
    )
    def put(self, blueprint_id):
        try:
            logger.debug("Entering Blueprints.put method.")
            tempdir = tempfile.mkdtemp()
            archive_file_name = os.path.join(
                tempdir,
                util.add_org_prefix(blueprint_id) + '.tar.gz')
            logger.info("Saving blueprint files locally.")
            self._save_file_locally(archive_file_name)
            logger.debug("Extracting archive.")
            with tarfile.open(archive_file_name, 'r:gz') as tfile:
                tfile.extractall(tempdir)
            files = os.listdir(tempdir)
            directory = None
            for file in files:
                if not file.endswith('.tar.gz'):
                    directory = file
                    break
            self.validate_blueprint_on_security_breaches(
                request.args['application_file_name'],
                os.path.join(tempdir, directory))

            logger.info("Uploading blueprint to Cloudify manager.")
            blueprint = g.cc.blueprints.upload(
                os.path.join(tempdir, directory,
                             request.args['application_file_name']),
                util.add_org_prefix(blueprint_id))
            logger.debug("Done. Exiting Blueprints.put method.")
            shutil.rmtree(tempdir, True)
            return util.remove_org_prefix(blueprint)
        except (Exception, exceptions.CloudifyClientError) as e:
            logger.exception(str(e))
            status = (400 if not isinstance(e, exceptions.CloudifyClientError)
                      else e.status_code)
            logger.debug("Done. Error. Exiting Blueprints.put method.")
            shutil.rmtree(tempdir, True)
            return util.make_response_from_exception(e, status)

    @swagger.operation(
        responseClass=responses.BlueprintState,
        nickname="deleteById",
        notes="Deletes a blueprint by its ID.",
        parameters=[{'name': 'blueprint_id',
                     'description': 'Blueprint ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'}]
    )
    def delete(self, blueprint_id):
        logger.debug("Entering Blueprints.delete method.")
        try:
            logger.info("Checking if blueprint exists.")
            self.get(blueprint_id)
            logger.info("Deleting blueprint from manager.")
            blueprint = g.cc.blueprints.delete(
                util.add_org_prefix(blueprint_id))
            logger.debug("Done. Exiting Blueprints.delete method.")
            return blueprint
        except exceptions.CloudifyClientError as e:
            logger.exception(str(e))
            return util.make_response_from_exception(e)

    @staticmethod
    def _save_file_locally(archive_file_name):
        logger.debug("Entering Blueprints._save_file_locally method.")
        if 'Transfer-Encoding' in request.headers:
            with open(archive_file_name, 'wb') as f:
                for buffered_chunked in decode(request.input_stream):
                    f.write(buffered_chunked)
        else:
            if not request.data:
                return make_response(
                    'Missing application archive in request body or '
                    '"blueprint_archive_url" in query parameters', 400)
            uploaded_file_data = request.data
            with open(archive_file_name, 'wb') as f:
                f.write(uploaded_file_data)
        logger.debug("Done. Exiting Blueprints._save_file_locally method.")
