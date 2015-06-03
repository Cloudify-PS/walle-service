# Copyright (c) 2015 VMware. All rights reserved

from score_api_server.common import cfg

CONF = cfg.CONF


def main(app, conf, cli_args):
    """CLI tool orchestrator
    :param app: flask app
    :param conf: tool conf
    :param cli_args: tool CLI arguments
    :rtype: NoneType
    """

    cfg.parse_args(cli_args)
    host, port = conf.server.host, conf.server.port
    try:
        app.run(host=host, port=port)
    except Exception as e:
        print(str(e))
