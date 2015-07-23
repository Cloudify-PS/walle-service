# Copyright (c) 2015 VMware. All rights reserved

import uuid
import datetime

from score_api_server.cli import app
from score_api_server.common import util

db = app.db
logger = util.setup_logging(__name__)


def utcnow():
    return datetime.datetime.utcnow()


class BaseDatabaseModel(object):

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = utcnow()
        self.updated_at = utcnow()
        self.deleted_at = utcnow()

    def save(self):
        try:
            app.db.session.add(self)
            app.db.session.commit()
        except Exception as e:
            logger.error(str(e))
            raise e

    def delete(self):
        try:
            app.db.session.delete(self)
            app.db.session.commit()
        except Exception as e:
            logger.error(str(e))
            raise e

    def update(self, **values):
        try:
            for key in values:
                if hasattr(self, key):
                    setattr(self, key, values[key])
            self.updated_at = utcnow()
            self.save()
            return self.find_by(id=self.id)
        except Exception as e:
            logger.error(str(e))
            raise e

    @classmethod
    def list(cls):
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(str(e))
            raise e

    @classmethod
    def find_by(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        return obj if obj else None

    def to_dict(self):
        return self.__dict__
