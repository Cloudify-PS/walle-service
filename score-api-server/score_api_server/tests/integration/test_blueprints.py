# Copyright (c) 2015 VMware. All rights reserved

import os
import uuid
import json
import urllib
import shutil
import tarfile
import tempfile

from os.path import expanduser

from score_api_server.tests.integration import base


class TestBlueprintsReSTResources(base.IntegrationBaseTestCase):

    def setUp(self):
        super(TestBlueprintsReSTResources, self).setUp()
        self.bp_id = str(uuid.uuid4()) + "some_bp_name"

    def tearDown(self):
        super(TestBlueprintsReSTResources, self).tearDown()

    def upload(self, blueprint_path, blueprint_id):
        tempdir = tempfile.mkdtemp()
        try:
            tar_path = self._tar_blueprint(blueprint_path, tempdir)
            application_file = os.path.basename(blueprint_path)
            return self._upload(
                tar_path,
                blueprint_id=blueprint_id,
                application_file_name=application_file)
        finally:
            shutil.rmtree(tempdir)

    def _tar_blueprint(self, blueprint_path, tempdir):

        blueprint_path = expanduser(blueprint_path)
        blueprint_name = os.path.basename(
            os.path.splitext(blueprint_path)[0])
        blueprint_directory = os.path.dirname(blueprint_path)

        if not blueprint_directory:
            # blueprint path only contains a file name from the local directory
            blueprint_directory = os.getcwd()
        tar_path = os.path.join(
            tempdir, '{0}.tar.gz'.format(blueprint_name))

        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(
                blueprint_directory,
                arcname=os.path.basename(blueprint_directory))

        return tar_path

    def _upload(self, tar_file,
                blueprint_id,
                application_file_name=None):
        query_params = {}
        if application_file_name is not None:
            query_params[
                'application_file_name'] = urllib.quote(
                application_file_name)

        with open(tar_file, 'rb') as f:
            return self.execute_put_request_with_route(
                '/blueprints/{0}'.format(blueprint_id),
                params=query_params,
                data=f.read()
            )

    def test_list_blueprints(self):
        response = self.execute_get_request_with_route("/blueprints")
        self.assertEqual(200, response.status_code)
        self.assertIn("OK", response.status)
        self.assertIsNotNone(response.data)
        self.assertTrue(isinstance(json.loads(response.data), list))

    def test_blueprint_not_found(self):
        response = self.execute_get_request_with_route(
            "/blueprints/%s" % self.bp_id)
        self.assertEqual(404, response.status_code)

    def test_delete_blueprint_not_found(self):
        response = self.execute_delete_request_with_route(
            "/blueprints/%s" % self.bp_id)
        self.assertEqual(404, response.status_code)

    def make_upload(self):
        # TODO(???) make blueprint path configurable
        blueprint_filename = "vcloud-postgresql-blueprint.yaml"
        current_dir = os.path.dirname(os.path.realpath(__file__))
        blueprints_dir = current_dir + '/../../../../blueprints/'
        blueprint_path = blueprints_dir + blueprint_filename
        response = self.upload(blueprint_path, blueprint_filename)
        return response

    def test_uploda_blueprint(self):
        response = self.make_upload()
        self.assertEqual(201, response.status_code)
        self.assertIn("CREATED", response.status)
        self.assertIsNotNone(json.loads(response.data))

    def test_upload_with_get(self):
        response_upload = self.make_upload()
        data = json.loads(response_upload.data)
        blueprint_id = data['blueprint_id']
        response_get = self.execute_get_request_with_route(
            "/blueprints/%s" % blueprint_id)
        self.assertNotEqual(404, response_get.status_code)
        self.assertEqual(200, response_get.status_code)
        self.assertIsNotNone(json.loads(response_get.data))

    def test_upload_with_get_and_delete(self):
        response_upload = self.make_upload()
        data = json.loads(response_upload.data)
        blueprint_id = data['blueprint_id']
        response_get = self.execute_get_request_with_route(
            "/blueprints/%s" % blueprint_id)
        response_delete = self.execute_delete_request_with_route(
            "/blueprints/%s" % blueprint_id)

        self.assertEqual(201, response_upload.status_code)
        self.assertEqual(200, response_get.status_code)
        self.assertEqual(202, response_delete.status_code)
