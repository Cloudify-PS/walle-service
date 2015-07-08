# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = [
        "sudo apt-get update",

        'sudo apt-get upgrade -y '
        '-o Dpkg::Options::="--force-confdef" '
        '-o Dpkg::Options::="--force-confold"',

        "sudo apt-get install -qy build-essential "
        "libssl-dev libffi-dev libxml2-dev",

        "sudo apt-get install -qy libxslt-dev python-dev "
        "python-pip git libpq-dev",

        "sudo apt-get install -qy postgresql-client",
        "sudo apt-get install gunicorn -qy 2>&1",
        "sudo apt-get install nginx -qy 2>&1"
    ]
    _run("\n".join(script))
