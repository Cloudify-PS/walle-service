# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    _run("""
export LC_ALL=C
sudo apt-get update 2>&1
sudo apt-get install -y postgresql postgresql-contrib 2>&1
    """)
