# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask

from score_api_server.common import util


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)

    def tearDown(self):
        super(TestBase, self).tearDown()

    def test_add_org_prefix(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            self.assertEqual(
                util.add_org_prefix("magic"),
                "some_id_magic"
            )