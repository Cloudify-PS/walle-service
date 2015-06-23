import os
import tarfile
import tempfile
import unittest

import flask
import mock

from score_api_server.resources import blueprints
from tests.unittests import fake_objects


class TestBase(unittest.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.addCleanup(super(TestBase, self).tearDown)

    @mock.patch.object(os, 'listdir')
    @mock.patch.object(tarfile, 'open')
    @mock.patch.object(tarfile.TarFile, 'extractall')
    @mock.patch.object(blueprints.Blueprints, '_save_file_locally')
    @mock.patch.object(tempfile, 'mkdtemp')
    def test_remove_org_prefix(self, mock_mkdtemp, mock_save_file,
                               mock_extractall, mock_open, mock_listdir):
        mock_mkdtemp.return_value = '/tmp'
        bp_id = 'foo'
        mock_listdir.return_value = [bp_id]
        bluprient = blueprints.Blueprints()
        with self.app.app_context():
            flask.g.org_id = "some_id"
            flask.g.cc = mock.MagicMock()
            fake_id = flask.g.org_id + '_' + bp_id
            fake_bp = fake_objects.FakeBlueprint(fake_id, fake_id, fake_id)
            flask.g.cc.blueprints.upload = mock.MagicMock(
                return_value=fake_bp)
            with self.app.test_request_context('/?application_file_name=bar'):
                bp, status = bluprient.put(bp_id)

        self.assertEqual(bp_id, bp.id)
