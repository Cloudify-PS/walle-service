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
        self.test_id = "some_id"

    def setup_context(self):
        flask.g.org_id = self.test_id
        flask.g.cc = mock.MagicMock()

    def prefix_deployment(self, deployment):
        return "{}_{}".format(self.test_id, deployment)

    def test_list_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.list = lambda deployment_id: deployment_id
            deployment = 123
            with self.app.test_request_context('/executions?deployment_id={}'.
                                               format(deployment)):
                deployment_id, status = self.executions.get()
                self.assertEqual(self.prefix_deployment(deployment),
                                 deployment_id)
                self.assertEqual(200, status)

    def test_start_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.start = lambda a, b: (a, b)
            deployment = 1
            workflow = "install"
            data = {
                'deployment_id': deployment,
                'workflow_id': workflow}
            with self.app.test_request_context('/executions', method="POST",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                deployment_tuple, status = self.executions.post()
                self.assertIn(self.prefix_deployment(deployment),
                              deployment_tuple)
                self.assertIn(workflow, deployment_tuple)
                self.assertEqual(202, status)

    def test_cancel_executions(self):
        with self.app.app_context():
            self.setup_context()
            flask.g.cc.executions.cancel = lambda a, b: (a, b)
            execution = 1
            force = False
            data = {
                'execution_id': execution,
                'force': force}
            with self.app.test_request_context('/executions', method="PUT",
                                               data=json.dumps(data),
                                               content_type='application/'
                                               'json'):
                execution_tuple, status = self.executions.put()
                self.assertIn(execution, execution_tuple)
                self.assertEqual(202, status)
                self.assertIn(force, execution_tuple)
