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
