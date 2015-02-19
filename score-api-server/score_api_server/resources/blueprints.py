from flask.ext import restful

class Blueprints(restful.Resource):
    def get(self, id=None):
        print 'get-blueprints'
        return {'result': 'ok'}
    def post(self, id=None):
        pass