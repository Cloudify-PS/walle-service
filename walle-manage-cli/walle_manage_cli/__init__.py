# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
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

import logging
import ConfigParser
import collections
import walle_manage_cli.wallemanage as walle
import pprint

_logger = None

CONFIGFILE = '.walle-manage'
SECTION = 'Manage'

USER = 'user'
TOKEN = 'token'
WALLE_HOST = 'walle_host'
WALLE_VERIFY = 'verify'

DEFAULT_PROTOCOL = 'http'
SECURED_PROTOCOL = 'https'


Configuration = collections.namedtuple('Configuration',
                                       'user, token, walle_host')


def get_logger():
    global _logger
    if _logger is not None:
        return _logger
    log_format = ('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s'
                  ' [%(asctime)s] %(message)s')
    _logger = logging.getLogger("walle_manage_logger")
    _logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


def save_config(service_parameters):
    _save_manage_config(service_parameters)


def load_config(logger):
    return _load_manage_config(logger)


def _save_manage_config(manage):
    config = ConfigParser.RawConfigParser()
    config.add_section(SECTION)
    config.set(SECTION, USER, manage.user)
    config.set(SECTION, TOKEN, manage.token)
    config.set(SECTION, WALLE_HOST, manage.walle_host)
    config.set(SECTION, WALLE_VERIFY, manage.verify)

    with open(CONFIGFILE, 'wb') as configfile:
        config.write(configfile)


def _load_manage_config(logger):
    manage = Configuration
    try:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGFILE)
        manage.user = config.get(SECTION, USER, None)
        manage.token = config.get(SECTION, TOKEN, None)
        manage.walle_host = config.get(SECTION, WALLE_HOST, None)
        manage.verify = config.get(SECTION, WALLE_VERIFY, True)
    except ConfigParser.NoSectionError as e:
        logger.info(e)
        raise RuntimeError("Can't load config. Please use 'login' command")
    return manage


def get_walle_client(config, logger):
    return walle.WalleManage(
        config.walle_host, token=config.token,
        verify=config.verify, logger=logger)


def print_dict(data):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)
