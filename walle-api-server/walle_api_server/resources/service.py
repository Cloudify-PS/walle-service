import walle_api_server
from walle_api_server.resources import responses

from flask import g
from flask.ext import restful
from flask_restful_swagger import swagger

from cloudify_rest_client import exceptions

from walle_api_server.common import util

logger = util.setup_logging(__name__)


class Status(restful.Resource):

    @swagger.operation(
        responseClass=responses.Status,
        nickname="status",
        notes="Returns state of running system services"
    )
    def get(self):
        logger.debug("Entering Status.get method.")
        try:
            logger.info("Checking Walle version.")
            walle_version = walle_api_server.get_version()
            logger.info("Checking Cloudify manager version.")
            manager_version = g.cc.manager.get_version()
            logger.info("Checking Cloudify manager status.")
            manager_status = g.cc.manager.get_status()
            logger.debug("Done. Exiting Status.get method.")
            return {"walle_version": walle_version,
                    "manager_version": manager_version["version"],
                    "manager_status": manager_status["status"]}
        except (Exception, exceptions.CloudifyClientError) as e:
            logger.error(str(e))
            status = (400 if not isinstance(e, exceptions.CloudifyClientError)
                      else e.status_code)
            return util.make_response_from_exception(e, status)


class Maintenance(restful.Resource):

    def get(self):
        return {"status": "deactivated", "requested_by": "",
                "activated_at": "", "activation_requested_at": "",
                "remaining_executions": None}


class Version(restful.Resource):

    def get(self):
        return {"date": "", "commit": "",
                "version": walle_api_server.get_version(),
                "build": ""}


class Context(restful.Resource):

    def get(self):
        return True
