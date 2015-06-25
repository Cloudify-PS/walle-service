# Copyright (c) 2015 VMware. All rights reserved

import os
from oslo_config import cfg


class PortOpt(cfg.Opt):
    def __init__(self, name, **kwargs):
        super(PortOpt, self).__init__(
            name,
            type=cfg.types.Integer(min=80, max=65535),
            **kwargs)

rest_opts = [
    cfg.IPOpt("host", version=4,
              default=os.getenv("SCORE_HOST", "127.0.0.1")),
    PortOpt("port", default=int(os.getenv("SCORE_PORT", 5000))),
    cfg.IntOpt("workers", default=int(os.getenv("SCORE_WORKERS", 4))),
    cfg.StrOpt('db_uri', default=os.getenv(
        "SCORE_DB", 'sqlite:////tmp/score.db'
    ))
]

cloudify_opts = [
    cfg.IPOpt("host", version=4,
              default=os.getenv("CFY_MANAGER_HOST", "127.0.0.1")),
    PortOpt("port", default=int(os.getenv("CFY_MANAGER_PORT", 80)))
]

rest_group = cfg.OptGroup("server", "ReST server config")
cloudify_group = cfg.OptGroup("cloudify", "Cloudify connection config")

CONF = cfg.CONF

CONF.register_group(rest_group)
CONF.register_group(cloudify_group)

CONF.register_opts(rest_opts, rest_group)
CONF.register_opts(cloudify_opts, cloudify_group)


def parse_args(argv, default_config_files=None):
    cfg.CONF(args=argv[1:],
             project='score-server',
             version="2015.1",
             default_config_files=default_config_files)
