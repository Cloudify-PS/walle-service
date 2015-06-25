# Copyright (c) 2015 VMware. All rights reserved
import flask
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
sql_database = 'sqlite:///' + current_dir + 'score-test.db'

app = flask.Flask(__name__)
db = SQLAlchemy(app)
# use in memmory db
app.config['SQLALCHEMY_DATABASE_URI'] = sql_database
# migrate to last version
migrate = Migrate(app, db)
