# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock
import json

from score_api_server.resources import executions


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.executions = executions.Executions()
        self.executions_id = executions.ExecutionsId()
        self.test_id = "some_id"

    def setup_context(self):
        flask.g.org_id = self.test_id
        flask.g.cc = mock.MagicMock()

    def prefix_deployment(self, deployment):
        return "{}_{}".format(self.test_id, deployment)

    def test_list_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.list = (lambda deployment_id:
                                          [{'deployment_id': deployment_id},
                                           {'deployment_id': 'test'}])
            deployment = '123'
            with self.app.test_request_context('/executions?deployment_id={}'.
                                               format(deployment)):
                deployment_list = self.executions.get()
                self.assertTrue(len(deployment_list), 1)
                self.assertEqual(deployment_list[0]['deployment_id'],
                                 deployment)

    def test_start_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.start = lambda a, b: {'deployment_id': a,
                                                        'workflow_id': b}
            deployment = '1'
            workflow = "install"
            data = {
                'deployment_id': deployment,
                'workflow_id': workflow}
            with self.app.test_request_context('/executions', method="POST",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                deployment = self.executions.post()
                self.assertEqual(deployment, data)

    def test_cancel_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.get = lambda _: {}
            flask.g.cc.executions.cancel = lambda a, b: {'execution_id': a,
                                                         'force': b}
            execution = 1
            force = False
            data = {
                'execution_id': execution,
                'force': force}
            with self.app.test_request_context('/executions', method="PUT",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                execution = self.executions_id.put()
                self.assertEqual(execution, data)
