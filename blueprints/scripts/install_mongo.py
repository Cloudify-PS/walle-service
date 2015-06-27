# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(commands):
    ctx.logger.info(commands)
    out = fabric.api.run(commands)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = [
        'export LC_ALL=C',
        'sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80' +
        ' --recv 7F0CEB10 2>&1',
        'echo "deb http://repo.mongodb.org/apt/ubuntu ' +
        '"$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee ' +
        '/etc/apt/sources.list.d/mongodb-org-3.0.list 2>&1',
        'sudo apt-get update 2>&1',
        'sudo apt-get install -y mongodb-org 2>&1',
        # enable access from any ip
        # by default access blocked to localhost
        'sudo sed "s/bind_ip = /#bind_ip = /g" -i /etc/mongod.conf',
        'sudo initctl stop mongod',
        'sudo initctl start mongod'
    ]
    _run("\n".join(script))
