# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import os
import uuid

from flask.ext.migrate import upgrade
from score_api_server.common import org_limit
from score_api_server.cli import app
from score_api_server.db.models import AllowedOrgs


class CommonOrgLimitTest(testtools.TestCase):

    def setUp(self):
        # needed for load fake app from tests
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with app.app.app_context():
            # TODO(denismakogon): change hardcoded sqlite
            # TODO(denismakogon): for tests to named temporary file
            migrate_dir = current_dir + '/../../migrations/'
            upgrade(directory=migrate_dir)
            app.db.create_all()
        self.prefix = str(uuid.uuid4())
        self.org_obj_list = []
        self._create_limit_orgs()
        super(CommonOrgLimitTest, self).setUp()

    def tearDown(self):
        for org in self.org_obj_list:
            app.db.session.delete(org)
        app.db.session.commit()
        super(CommonOrgLimitTest, self).tearDown()

    def _create_limit_orgs(self):
        # add some values
        org = AllowedOrgs(self.prefix + "some_id")
        org.save()
        k_org = AllowedOrgs(self.prefix + "k_id")
        k_org.save()
        self.org_obj_list.append(k_org)
        self.org_obj_list.append(org)

    def test_get_current_limit(self):
        """get current limit for organizations"""

        with app.app.app_context():
            # check value for current existed
            flask.g.org_id = self.prefix + "some_id"
            limit = org_limit.get_current_limit()
            self.assertTrue(limit)
            self.assertIn(self.prefix + "some_id",
                          limit.org_id)
            # check count
            flask.g.org_id = self.prefix + "k_id"
            limit = org_limit.get_current_limit()
            self.assertTrue(limit)
            self.assertIn(self.prefix + "k_id", limit.org_id)
            # no orgs
            flask.g.org_id = self.prefix + "some_other_id"
            limit = org_limit.get_current_limit()
            self.assertFalse(limit)
