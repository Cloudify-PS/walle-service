import os
import tempfile
import tarfile
import shutil

from flask.ext import restful
from flask import request, abort, g

from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient

# Chunked is handled by gunicorn
def decode(input_stream, buffer_size=8192):
    while True:
        read_buffer = input_stream.read(buffer_size)
        yield read_buffer
        if len(read_buffer) < buffer_size:
            return

#todo: download blueprint
class Blueprints(restful.Resource):

    def get(self, blueprint_id=None):
        if blueprint_id is not None:
            if not blueprint_id.startswith(g.org_id+'_'): 
                return None
            return g.cc.blueprints.get(blueprint_id)
        else:
            blueprints = g.cc.blueprints.list()
            result = []
            for blueprint in blueprints:
                if blueprint.id.startswith(g.org_id+'_'): result.append(blueprint)
            return result

    def put(self, blueprint_id):
        tempdir = tempfile.mkdtemp()
        try:
            modified_id = g.org_id+'_'+blueprint_id
            archive_file_name = tempdir + '/' + modified_id+'.tar.gz'
            self._save_file_locally(archive_file_name)
            
            tfile = tarfile.open(archive_file_name, 'r:gz')
            tfile.extractall(tempdir)
            files = os.listdir(tempdir)
            directory = None
            for file in files:
                if not file.endswith('.tar.gz'):
                    directory = file
                    break
            
            blueprint = g.cc.blueprints.upload(tempdir + '/' + directory + '/blueprint.yaml', modified_id)
            return blueprint, 201
        finally:
            shutil.rmtree(tempdir)
                
    def delete(self, blueprint_id):
        assert blueprint_id
        blueprint = g.cc.blueprints.delete(blueprint_id)
        return blueprint
                
    @staticmethod
    def _save_file_locally(archive_file_name):
        
        if 'Transfer-Encoding' in request.headers:
            with open(archive_file_name, 'w') as f:
                for buffered_chunked in decode(request.input_stream):
                    f.write(buffered_chunked)
        else:
            if not request.data:
                raise manager_exceptions.BadParametersError(
                    'Missing application archive in request body or '
                    '"blueprint_archive_url" in query parameters')
            uploaded_file_data = request.data
            with open(archive_file_name, 'w') as f:
                f.write(uploaded_file_data)        
