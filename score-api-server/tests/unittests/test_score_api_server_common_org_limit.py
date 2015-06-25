# Copyright (c) 2015 VMware. All rights reserved

import testtools
import flask
import os
import random
import string
import sys
from flask.ext.migrate import upgrade
from score_api_server.common import org_limit
# needed for load fake app from tests
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)
import app
# import db models
from score_api_server.resources.models import UsedOrgs, AllowedOrgs
# migrate db before run tests
with app.app.app_context():
    migrate_dir = current_dir + '/../../migrations/'
    upgrade(directory=migrate_dir)
    app.db.create_all()


class CommonOrgLimitTest(testtools.TestCase):

    def setUp(self):
        super(CommonOrgLimitTest, self).setUp()

        self.prefix = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(10)
        )
        self.org_obj_list = []

    def tearDown(self):
        for org in self.org_obj_list:
            app.db.session.delete(org)
        app.db.session.commit()
        super(CommonOrgLimitTest, self).tearDown()

    def _create_usage_orgs(self):
        # add some values
        org = UsedOrgs(self.prefix + "some_id", 0)
        k_org = UsedOrgs(self.prefix + "k_id", 1024)
        app.db.session.add(org)
        app.db.session.add(k_org)
        app.db.session.commit()
        self.org_obj_list.append(k_org)
        self.org_obj_list.append(org)

    def _create_limit_orgs(self):
        # add some values
        org = AllowedOrgs(self.prefix + "some_id", 0)
        k_org = AllowedOrgs(self.prefix + "k_id", 1024)
        app.db.session.add(org)
        app.db.session.add(k_org)
        app.db.session.commit()
        self.org_obj_list.append(k_org)
        self.org_obj_list.append(org)

    def test_get_current_usage(self):
        """get current amount of installation by organization"""
        with app.app.app_context():
            self._create_usage_orgs()
            # check value for current existed
            flask.g.org_id = self.prefix + "some_id"
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "some_id")
            self.assertEqual(usage.deployments_count, 0)
            # check count
            flask.g.org_id = self.prefix + "k_id"
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "k_id")
            self.assertEqual(usage.deployments_count, 1024)
            # no orgs, created new record without commit
            flask.g.org_id = self.prefix + "some_other_id"
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "some_other_id")
            self.assertEqual(usage.deployments_count, 0)

    def test_get_current_limit(self):
        """get current limit for organizations"""
        with app.app.app_context():
            self._create_limit_orgs()
            # check value for current existed
            flask.g.org_id = self.prefix + "some_id"
            limit = org_limit.get_current_limit()
            self.assertTrue(limit)
            self.assertEqual(limit.org_id, self.prefix + "some_id")
            self.assertEqual(limit.deployments_limit, 0)
            # check count
            flask.g.org_id = self.prefix + "k_id"
            limit = org_limit.get_current_limit()
            self.assertTrue(limit)
            self.assertEqual(limit.org_id, self.prefix + "k_id")
            self.assertEqual(limit.deployments_limit, 1024)
            # no orgs
            flask.g.org_id = self.prefix + "some_other_id"
            limit = org_limit.get_current_limit()
            self.assertFalse(limit)

    def test_decrement(self):
        """check decrement usage of organization"""
        with app.app.app_context():
            self._create_usage_orgs()
            # if current usage is zero, does not do any thing
            flask.g.org_id = self.prefix + "some_id"
            org_limit.decrement()
            # check
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "some_id")
            self.assertEqual(usage.deployments_count, 0)
            # current usage is not zero
            flask.g.org_id = self.prefix + "k_id"
            org_limit.decrement()
            # check
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "k_id")
            self.assertEqual(usage.deployments_count, 1023)

    def test_increment(self):
        """check increment usage of organization"""
        with app.app.app_context():
            self._create_usage_orgs()
            self._create_limit_orgs()
            # if current usage is zero, does not do any thing
            flask.g.org_id = self.prefix + "some_id"
            org_limit.increment()
            # check
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "some_id")
            self.assertEqual(usage.deployments_count, 1)
            # current usage is not zero
            flask.g.org_id = self.prefix + "k_id"
            self.assertFalse(org_limit.increment())
            # check
            usage = org_limit.get_current_usage()
            self.assertTrue(usage)
            self.assertEqual(usage.org_id, self.prefix + "k_id")
            self.assertEqual(usage.deployments_count, 1024)
            # unknow org_id
            flask.g.org_id = self.prefix + "something_secret"
            self.assertFalse(org_limit.increment())
