# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask

from score_api_server.common import util
from flask import g


class FakeObj(object):
    def __init__(self, id_string, blueprint_string, deployment_string):
        self.id_string = id_string
        self.blueprint_string = blueprint_string
        self.deployment_string = deployment_string

    @property
    def id(self):
        return self.id_string

    @property
    def blueprint_id(self):
        return self.blueprint_string

    @property
    def deployment_id(self):
        return self.deployment_string


class FakeObjSmall(object):
    def __init__(self, id_string):
        self.id_string = id_string

    @property
    def id(self):
        return self.id_string


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
        def prepare(org_id, string):
            return '{}_{}'.format(org_id, string)

        with self.app.app_context():
            id_string = 'id'
            blueprint_string = 'blueprint'
            deployment_string = 'deployment'
            g.org_id = '123'
            obj = None
            util.remove_org_prefix(obj)
            obj = {'id': prepare(g.org_id, id_string)}
            res = util.remove_org_prefix(obj)
            self.assertEqual(res['id'], id_string)

            obj = {'id': prepare(g.org_id, id_string),
                   'blueprint_id': prepare(g.org_id, blueprint_string),
                   'deployment_id': prepare(g.org_id, deployment_string)}
            res = util.remove_org_prefix(obj)
            self.assertEqual(res['id'], id_string)

            obj = FakeObjSmall(id_string)
            res = util.remove_org_prefix(obj)
            self.assertEqual(res.id, id_string)

            obj = FakeObj(id_string,
                          blueprint_string,
                          deployment_string)
            res = util.remove_org_prefix(obj)
            self.assertEqual(res.id, id_string)
            self.assertEqual(res.blueprint_id, blueprint_string)
            self.assertEqual(res.deployment_id, deployment_string)
>>>>>>> SCOR-101 Update unittests for utils
