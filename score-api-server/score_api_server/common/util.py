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
    if not isinstance(name, basestring) or not name:
        raise ValueError("Name must be nonempty instance of basestring.")
    return "{}_{}".format(g.tenant_id, name)


def remove_org_prefix(obj):
    if not obj:
        return obj
    if not isinstance(obj, dict):
        raise ValueError("Object must be instance of dict")
    obj_copy = copy.deepcopy(obj)
    for attr in ('id', 'blueprint_id', 'deployment_id'):
        try:
            if obj_copy[attr]:
                obj_copy[attr] = obj_copy[attr].replace(
                    "{}_".format(g.tenant_id), "", 1)
        except KeyError:
            pass
    return obj_copy


def make_response_from_exception(exception, code=None):
    def remove_org(e):
        response = str(e)
        response = response.replace("{}_".format(g.tenant_id), "")
        return response

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
                return make_response("Bad json data in request body."
                                     " Can't parse input json file", 400)
            except ValidationError as e:
                setup_logging(__name__).exception(e)
                return make_response(" Validation error: {}.".format(e),
                                     400)
        return decorated
    return wrapper


def add_prefix_to_deployment(deployment_id):
    if deployment_id:
        return add_org_prefix(deployment_id)
    return deployment_id
