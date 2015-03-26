import os
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

allowed_orgs = [
                '37d9e482-a5d1-4811-b466-c4d1e2f67f2c', #on demand
                'edaaea15-5ad9-40ca-af23-1e146640eba5', #app services
                '0ea8e6de-8dc0-4b2d-83a0-629544be5465', #vmop
                'fdb1f868-9a16-4153-aaf4-25389fc18d03', #cert23
                '72cb93a9-ab17-497c-96f6-5d278d908f89', #Timo
		'eaa53571-0a98-4976-aaa1-678ac5e8bc6e', #Udi
		'61209cc8-c4ea-467d-bc07-d3fa74929ae4', #Bob
		'dd3f9a9a-5894-4bac-8fde-f55c61a000c4', #Greg
		'224b99a3-23f4-4f0a-aa3f-69f405bcf2ae', #Xiaoyun
		'24d27926-2dcd-42d6-81b9-456e50de25ec', #Todd
                '64c7bf06-3dd6-4d82-b25a-3edf58ff9d87'  #prod
                ]
                
print 'connecting to cloudify manager server at', os.environ['CFY_HOST'], os.environ['CFY_PORT']
                

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
    g.cc = CloudifyClient(host=os.environ['CFY_HOST'], port=int(os.environ['CFY_PORT']))
    # g.cc = CloudifyClient(host='192.240.158.81', port=5580)
    # g.cc = CloudifyClient(host='192.168.109.5', port=80)
        
api.add_resource(Blueprints, '/blueprints', '/blueprints/<string:blueprint_id>')
api.add_resource(Deployments, '/deployments', '/deployments/<string:deployment_id>')
api.add_resource(Executions, '/executions', '/executions/<string:execution_id>')

if __name__ == '__main__':
    app.run()
    
