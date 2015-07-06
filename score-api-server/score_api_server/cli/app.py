# Copyright (c) 2015 VMware. All rights reserved

from flask import Flask
from flask.ext import restful
from flask import request, abort, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

from pyvcloud.vcloudsession import VCS
from cloudify_rest_client.client import CloudifyClient

from score_api_server.common import cfg
from score_api_server.common import org_limit
from score_api_server.resources.blueprints import Blueprints
from score_api_server.resources.deployments import Deployments
from score_api_server.resources.executions import Executions
from score_api_server.resources.events import Events
from score_api_server.resources.status import Status

app = Flask(__name__)
api = restful.Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CONF = cfg.CONF
app.config['SQLALCHEMY_DATABASE_URI'] = CONF.server.db_uri


# note: assume vcs.organization.id is unique across the service
@app.before_request
def check_authorization():
    vcloud_token = request.headers.get('x-vcloud-authorization')
    vcloud_org_url = request.headers.get('x-vcloud-org-url')
    vcloud_version = request.headers.get('x-vcloud-version')
    if (vcloud_token is None or vcloud_org_url
       is None or vcloud_version is None):
        abort(401)
    vcs = VCS(vcloud_org_url, None, None, None,
              vcloud_org_url, vcloud_org_url,
              version=vcloud_version)
    result = vcs.login(token=vcloud_token)
    if result:
        g.org_id = vcs.organization.id[vcs.organization.id.rfind(':') + 1:]
        limit = org_limit.get_current_limit()
        if not limit:
            abort(401)
    else:
        abort(vcs.response.status_code)


@app.before_request
def connect_to_cloudify():
    g.cc = CloudifyClient(host=CONF.cloudify.host,
                          port=CONF.cloudify.port)

api.add_resource(Blueprints, '/blueprints',
                 '/blueprints/<string:blueprint_id>')
api.add_resource(Deployments, '/deployments',
                 '/deployments/<string:deployment_id>')
api.add_resource(Executions, '/executions')
api.add_resource(Events, '/events')
api.add_resource(Status, '/status')


def main():
    host, port, workers = (CONF.server.host,
                           CONF.server.port,
                           CONF.server.workers)
    try:
        app.run(
            host=host,
            port=port,
            processes=workers
        )
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
