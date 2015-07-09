# Copyright (c) 2015 VMware. All rights reserved

import copy
import logging

from flask import g

from score_api_server.common import cfg

CONF = cfg.CONF


def add_org_prefix(name):
    return "{}_{}".format(g.org_id, name)


def remove_org_prefix(obj):
    obj_copy = copy.deepcopy(obj)
    if isinstance(obj, dict):
        replaced_id = obj['id'].replace("{}_".format(g.org_id), "", 1)
    else:
        replaced_id = obj.id.replace("{}_".format(g.org_id), "", 1)
    obj_copy['id'] = replaced_id
    obj_copy['blueprint_id'] = replaced_id
    obj_copy['deployment_id'] = replaced_id
    return obj_copy


def get_logging_level():
    logging_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
    }
    return logging_mapping.get(CONF.logging.level)
