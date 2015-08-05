# Copyright (c) 2015 VMware. All rights reserved

import uuid

from score_api_server.tests.post_deployment import base


class TestBlueprintScenarios(base.BasePostDeploymentTestCase):

    def test_upload_get_delete(self):
        """Test scenarios #1

                1. Validate blueprint at client site.
                2. Upload blueprint
                3. List blueprints
                4. Get blueprint.
                5. Delete blueprint.
        """
        try:

            self.score_client.blueprints.validate(
                self.valid_blueprint_path)
            self.printer("1. Validate blueprint at client site. Passed.")

            blueprint_id = str(uuid.uuid4())
            uploaded_blueprint = self.score_client.blueprints.upload(
                self.valid_blueprint_path, blueprint_id)
            self.printer("2. Upload blueprint. Passed.",
                         self.score_client.response.json())

            self.assertIsNotNone(uploaded_blueprint)
            self.assertEqual(
                200, self.score_client.response.status_code)
            self.assertEqual(uploaded_blueprint['id'], blueprint_id)

            blueprints = self.score_client.blueprints.list()
            self.printer("3. List blueprint. Passed.",
                         self.score_client.response.json())

            self.assertNotEqual(0, len(blueprints))
            self.assertEqual(
                200, self.score_client.response.status_code)

            get_blueprint = self.score_client.blueprints.get(
                blueprint_id)
            self.printer("3. Get blueprint. Passed.",
                         self.score_client.response.json())

            self.assertEqual(uploaded_blueprint['id'],
                             get_blueprint['id'])
            self.assertEqual(
                200, self.score_client.response.status_code)

            self.score_client.blueprints.delete(blueprint_id)
            self.printer("5. Delete blueprint. Passed.",
                         self.score_client.response.json())

            self.assertEqual(
                200, self.score_client.response.status_code)

        except Exception as e:
            print(str(e))
            print(self.score_client.response.content)
            print(self.score_client.response.status_code)
            raise e
