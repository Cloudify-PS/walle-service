from flask import Flask
from flask.ext import restful
from flask import request, abort, g

from pyvcloud.vcloudsession import VCS
from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient

from score_api_server.resources.blueprints import Blueprints

app = Flask(__name__)
api = restful.Api(app)

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
    else:
        abort(vcs.response.status_code)
        
@app.before_request
def connect_to_cloudify():
    g.cc = CloudifyClient(host='192.240.158.81', port=580)
        
api.add_resource(Blueprints, '/blueprints', '/blueprints/<string:blueprint_id>')

# api.add_resource(File, '/blueprints/<path:fname>')

 