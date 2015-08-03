# Copyright (c) 2015 VMware. All rights reserved

import uuid
import json
import testtools

from score_api_server.tests.integration import base


class TestBlueprintsReSTResources(base.IntegrationBaseTestCase):

    def setUp(self):
        super(TestBlueprintsReSTResources, self).setUp()
        self.bp_id = str(uuid.uuid4()) + "some_bp_name"

    def tearDown(self):
        for blueprint in json.loads(
                self.execute_get_request_with_route(
                "/blueprints").data):
            self.execute_delete_request_with_route(
                "/blueprints/%s" %
                blueprint['id'])
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

    def test_upload_blueprint(self):
        response = self.make_upload_blueprint()
        self.assertEqual(200, response.status_code, response.data)
        self.assertIn("OK", response.status,
                      response.data)
        self.assertIsNotNone(json.loads(response.data),
                             response.data)

    def _upload_invalid_blueprint(self, name, expected_code=403,
                                  expected_message_part="invalid"):
        response = self.make_upload_blueprint(
            blueprint_filename=name)
        self.assertEqual(403, expected_code, response.data)
        self.assertIn(expected_message_part, response.data)

    def test_upload_invalid_blueprint(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-for-tests.yaml")

    def test_upload_blueprint_with_relative_import(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-with-relative-import.yaml",
            expected_message_part="Unable to access types definition file")

    def test_upload_blueprint_with_unapproved_plugins(self):
        self.drop_approved_plugins()
        self._upload_invalid_blueprint(
            "vcloud-blueprint-for-tests.yaml", 403,
            expected_message_part="is not approved. Blueprint: ")
        self.recreate_approved_plugins()

    def test_upload_blueprint_with_file_uri(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-with-file-uri-import.yaml",
            403, expected_message_part="Invalid types import - "
                                       "file://filesomewhere. ")

    def test_upload_blueprint_fabric_forward_agent(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-fabric-env-forward_agent.yaml",
            403, expected_message_part="Invalid fabric env - "
                                       "forward_agent is not allowed")

    @testtools.skip("SCOR-149")
    def test_upload_blueprint_fabric_key_filename(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-fabric-env-key_filename.yaml",
            403, expected_message_part="Invalid fabric env - "
                                       "key_file is not allowed")

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

    def test_upload_blueprint_with_buitin_tasks(self):
        self._upload_invalid_blueprint(
            "vcloud-invalid-blueprint-with-builtins.yaml", 403,
            expected_message_part='Forbidden workflow '
                                  'diamond_agent.tasks.')
