# Copyright (c) 2015 VMware. All rights reserved

from score_api_server.tests.integration import base


class TestApiLogin(base.IntegrationBaseTestCase):

    def test_spec(self):
        response = self.execute_post_request_with_route("/login")
        self.assertEqual(401, response.status_code)
        self.assertIsNone(response.data)
