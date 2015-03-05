from flask import Flask
from flask.ext import restful
from flask import request, abort, g

from pyvcloud.vcloudsession import VCS
from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient

from score_api_server.resources.blueprints import Blueprints
from score_api_server.resources.deployments import Deployments
from score_api_server.resources.executions import Executions

app = Flask(__name__)
api = restful.Api(app)

allowed_orgs = ['37d9e482-a5d1-4811-b466-c4d1e2f67f2c', #on demand
                'edaaea15-5ad9-40ca-af23-1e146640eba5', #app services
                '0ea8e6de-8dc0-4b2d-83a0-629544be5465'] #vmop

#note: assume vcs.organization.id is unique across the service
@app.before_request
def check_authorization():
    vcloud_token = request.headers.get('x-vcloud-authorization')
    vcloud_org_url = request.headers.get('x-vcloud-org-url')
    vcloud_version = request.headers.get('x-vcloud-version')
    if vcloud_token is None or vcloud_org_url is None or vcloud_version is None:
        abort(401)
    vcs = VCS(vcloud_org_url, None, None, None, vcloud_org_url, vcloud_org_url, version=vcloud_version)
    result = vcs.login(token=vcloud_token)
    if result:
        g.org_id = vcs.organization.id[vcs.organization.id.rfind(':')+1:]
        if g.org_id not in allowed_orgs:
            abort(401)
    else:
        abort(vcs.response.status_code)
        
@app.before_request
def connect_to_cloudify():
    g.cc = CloudifyClient(host='192.240.158.81', port=5580)
    # g.cc = CloudifyClient(host='192.168.109.5', port=80)
        
api.add_resource(Blueprints, '/blueprints', '/blueprints/<string:blueprint_id>')
api.add_resource(Deployments, '/deployments', '/deployments/<string:deployment_id>')
api.add_resource(Executions, '/executions', '/executions/<string:execution_id>')

if __name__ == '__main__':
    app.run()
    