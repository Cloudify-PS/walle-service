# Copyright (c) 2015 VMware. All rights reserved

import copy
import logging
from functools import wraps
from jsonschema import ValidationError, validate
from werkzeug.exceptions import BadRequest

from flask import g, request, make_response

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


def validate_json(schema):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            try:
                json = request.get_json(force=True)
                validate(json, schema)
                return fn(args[0], json, **kwargs)
            except BadRequest as e:
                setup_logging(__name__).exception(e)
                return make_response("Unauthorized."
                                     " Can't parse input json file", 401)
            except ValidationError as e:
                setup_logging(__name__).exception(e)
                return make_response("Unauthorized."
                                     " Validation error: {}.".format(e),
                                     401)
        return decorated
    return wrapper
