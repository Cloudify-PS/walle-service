# Copyright (c) 2016 VMware. All rights reserved
import hashlib
import time
from flask import make_response, g
from walle_api_server.resources import responses
from flask.ext import restful
from walle_api_server.common import util
from flask_restful_swagger import swagger


logger = util.setup_logging(__name__)


class LoginWalle(restful.Resource):
    @swagger.operation(
        responseClass=responses.LoginWalle,
        nickname="login_walle",
        notes="Returns information for authorization in Walle.",
        parameters=[{'name': 'user',
                     'description': 'User login.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'password',
                     'description': 'User password.',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=['application/json']
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "user": {"type": "string", "minLength": 1},
             "password": {"type": "string", "minLength": 1}
         },
         "required": ["user", "password"]}
    )
    def post(self, json):
        logger.debug("Entering Login.get method.")
        user = json.get('user')
        password = json.get('password')
        walle_logined = False
        from walle_api_server.db.models import WalleAdministrators
        admin = WalleAdministrators.find_by(name=user)
        if admin and admin.password_check(password):
            expire_time = _get_expire_time()
            g.token = _generate_token(password, expire_time)
            admin.update(token=g.token, expire=expire_time)
            walle_logined = True
        else:
            logger.error("Login failed")
        if walle_logined:
            reply = {
                'x-walle-authorization': g.token,
            }
            return reply
        return make_response("Unauthorized. Recheck credentials.", 401)


def _get_expire_time():
    now = time.time()
    expire_sec = 30 * 60
    return now + expire_sec


def _generate_token(password, timestamp):
    return hashlib.md5(password + str(timestamp)).hexdigest()
