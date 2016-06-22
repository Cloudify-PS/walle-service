# Copyright (c) 2015 VMware. All rights reserved

import os
import testtools

from flask.ext.migrate import upgrade

from walle_api_server.cli import app


class BaseTestCaseWihtBackend(testtools.TestCase):

    def setUp(self):
        # needed for load fake app from tests
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with app.app.app_context():
            # TODO(denismakogon): change hardcoded sqlite
            # TODO(denismakogon): for tests to named temporary file
            migrate_dir = current_dir + '/../../../migrations/'
            upgrade(directory=migrate_dir)
            app.db.create_all()
        self.obj_list = []
        super(BaseTestCaseWihtBackend, self).setUp()

    def tearDown(self):
        for org in self.obj_list:
            app.db.session.delete(org)
        app.db.session.commit()
        super(BaseTestCaseWihtBackend, self).tearDown()
