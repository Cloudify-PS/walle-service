# Copyright (c) 2015 VMware. All rights reserved

import os
import tempfile
import tarfile
import shutil
import os.path

from flask.ext import restful
from flask import request, g, make_response
from flask_restful_swagger import swagger

from cloudify_rest_client import exceptions

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
            return make_response(str(e), e.status_code)


# TODO(???): download blueprint
class BlueprintsId(restful.Resource):

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
            logger.error(str(e))
            return make_response(str(e), e.status_code)

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
                     'paramType': 'body'},
                    {'name': 'application_file_name',
                     'description': 'Name of blueprint tar gzipped file',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=[
            "application/octet-stream"
        ]
    )
    def put(self, blueprint_id):
        logger.debug("Entering Blueprints.put method.")
        tempdir = tempfile.mkdtemp()
        try:
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
            logger.info("Uploading blueprint to Cloudify manager.")
            blueprint = g.cc.blueprints.upload(
                os.path.join(tempdir, directory,
                             request.args['application_file_name']),
                util.add_org_prefix(blueprint_id))
            logger.debug("Done. Exiting Blueprints.put method.")
            return util.remove_org_prefix(blueprint)
        except (Exception, exceptions.CloudifyClientError) as e:
            logger.error(str(e))
            return make_response(str(e), 400 if not isinstance(
                e, exceptions.CloudifyClientError) else e.status_code)
        finally:
            shutil.rmtree(tempdir, True)

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
            logger.error(str(e))
            return make_response(str(e), e.status_code)

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
