
from flask.ext import restful
from score_api_server.common import util

logger = util.setup_logging(__name__)


class OrgIds(restful.Resource):
    def get(self):
        logger.debug("Entering OrgIds.get method.")
        logger.info("Listing all org_ids.")

        from score_api_server.db import models
        org_ids = models.AllowedOrgs.list()
        return [o.to_dict() for o in org_ids]

    @util.validate_json(
        {"type": "object",
         "properties": {
             "org_id": {"type": "string", "minLength": 1},
             "info": {"type": ["string", "null"]},
         },
         "required": ["org_id"]}
    )
    def post(self, json):
        logger.debug("Entering OrgIds.post method.")
        logger.info("Update org_ids.")
        from score_api_server.db import models
        org = models.AllowedOrgs(json['org_id'], info=json['info'])
        return org.to_dict()


class OrgIdsId(restful.Resource):
    def delete(self, org_id):
        logger.debug("Entering OrgIds.delete method.")
        logger.info("Delete org_ids.")
        from score_api_server.db import models
        org = models.AllowedOrgs.find_by(org_id=org_id)
        if org:
            org.delete()
            return "OK"
        else:
            return "ERROR: Org-ID not found"


class OrgIdLimits(restful.Resource):
    def get(self):
        logger.debug("Entering OrgIdLimitss.get method.")
        logger.info("Listing all org_id_limits.")
        from score_api_server.db import models
        limits = models.OrgIDToCloudifyAssociationWithLimits.list()
        return [l.to_dict() for l in limits]

    @util.validate_json(
        {"type": "object",
         "properties": {
             "org_id": {"type": "string", "minLength": 1},
             "cloudify_host": {"type": "string", "minLength": 1},
             "cloudify_port": {"type": "string", "minLength": 1},
             "deployment_limits": {"type": "string", "minLength": 1},
         },
         "required": ["org_id", "cloudify_host", "cloudify_port",
                      "deployment_limits"]}
    )
    def post(self, json):
        logger.debug("Entering OrgIdLimits.post method.")
        logger.info("Create org_id_limits.")
        from score_api_server.db import models
        if not models.AllowedOrgs.find_by(org_id=json['org_id']):
            return "ERROR: No such Org-ID."
        limit = models.OrgIDToCloudifyAssociationWithLimits(
            json['org_id'],
            json['cloudify_host'],
            json['cloudify_port'],
            json['deployment_limits'],
        )
        return limit.to_dict()

    @util.validate_json(
        {"type": "object",
         "properties": {
             "id": {"type": "string", "minLength": 1},
             "org_id": {"type": ["string", "null"]},
             "cloudify_host": {"type": ["string", "null"]},
             "cloudify_port": {"type": ["string", "null"]},
             "deployment_limits": {"type": ["string", "null"]},
             "number_of_deployments": {"type": ["string", "null"]},
         },
         "required": ["id"]}
    )
    def put(self, json):
        logger.debug("Entering OrgIdLimits.put method.")
        logger.info("Update org_id_limits.")
        from score_api_server.db import models
        update_json = {}
        limit_id = json["id"]

        keys = ["org_id", "cloudify_host", "cloudify_port",
                "deployment_limits", "number_of_deployments"]

        for key in keys:
            if json.get(key):
                update_json.update({key: json.get(key)})

        if not models.AllowedOrgs.find_by(org_id=json.get("org_id"))\
                and not limit_id:
            return "ERROR: ID or existing Org-ID required."

        limit = models.OrgIDToCloudifyAssociationWithLimits.find_by(
            id=limit_id)
        if not limit:
            return "No such Org-ID limit entity."
        else:
            limit.update(**update_json)
            updated_limit = (
                models.OrgIDToCloudifyAssociationWithLimits.find_by(
                    id=limit_id))
            return updated_limit.to_dict()


class OrgIdLimitsId(restful.Resource):
    def delete(self, id):
        logger.debug("Entering OrgIdLimits.delete method.")
        logger.info("Delete org_id_limit.")
        from score_api_server.db import models
        limit = models.OrgIDToCloudifyAssociationWithLimits.find_by(id=id)
        if not limit:
            return "ERROR: No such Org-ID limit entity."
        else:
            limit.delete()
            return "OK"


class KeystoreUrls(restful.Resource):
    def get(self):
        logger.debug("Entering KeystoreUrls.get method.")
        logger.info("Listing all keystore_url.")

        from score_api_server.db import models
        keystore_url = models.AllowedKeyStoreUrl.list()
        return [u.to_dict() for u in keystore_url]

    @util.validate_json(
        {"type": "object",
         "properties": {
             "keystore_url": {"type": "string", "minLength": 1},
             "info": {"type": ["string", "null"]},
         },
         "required": ["keystore_url"]}
    )
    def post(self, json):
        logger.debug("Entering KeystoreUrls.post method.")
        logger.info("Update keystore_url.")
        from score_api_server.db import models
        url = models.AllowedKeyStoreUrl(
            json['keystore_url'], info=json['info']
        )
        return url.to_dict()


