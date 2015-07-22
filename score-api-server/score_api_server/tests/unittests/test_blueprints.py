# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock

from score_api_server.resources import blueprints
from score_api_server.tests.fakes import fake_objects


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.bp_id = 'foo'
        self.app = flask.Flask(__name__)
        self.bluprient = blueprints.Blueprints()
        self.bluprient_id = blueprints.BlueprintsId()

    def test_get_with_blueprint_id(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.get = mock.MagicMock(return_value=fake_bp)
            bp = self.bluprient_id.get(blueprint_id=self.bp_id)
        self.assertEqual(fake_id, bp.id)

    def test_get_all_blueprints(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.list = mock.MagicMock(return_value=[fake_bp])
            bps = self.bluprient.get()
        self.assertEqual(self.bp_id, bps[0].id)

    def test_delete(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.delete = mock.MagicMock(
                return_value=fake_bp)
            bp = self.bluprient_id.delete(blueprint_id=self.bp_id)
        self.assertEqual(fake_id, bp.id)
