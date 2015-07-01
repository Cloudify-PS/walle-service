# Copyright (c) 2015 VMware. All rights reserved

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
