# Copyright (c) 2015 VMware. All rights reserved

import testtools
import os
import tarfile
import tempfile

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

    @mock.patch.object(os, 'listdir')
    @mock.patch.object(tarfile, 'open')
    @mock.patch.object(tarfile.TarFile, 'extractall')
    @mock.patch.object(blueprints.BlueprintsId, '_save_file_locally')
    @mock.patch.object(tempfile, 'mkdtemp')
    def test_put(self, mock_mkdtemp, mock_save_file,
                 mock_extractall, mock_open, mock_listdir):
        mock_mkdtemp.return_value = '/tmp'

        mock_listdir.return_value = [self.bp_id]
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.upload = mock.MagicMock(return_value=fake_bp)
            with self.app.test_request_context('/?application_file_name=bar'):
                bp = self.bluprient_id.put(self.bp_id)

        self.assertEqual(self.bp_id, bp.id)

    def test_get_with_blueprint_id(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + self.bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.get = mock.MagicMock(return_value=fake_bp)
            bp = self.bluprient_id.get(blueprint_id=self.bp_id)
        self.assertEqual(self.bp_id, bp.id)

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
            flask.g.cc.blueprints.get = mock.MagicMock(return_value=None)
            flask.g.cc.blueprints.delete = mock.MagicMock(return_value=fake_bp)
            bp = self.bluprient_id.delete(blueprint_id=self.bp_id)
            self.assertEqual(self.bp_id, bp.id)
