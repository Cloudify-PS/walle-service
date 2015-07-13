# Copyright (c) 2015 VMware. All rights reserved

from cloudify import ctx
import fabric


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    score_package_url = config.get('score_package_url', None)
    script.append("""
wget -c %s -O score-service.deb 2>&1 | tee wget_log.txt
        """ % score_package_url)
    script.append("""
sudo dpkg -i score-service.deb 2>&1
    """)
    _run("\n".join(script))
