from flask.ext import restful


class Maintenance(restful.Resource):

    def get(self):
        return {"status": "deactivated", "requested_by": "",
                "activated_at": "", "activation_requested_at": "",
                "remaining_executions": None}