class KeystoreUrlsId(restful.Resource):
    def delete(self, keystore_url):
        logger.debug("Entering KeystoreUrlsId.delete method.")
        logger.info("Delete keystore_url.")
        from score_api_server.db import models
        org = models.AllowedKeyStoreUrl.find_by(keystore_url=keystore_url)
        if org:
            org.delete()
            return "OK"
        else:
            return "ERROR: keystore_url not found"


class KeyStoreUrlLimits(restful.Resource):
    def get(self):
        logger.debug("Entering OrgIdLimitss.get method.")
        logger.info("Listing all keystore_url_limit.")
        from score_api_server.db import models
        limits = models.KeyStoreUrlToCloudifyAssociationWithLimits.list()
        return [l.to_dict() for l in limits]

    @util.validate_json(
        {"type": "object",
         "properties": {
             "keystore_url": {"type": "string", "minLength": 1},
             "cloudify_host": {"type": "string", "minLength": 1},
             "cloudify_port": {"type": "string", "minLength": 1},
             "deployment_limits": {"type": "string", "minLength": 1},
         },
         "required": ["keystore_url", "cloudify_host", "cloudify_port",
                      "deployment_limits"]}
    )
    def post(self, json):
        logger.debug("Entering OrgIdLimits.post method.")
        logger.info("Create org_id_limits.")
        from score_api_server.db import models
        if not models.AllowedKeyStoreUrl.\
                find_by(keystore_url=json['keystore_url']):
            return "ERROR: No such Org-ID."
        limit = models.KeyStoreUrlToCloudifyAssociationWithLimits(
            json['keystore_url'],
            json['cloudify_host'],
            json['cloudify_port'],
            json['deployment_limits'],
        )
        return limit.to_dict()

    @util.validate_json(
        {"type": "object",
         "properties": {
             "id": {"type": "string", "minLength": 1},
             "keystore_url": {"type": ["string", "null"]},
             "cloudify_host": {"type": ["string", "null"]},
             "cloudify_port": {"type": ["string", "null"]},
             "deployment_limits": {"type": ["string", "null"]},
             "number_of_deployments": {"type": ["string", "null"]},
         },
         "required": ["id"]}
    )
    def put(self, json):
        logger.debug("Entering KeyStoreUrlLimits.put method.")
        logger.info("Update keystore_url.")
        from score_api_server.db import models
        update_json = {}
        limit_id = json["id"]

        keys = ["keystore_url", "cloudify_host", "cloudify_port",
                "deployment_limits", "number_of_deployments"]

        for key in keys:
            if json.get(key):
                update_json.update({key: json.get(key)})

        if not models.AllowedKeyStoreUrl.find_by(
                keystore_url=json.get("keystore_url"))\
                and not limit_id:
            return "ERROR: ID or existing keystore_url required."

        limit = models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
            id=limit_id)
        if not limit:
            return "No such keystore_url limit entity."
        else:
            limit.update(**update_json)
            updated_limit = (
                models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
                    id=limit_id))
            return updated_limit.to_dict()


class KeyStoreUrlLimitsId(restful.Resource):
    def delete(self, id):
        logger.debug("Entering KeyStoreUrlLimitsId.delete method.")
        logger.info("Delete keystore_url_limit.")
        from score_api_server.db import models
        limit = models.KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
            id=id
        )
        if not limit:
            return "ERROR: No such keystore_url_limit entity."
        else:
            limit.delete()
            return "OK"


class ApprovedPlugins(restful.Resource):
    def get(self):
        logger.debug("Entering ApprovedPlugins.get method.")
        logger.info("Listing all keystore_url.")

        from score_api_server.db import models
        plugins = models.ApprovedPlugins.list()
        return [u.to_dict() for u in plugins]

    @util.validate_json(
        {"type": "object",
         "properties": {
             "name": {"type": "string"},
             "source": {"type": "string"},
             "type": {"type": "string"},
         },
         "required": ["name", "source", "type"]}
    )
    def post(self, json):
        logger.debug("Entering ApprovedPlugins.post method.")
        logger.info("Update keystore_url.")
        from score_api_server.db import models
        plugin = models.ApprovedPlugins(json["name"],
                                        json["source"], json["type"])
        return plugin.to_dict()


class ApprovedPluginsFromFile(restful.Resource):
    @util.validate_json(
        {"type": "object",
         "properties": {
             "from_file": {"type": "array"},
         },
         "required": ["from_file"]}
    )
    def post(self, json):
        logger.debug("Entering ApprovedPluginsFromFile.post method.")
        logger.info("Update keystore_url.")
        from score_api_server.db import models
        for name, source, type in json['from_file']:
            models.ApprovedPlugins(name, source, type)
        return "Registered {} plugins".format(len(json['from_file']))


class ApprovedPluginsId(restful.Resource):
    def delete(self, name):
        logger.debug("Entering ApprovedPlugins.delete method.")
        logger.info("Delete keystore_url_limit.")
        from score_api_server.db import models
        plugin = models.ApprovedPlugins.find_by(name=name)
        if plugin:
            plugin.delete()
            return "Deleted"
        else:
            return "ERROR: No such plugin name entity."
