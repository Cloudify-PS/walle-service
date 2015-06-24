# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def _generate_service(server_host, cloudify_host):
    return [
        "description 'score service'",
        "# used to be: start on startup",
        "# until we found some mounts were not ready yet while booting:",
        "start on started mountall",
        "stop on shutdown",
        "# Automatically Respawn:",
        "respawn",
        "respawn limit 99 5",
        "script",
        "    export SCORE_HOST=%s" % server_host,
        "    export SCORE_PORT=8001",
        "    export SCORE_WORKERS=4",
        "    export CFY_MANAGER_HOST=%s" % cloudify_host,
        "    export CFY_MANAGER_PORT=80",
        "    exec /usr/bin/gunicorn -w 4 -b %s:8001 " +
        "score_api_server.cli.app:app 2>&1 > /tmp/log" % server_host,

        "end script"
    ]


def configure(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    server_host = config.get("score_public_ip", "0.0.0.0")
    cloudify_host = config.get("manager_public_ip", "localhost")

    # create service config
    service = _generate_service(server_host, cloudify_host)
    ctx.logger.info(service)
    script.append("rm -f /home/ubuntu/score_api_server.conf")
    for service_str in service:
        script.append('echo "' + service_str +
                      '" >> /home/ubuntu/score_api_server.conf')
    # create init file
    script.append("""
sudo cp /home/ubuntu/score_api_server.conf /etc/init/score_api_server.conf
sudo chown root:root /etc/init/score_api_server.conf
# run service
sudo initctl start score_api_server
    """)
    # configure nginx service
    script.append("""
sudo rm /etc/nginx/sites-enabled/*
sudo cp /home/ubuntu/score-service/etc/nginx/vca_io /etc/nginx/sites-enabled
sudo cp /home/ubuntu/score-service/etc/keys/* /etc/nginx/
sudo service nginx restart
    """)
    _run("\n".join(script))
