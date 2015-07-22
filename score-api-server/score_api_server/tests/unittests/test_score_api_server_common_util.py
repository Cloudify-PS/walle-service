# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask

from flask import g

from score_api_server.common import util
from score_api_server.tests.fakes import fake_objects


class CommonUtilTest(testtools.TestCase):

    def setUp(self):
        super(CommonUtilTest, self).setUp()
        self.app = flask.Flask(__name__)

    def tearDown(self):
        super(CommonUtilTest, self).tearDown()

    def test_add_org_prefix(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            self.assertEqual(
                util.add_org_prefix("magic"),
                "some_id_magic"
            )

    def test_make_response_from_exception(self):
        with self.app.app_context():
            flask.g.org_id = "some_id"
            text = "Error"
            e = Exception(util.add_org_prefix(text))

            resp = util.make_response_from_exception(e, 401)
            self.assertEqual(resp.data, text)

            e.status_code = 404
            resp = util.make_response_from_exception(e)
            self.assertEqual(resp.data, text)

    def test_remove_org_prefix(self):
        with self.app.app_context():
            id_string = 'id'
            blueprint_string = 'blueprint'
            deployment_string = 'deployment'
            g.org_id = '123'

            self.assertEqual(None, util.remove_org_prefix(None))
            self.assertEqual("", util.remove_org_prefix(""))
            self.assertEqual([], util.remove_org_prefix([]))
            self.assertRaises(ValueError, util.remove_org_prefix, "Sample string")
            self.assertRaises(ValueError, util.remove_org_prefix, 123)

            test_dict = {'id': util.add_org_prefix(id_string),
                         'blueprint_id': util.add_org_prefix(blueprint_string),
                         'deployment_id': util.add_org_prefix(
                             deployment_string)}

            res = util.remove_org_prefix(test_dict)
            self.assertEqual(res['id'], id_string)
            self.assertEqual(res['blueprint_id'], blueprint_string)
            self.assertEqual(res['deployment_id'], deployment_string)

            obj = fake_objects.FakeDeployment(test_dict)
            res = util.remove_org_prefix(obj)
            self.assertEqual(res.id, id_string)
            self.assertEqual(res.blueprint_id, blueprint_string)
            self.assertEqual(res.deployment_id, deployment_string)
