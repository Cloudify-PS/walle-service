import unittest

import flask
import mock
import json

from score_api_server.resources import executions


class TestBase(unittest.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.executions = executions.Executions()
        self.addCleanup(super(TestBase, self).tearDown)
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
                deployment_id = self.executions.get()
                self.assertEqual(self.prefix_deployment(deployment),
                                 deployment_id)

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
                                               content_type='application/json'):
                deployment_id, workflow_id = self.executions.post()
                self.assertEqual(self.prefix_deployment(deployment),
                                 deployment_id)
                self.assertEqual(workflow, workflow_id)

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
                                               content_type='application/json'):
                execution_id, force_id = self.executions.put()
                self.assertEqual(execution, execution_id)
                self.assertEqual(force, force_id)
