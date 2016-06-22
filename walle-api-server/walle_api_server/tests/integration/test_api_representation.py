# Copyright (c) 2015 VMware. All rights reserved

from walle_api_server.tests.integration import base


class TestApiRepresentation(base.IntegrationBaseTestCase):

    def test_spec(self):
        response = self.execute_get_request_with_route("/api/spec.json")
        self.assertEqual(200, response.status_code)
        self.assertIn("OK", response.status)
        self.assertIsNotNone(response.data)
