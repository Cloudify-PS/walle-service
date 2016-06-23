# Copyright (c) 2015 VMware. All rights reserved

from walle_api_server.tests.integration import base


class TestWalleAuthorizationHooks(base.IntegrationBaseTestCase):
    def setUp(self):
        super(TestWalleAuthorizationHooks, self).setUp()
        self.safe = base.vcloud_air_client.VCS.login

    def tearDown(self):
        super(TestWalleAuthorizationHooks, self).tearDown()
        base.vcloud_air_client.VCS.login = self.safe

    def test_unauthorized(self):
        rv = self.try_auth()
        self.assertEqual(401, rv.status_code)

    def test_authorized_with_no_limits(self):
        response = self.try_auth(
            headers={
                "x-vcloud-authorization": "True",
                "x-vcloud-org-url": "URL",
                "x-vcloud-version": "some_version"
            })
        self.assertEqual(403, response.status_code)
        self.assertIn("FORBIDDEN", response.status)
        self.assertIn("were not defined.", response.data)

    def test_authorize_with_existing_limits(self):
        response = self.execute_get_request_with_route("/")
        # code 404 means that Walle doesn't
        # have such route and pinned resource
        self.assertEqual(404, response.status_code)
