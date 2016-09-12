# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock

from walle_api_server.resources import blueprints
from walle_api_server.tests.fakes import fake_objects
from walle_api_server.tests.fakes import http_proxy
from walle_api_server.common import service_limit


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.bp_id = 'foo'
        self.app = flask.Flask(__name__)
        self.bluprient = blueprints.Blueprints()
        self.bluprient_id = blueprints.BlueprintsId()

    def test_get_with_blueprint_id(self):
        with self.app.app_context():
            flask.g.tenant_id = "some_id"
            flask.g.cc = mock.MagicMock()
            flask.g.rights = [service_limit.USER_RIGHT]
            fake_id = flask.g.tenant_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.get = mock.MagicMock(return_value=fake_bp)
            with self.app.test_request_context():
                bp = self.bluprient_id.get(blueprint_id=self.bp_id)
        self.assertEqual(self.bp_id, bp.id)

    def test_get_all_blueprints(self):
        with self.app.app_context():
            flask.g.tenant_id = "some_id"
            flask.g.cc = mock.MagicMock()
            flask.g.rights = [service_limit.USER_RIGHT]
            flask.g.proxy = http_proxy.HTTPClient("host")
            fake_id = flask.g.tenant_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.list = mock.MagicMock(return_value=[fake_bp])
            bps = self.bluprient.get()
            self.assertEqual(self.bp_id, bps["items"][0]["id"])

    def test_delete(self):
        with self.app.app_context():
            flask.g.tenant_id = "some_id"
            flask.g.cc = mock.MagicMock()
            flask.g.rights = [service_limit.USER_RIGHT]
            fake_id = flask.g.tenant_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.get = mock.MagicMock(return_value=None)
            flask.g.cc.blueprints.delete = mock.MagicMock(return_value=fake_bp)
            with self.app.test_request_context():
                bp = self.bluprient_id.delete(blueprint_id=self.bp_id)
            self.assertEqual(self.bp_id, bp.id)
