# Copyright (c) 2015 VMware. All rights reserved

import uuid
import json

from score_api_server.tests.integration import base


class TestBlueprintsReSTResources(base.IntegrationBaseTestCase):

    def setUp(self):
        super(TestBlueprintsReSTResources, self).setUp()
        self.bp_id = str(uuid.uuid4()) + "some_bp_name"

    def tearDown(self):
        super(TestBlueprintsReSTResources, self).tearDown()

    def test_list_blueprints(self):
        response = self.execute_get_request_with_route("/blueprints")
        self.assertEqual(200, response.status_code,
                         response.data)
        self.assertIn("OK", response.status,
                      response.data)
        self.assertIsNotNone(response.data)
        self.assertTrue(isinstance(json.loads(response.data), list),
                        response.data)

    def test_blueprint_not_found(self):
        response = self.execute_get_request_with_route(
            "/blueprints/%s" % self.bp_id)
        self.assertEqual(404, response.status_code,
                         response.data)

    def test_delete_blueprint_not_found(self):
        response = self.execute_delete_request_with_route(
            "/blueprints/%s" % self.bp_id)
        self.assertEqual(404, response.status_code,
                         response.data)

    def test_uploda_blueprint(self):
        response = self.make_upload_blueprint()
        self.assertEqual(200, response.status_code, response.data)
        self.assertIn("OK", response.status,
                      response.data)
        self.assertIsNotNone(json.loads(response.data),
                             response.data)

    def test_upload_invalid_blueprint(self):
        response = self.make_upload_blueprint(
            blueprint_filename="vcloud-invalid-blueprint-for-tests.yaml")
        self.assertEqual(403, response.status_code,
                         response.data)
        self.assertIn("invalid", response.data)

    def test_upload_with_get_and_delete(self):
        response_upload = self.make_upload_blueprint()
        self.assertEqual(200, response_upload.status_code,
                         response_upload.data)
        data = json.loads(response_upload.data)
        blueprint_id = data['id']
        response_get = self.execute_get_request_with_route(
            "/blueprints/%s" % blueprint_id)
        self.assertEqual(200, response_get.status_code,
                         response_upload.data)

        response_delete = self.execute_delete_request_with_route(
            "/blueprints/%s" % blueprint_id)
        self.assertEqual(200, response_delete.status_code,
                         response_upload.data)
