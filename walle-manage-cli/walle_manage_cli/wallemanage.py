# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
# Copyright (c) 2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json


class WalleException(Exception):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


def _check_exception(logger, response):
    if response.status_code != requests.codes.ok:
        logger.error('returned %s:%s' % (
            response.status_code, response.content
        ))
        raise WalleException(response.content)


class WalleManage(object):

    def __init__(self, url, auth_url=None, token=None,
                 region=None, verify=True, logger=None):
        self.url = url
        self.token = token
        self.verify = verify
        self.response = None
        self.logger = logger

    def get_headers(self):
        headers = {}
        headers["x-walle-authorization"] = self.token
        return headers

    def get_status(self):
        self.response = requests.get(
            self.url + '/status', headers=self.get_headers(),
            verify=self.verify
        )
        return self.response.content

    def add(self, route, data):
        headers = self.get_headers()
        headers['Content-type'] = 'application/json'
        self.logger.debug("Headers: {}\n Route:{}\nData:{}".
                          format(headers, route, data))
        self.response = requests.post(self.url +
                                      '/manage/{0}'.format(route),
                                      data=json.dumps(data),
                                      headers=headers,
                                      verify=self.verify)
        _check_exception(self.logger, self.response)
        return json.loads(self.response.content)

    def delete(self, route, id):
        headers = self.get_headers()
        self.logger.debug("Headers: {}\n Route:{}\nId:{}".
                          format(headers, route, id))
        self.response = requests.delete(
            self.url + '/manage/{0}/{1}'.format(route, id),
            headers=headers,
            verify=self.verify)
        _check_exception(self.logger, self.response)
        return json.loads(self.response.content)

    def update(self, route, data):
        headers = self.get_headers()
        headers['Content-type'] = 'application/json'
        self.logger.debug("Headers: {}\n Route:{}\nData:{}".
                          format(headers, route, data))
        self.response = requests.put(self.url +
                                     '/manage/{0}'.format(route),
                                     data=json.dumps(data),
                                     headers=headers,
                                     verify=self.verify)
        _check_exception(self.logger, self.response)
        return json.loads(self.response.content)

    def list(self, route):
        headers = self.get_headers()
        self.logger.debug("Headers: {}\n Route:{}".format(headers, route))
        self.response = requests.get(self.url +
                                     '/manage/{0}'.format(route),
                                     headers=headers,
                                     verify=self.verify)
        _check_exception(self.logger, self.response)
        return json.loads(self.response.content)
