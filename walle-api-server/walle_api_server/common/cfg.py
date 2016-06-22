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
              default=os.getenv("WALLE_HOST", "127.0.0.1")),
    PortOpt("port", default=int(os.getenv("WALLE_PORT", 5000))),
    cfg.IntOpt("workers", default=int(os.getenv("WALLE_WORKERS", 4))),
    cfg.StrOpt('db_uri', default=os.getenv(
        "WALLE_DB", 'sqlite:////tmp/score.db'
    ))
]

logging_opts = [
    cfg.StrOpt("level",
               default=os.getenv("WALLE_LOGGING_LEVEL", "DEBUG"),
               choices=("DEBUG", "INFO")),
    cfg.StrOpt("file", default=os.getenv("WALLE_LOGGING_FILE",
                                         "/var/log/score-api.log")),
    cfg.StrOpt("formatter",
               default='[%(asctime)s] - '
                       'PID: %(process)s - '
                       '%(name)s - '
                       '%(levelname)s - '
                       '{%(pathname)s:%(lineno)d} - '
                       '%(module)s - '
                       '%(funcName)s - '
                       '%(message)s')
]

rest_group = cfg.OptGroup("server", "ReST server config")
logging_group = cfg.OptGroup("logging", "Score logging config.")

CONF = cfg.CONF

CONF.register_group(rest_group)
CONF.register_group(logging_group)

CONF.register_opts(rest_opts, rest_group)
CONF.register_opts(logging_opts, logging_group)


def parse_args(argv, default_config_files=None):
    cfg.CONF(args=argv[1:],
             project='walle-server',
             version="2015.1",
             default_config_files=default_config_files)
