# Copyright (c) 2015 VMware. All rights reserved

import uuid

from score_api_server.db import models


class VCS(object):

    class Org(object):

        def __init__(self):
            self.id = ":".join([str(uuid.uuid4())])
            if self.id not in [org.tenant_id
                               for org in
                               models.AllowedOrgs.list()]:
                models.AllowedOrgs(
                    self.id,
                    info="org-id-%s" % self.id)

    def __init__(self, url, username, org,
                 instance, api_url, org_url,
                 version='5.7', verify=True, log=False):
        self.url = url
        self.username = username
        self.token = None
        self.org = org
        self.instance = instance
        self.version = version
        self.verify = verify
        self.api_url = api_url
        self.org_url = org_url
        self.organization = None
        self.response = None
        self.session = None
        self.log = log
        self.logger = None

    def login(self, password=None, token=None):
        self.organization = self.Org()
        return self
