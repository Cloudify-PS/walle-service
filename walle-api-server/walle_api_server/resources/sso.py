import os

from flask.ext import restful
from flask_restful_swagger import swagger

from flask import (request, redirect, session, make_response)
from urlparse import urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saml'))
    return auth


def prepare_flask_request():
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'query_string': request.query_string,
        # TODO check it
        'request_uri': request.path
    }

class Login(restful.Resource):

    @swagger.operation(
        nickname="sso actions",
        notes="""Return for action equal metadata, possible action:
        * metadata - return metadata,
        * acs - sso login
        * slo - logout
        """
    )
    def get(self):
        req = prepare_flask_request()
        auth = init_saml_auth(req)
        if 'metadata' in request.args:
            settings = auth.get_settings()
            metadata = settings.get_sp_metadata()
            errors = settings.validate_metadata(metadata)

            if len(errors) == 0:
                resp = make_response(metadata, 200)
                resp.headers['Content-Type'] = 'text/xml'
            else:
                resp = make_response(', '.join(errors), 500)
            return resp
        elif 'acs' in request.args:
            return redirect(auth.login())
        elif 'slo' in request.args:
            return redirect(auth.logout(name_id=None, session_index=None))
        return make_response("Unsupported", 404)

    @swagger.operation(
        nickname="sso actions",
        notes="""Return for action equal metadata, possible action:
        * acs - login redirect
        * sls - logout redirect
        """
    )
    def post(self):
        req = prepare_flask_request()
        auth = init_saml_auth(req)
        if 'acs' in request.args:
            auth.process_response()
            errors = auth.get_errors()
            not_auth_warn = not auth.is_authenticated()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                return redirect(auth.redirect_to(request.form['RelayState']))
            return str((not_auth_warn, auth.get_attributes(), auth.get_nameid(), auth.get_session_index()))
        elif 'sls' in request.args:
            url = auth.process_slo(delete_session_cb=[])
            errors = auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return redirect(url)
        return make_response("Unsupported", 404)
