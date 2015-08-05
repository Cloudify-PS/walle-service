# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock

from score_api_server.resources import deployments


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.test_id = "some_id"
        self.outputs = deployments.DeploymentOutputs()

    def setup_context(self):
        flask.g.org_id = self.test_id
        flask.g.cc = mock.MagicMock()
        flask.g.cc.deployments = mock.MagicMock()

    def test_deployments_output(self):
        with self.app.app_context():
            self.setup_context()
            output = {"var": "val"}
            flask.g.cc.deployments.outputs = mock.MagicMock()
            flask.g.cc.deployments.outputs.get = lambda d: {"outputs": output,
                                                            "deployment_id": d}
            deployment_id = "deployment_id"
            outputs = self.outputs.get(deployment_id)
            self.assertEqual(outputs, {"outputs": output,
                                       "deployment_id": deployment_id})
