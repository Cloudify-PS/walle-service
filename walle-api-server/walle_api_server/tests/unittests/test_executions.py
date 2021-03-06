# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock
import json

from walle_api_server.resources import executions
from walle_api_server.common import service_limit
from walle_api_server.tests.fakes.fake_objects import ListResponse


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.executions = executions.Executions()
        self.executions_id = executions.ExecutionsId()
        self.test_id = "some_id"

    def setup_context(self):
        flask.g.tenant_id = self.test_id
        flask.g.token = "secret token"
        flask.g.org_url = "org_url"
        flask.g.cc = mock.MagicMock()
        flask.g.rights = [service_limit.USER_RIGHT]

    def prefix_deployment(self, deployment):
        return "{}_{}".format(self.test_id, deployment)

    def test_list_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.list = (lambda deployment_id, _include,
                                          status:
                                          ListResponse(
                                              [{'deployment_id': deployment_id,
                                                'workflow_id': 'walleinstall'},
                                               {'deployment_id': 'test',
                                                'workflow_id': 'walleinstal'}]))
            deployment = '123'
            with self.app.test_request_context('/executions?deployment_id={}'.
                                               format(deployment)):
                deployment_list = self.executions.get()
                self.assertTrue(len(deployment_list), 1)
                self.assertEqual(deployment_list['items'][0]['deployment_id'],
                                 deployment)

    def test_start_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.start = lambda a, b, c, \
                d, e: {'deployment_id': a,
                       'workflow_id': b,
                       'parameters': c,
                       'allow_custom_parameters': d,
                       'force': e}
            deployment = '1'
            workflow = "install"
            data = {
                'deployment_id': deployment,
                'workflow_id': workflow,
                'parameters': None,
                'allow_custom_parameters': 'false',
                'force': 'false'}
            with self.app.test_request_context('/executions', method="POST",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                deployment = self.executions.post()
                self.assertEqual(deployment, data)

    def test_cancel_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.get = lambda _: {
                'workflow_id': 'walleinstall'
            }
            flask.g.cc.executions.cancel = lambda _, a: {
                'force': a, 'workflow_id': 'walleinstall'
            }
            execution = 1
            force = 'false'
            data = {'force': force}
            with self.app.test_request_context('/executions/{}'.
                                               format(execution),
                                               method="POST",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                execution = self.executions_id.post()
                self.assertEqual(execution, {
                    'workflow_id': 'install', 'force': False
                })
