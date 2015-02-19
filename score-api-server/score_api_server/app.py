from flask import Flask
from flask.ext import restful

from score_api_server.resources.blueprints import Blueprints

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(Blueprints, '/blueprints', '/blueprints')

if __name__ == '__main__':
    app.run(debug=True)
