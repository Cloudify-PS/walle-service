# Copyright (c) 2015 VMware. All rights reserved

from walle_api_server.tests.integration import base


class TestApiLogin(base.IntegrationBaseTestCase):

    def test_spec(self):
        response = self.execute_post_request_with_route("/login")
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.data, "Bad json data in request body. "
                         "Can't parse input json file")
