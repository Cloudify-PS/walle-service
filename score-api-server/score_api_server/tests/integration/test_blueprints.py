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

    def test_uploda_blueprint(self):
        # TODO(???): write a blueprint that passes validations
        response = self.make_upload_blueprint()
        self.assertEqual(403, response.status_code)
        self.assertIn('403', response.data)
        self.assertIn(
            "Blueprint is invalid due to presence of groups",
            response.data)
        # self.assertIn("OK", response.status)
        # self.assertIsNotNone(json.loads(response.data))

    def test_upload_with_get_and_delete(self):
        response_upload = self.make_upload_blueprint()
        # blueprint_id = data['blueprint_id']
        blueprint_id = str(uuid.uuid4())
        response_get = self.execute_get_request_with_route(
            "/blueprints/%s" % blueprint_id)
        response_delete = self.execute_delete_request_with_route(
            "/blueprints/%s" % blueprint_id)

        self.assertEqual(403, response_upload.status_code)
        self.assertEqual(404, response_get.status_code)
        self.assertEqual(404, response_delete.status_code)
