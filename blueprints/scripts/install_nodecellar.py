# Copyright (c) 2015 VMware. All rights reserved

from cloudify import ctx
import fabric

NODE_CELLAR_ARCHIVE = (
    "https://github.com/cloudify-cosmo/" +
    "nodecellar/archive/master.tar.gz"
)


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def _generate_service(mongodb_host):
    return [
        "description 'nodecellar service'",
        "# used to be: start on startup",
        "# until we found some mounts were not ready yet while booting:",
        "start on started mountall",
        "stop on shutdown",
        "# Automatically Respawn:",
        "respawn",
        "respawn limit 99 5",
        "script",
        "    export LC_ALL=C",
        "    export NODECELLAR_PORT=8080",
        "    export MONGO_PORT=27017",
        "    export MONGO_HOST=" + mongodb_host,
        "    exec LC_ALL=C /usr/bin/nodejs " +
        "${HOME}/nodecellar-master/server.js &> /tmp/log",
        "end script"
    ]


def install(config):
    script = []
    script.append("""
export LC_ALL=C
wget -c -v """ + NODE_CELLAR_ARCHIVE + """ 2>&1
tar -xvf master.tar.gz
cd nodecellar-master && npm update
    """)
    # create service config
    service = _generate_service(config.get("mongo", "localhost"))
    script.append("rm -f ${HOME}/nodecellar.conf")
    for service_str in service:
        script.append(
            'echo "' + service_str + '" >> ${HOME}/nodecellar.conf'
        )
    # create init file
    script.append("""
sudo cp ${HOME}/nodecellar.conf /etc/init/nodecellar.conf
sudo chown root:root /etc/init/nodecellar.conf
# run service
sudo initctl start nodecellar
    """)
    _run("\n".join(script))
