import os
import tempfile
import tarfile

from flask.ext import restful
from flask import request, abort, g

from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient

def decode(input_stream, buffer_size=8192):
    while True:
        print 'about to read'
        read_buffer = input_stream.read(buffer_size)
        print len(read_buffer)
        yield read_buffer
        if len(read_buffer) < buffer_size:
            return


#curl http://127.0.0.1:8080/blueprints --header 'x-vcloud-authorization: '$session_token --header 'x-vcloud-org-url: '$org_url --header 'x-vcloud-version: 5.6'|jq ".[].id"
            
#upload blueprint
#curl -v -i -X PUT http://127.0.0.1:8080/blueprints/bp1 --header 'x-vcloud-authorization: '$session_token --header 'x-vcloud-org-url: '$org_url --header 'x-vcloud-version: 5.6' --data-binary @hellovcloud.tar.gz --header "Content-Type: application/octect-stream"

class Blueprints(restful.Resource):
    def get(self, blueprint_id=None):
        blueprints = g.cc.blueprints.list()
        result = []
        for blueprint in blueprints:
            if blueprint.id.startswith(g.org_id+'_'): result.append(blueprint)
        return result

    def put(self, blueprint_id):
        file_server_root = '.' #config.instance().file_server_root
        archive_target_path = tempfile.mktemp(dir=file_server_root)
        try:
            modified_id = g.org_id+'_'+blueprint_id
            # self._save_file_locally(archive_target_path+'.tar.gz')
            archive_file_name = modified_id+'.tar.gz'
            self._save_file_locally(archive_file_name)
            
            tfile = tarfile.open(archive_file_name, 'r:gz')
            tfile.extractall('.')
            
            blueprint = g.cc.blueprints.upload('hellovcloud/blueprint.yaml', modified_id)
            return blueprint, 201
        finally:
            if os.path.exists(archive_target_path):
                os.remove(archive_target_path)
                
                
    @staticmethod
    def _save_file_locally(archive_file_name):
        if not request.data:
            raise manager_exceptions.BadParametersError(
                'Missing blueprint archive in request body')
        uploaded_file_data = request.data
        with open(archive_file_name, 'w') as f:
            f.write(uploaded_file_data)