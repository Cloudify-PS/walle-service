# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import mock
import json
from score_api_server.resources import login
import score_api_server


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.app = flask.Flask(__name__)
        self.test_id = "some_id"

    def setup_context(self):
        flask.g.org_id = self.test_id
        flask.g.cc = mock.MagicMock()

    def test_login(self):
        with self.app.app_context():
            self.setup_context()

    def test_local_functions(self):
        self.assertTrue(login._is_ondemand('ondemand'))
        self.assertTrue(login._is_subscription('subscription'))
        self.assertEqual(login._add_prefix('host'), 'https://host')
        self.assertEqual(login._add_prefix('https://test'), 'https://test')
        self.assertEqual(login._set_host('host', 'ondemand'), 'https://host')
        self.assertEqual(login._set_host('', 'ondemand'),
                         'https://iam.vchs.vmware.com')
        self.assertEqual(login._set_host('', 'subscription'),
                         'https://vchs.vmware.com')
        self.assertEqual(login._set_version('5.0', 'ondemand'), '5.0')
        self.assertEqual(login._set_version('', 'ondemand'), '5.7')
        self.assertEqual(login._set_version('', 'subscription'), '5.6')

    @mock.patch('score_api_server.resources.login.VCA')
    def test_login_user_to_service(self, mock_vca):
        fake_vca = mock.MagicMock()
        mock_vca.return_value = fake_vca

        fake_vca.login = mock.MagicMock(return_value=False)
        self.assertFalse(login._login_user_to_service(1, 2, 3, 4, 5, 6, 7, 8))

        fake_vca.login = mock.MagicMock(return_value=True)
        fake_vca.login_to_instance = mock.MagicMock(return_value=True)
        self.assertTrue(login._login_user_to_service(1, 2, 3, 'ondemand',
                                                     5, 6, 7, 8))

        fake_vca.instances = False
        self.assertFalse(login._login_user_to_service(1, 2, 3, 'ondemand',
                                                      5, None, 7, 8))

        fake_vca.login_to_instance = mock.MagicMock(return_value=False)
        self.assertFalse(login._login_user_to_service(1, 2, 3, 'ondemand',
                                                      5, 6, 7, 8))

        fake_vca.login_to_org = mock.MagicMock(return_value=True)
        self.assertTrue(login._login_user_to_service(1, 2, 3, 'subscription',
                                                     5, 6, 7, 8))

        fake_vca.services = False
        fake_vca.services = mock.MagicMock()
        fake_vca.services.get_Service = mock.MagicMock(return_value=False)
        self.assertFalse(login._login_user_to_service(1, 2, 3, 'subscription',
                                                      5, 6, None, None))

        self.assertTrue(login._login_user_to_service(1, 2, 3, 'subscription',
                                                     5, 6, None, 8))
        fake_vca.login_to_org = mock.MagicMock(return_value=False)
        self.assertFalse(login._login_user_to_service(1, 2, 3, 'subscription',
                                                      5, 6, 7, 8))

    def test_post(self):
        testlogin = login.Login()
        data = {
            'user': 'user',
            'password': 'password',
            'instance': 'instance',
            'service': 'service'}
        with self.app.app_context():
            with self.app.test_request_context('/login', method="POST"):
                self.assertEqual(testlogin.post().status_code, 401)

        with self.app.test_request_context('/login', method="POST",
                                           data=json.dumps(data),
                                           content_type='application/'
                                           'json'):
            with mock.patch.object(score_api_server.resources.login,
                                   '_login_user_to_service') as fake_login:
                token = 1
                org_url = 'url'
                version = 5
                fake_vca = mock.MagicMock()
                fake_vca.vcloud_session = mock.MagicMock()
                fake_vca.vcloud_session.token = token
                fake_vca.vcloud_session.org_url = org_url
                fake_vca.version = version
                fake_login.return_value = fake_vca
                result = {"x_vcloud_authorization": token,
                          "x_vcloud_org_url": org_url,
                          "x_vcloud_version": version}
                self.assertEqual(testlogin.post(), result)
                fake_login.assert_called_with('user',
                                              'https://iam.vchs.vmware.com',
                                              'password', 'ondemand', '5.7',
                                              'instance', 'service', None)

                fake_login.side_effect = Exception(404)
                self.assertRaises(Exception, testlogin.post())
