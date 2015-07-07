# Copyright (c) 2015 VMware. All rights reserved

import os
import tempfile
import tarfile
import shutil
import os.path

from flask.ext import restful
from flask import request, g, make_response
from cloudify_rest_client import exceptions

from score_api_server.common import util


# Chunk is handled by gunicorn
def decode(input_stream, buffer_size=8192):
    while True:
        read_buffer = input_stream.read(buffer_size)
        yield read_buffer
        if len(read_buffer) < buffer_size:
            return


# TODO(???): download blueprint
class Blueprints(restful.Resource):

    def get(self, blueprint_id=None):
        try:
            if blueprint_id is not None:
                return g.cc.blueprints.get(
                    util.add_org_prefix(blueprint_id)), 200
            else:
                blueprints = g.cc.blueprints.list()
                result = []
                for blueprint in blueprints:
                    if blueprint.id.startswith(g.org_id + '_'):
                        result.append(util.remove_org_prefix(blueprint))
                return result, 200
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)

    def put(self, blueprint_id):
        tempdir = tempfile.mkdtemp()
        try:
            archive_file_name = os.path.join(
                tempdir,
                util.add_org_prefix(blueprint_id) + '.tar.gz')
            self._save_file_locally(archive_file_name)
            with tarfile.open(archive_file_name, 'r:gz') as tfile:
                tfile.extractall(tempdir)
            files = os.listdir(tempdir)
            directory = None
            for file in files:
                if not file.endswith('.tar.gz'):
                    directory = file
                    break
            blueprint = g.cc.blueprints.upload(
                os.path.join(tempdir, directory,
                             request.args['application_file_name']),
                util.add_org_prefix(blueprint_id))
            return util.remove_org_prefix(blueprint), 201
        except (Exception, exceptions.CloudifyClientError) as e:
            print(str(e))
            return make_response(str(e), 400 if not isinstance(
                e, exceptions.CloudifyClientError) else e.status_code)
        finally:
            shutil.rmtree(tempdir, True)

    def delete(self, blueprint_id):
        try:
            self.get(blueprint_id)
            blueprint = g.cc.blueprints.delete(
                util.add_org_prefix(blueprint_id))
            return blueprint, 202
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)

    @staticmethod
    def _save_file_locally(archive_file_name):
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
