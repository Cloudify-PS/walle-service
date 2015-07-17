# Copyright (c) 2015 VMware. All rights reserved

import copy
import logging

from flask import g, make_response

from score_api_server.common import cfg

CONF = cfg.CONF


def add_org_prefix(name):
    return "{}_{}".format(g.org_id, name)


def remove_org_prefix(obj):
    def replace(obj, attr):
        if isinstance(obj, dict):
            replaced = obj[attr].replace("{}_".format(g.org_id), "", 1)
        else:
            replaced = getattr(obj, attr).replace("{}_".format(
                g.org_id), "", 1)
        return replaced

    obj_copy = copy.deepcopy(obj)
    obj_copy['id'] = replace(obj, 'id')
    obj_copy['blueprint_id'] = replace(obj, 'blueprint_id')
    obj_copy['deployment_id'] = replace(obj, 'deployment_id')
    return obj_copy


def make_response_from_exception(exception, code=None):
    def remove_org(e):
        return str(e).replace("{}_".format(g.org_id), "")

    status = code if code else exception.status_code
    return make_response(remove_org(exception),
                         status)


def get_logging_level():
    logging_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
    }
    return logging_mapping.get(CONF.logging.level)


def common_log_setup():
    log_file_handler = logging.FileHandler(CONF.logging.file)
    formatter = logging.Formatter(CONF.logging.formatter,
                                  "%Y-%m-%d %H:%M:%S")
    log_file_handler.setFormatter(formatter)
    return log_file_handler


def setup_logging_for_app(app):
    app.logger.addHandler(common_log_setup())
    app.logger.setLevel(get_logging_level())


def setup_logging(name):
    import logging
    log_file_handler = common_log_setup()
    logger = logging.getLogger(name)
    logger.addHandler(log_file_handler)
    logger.setLevel(get_logging_level())
    return logger
