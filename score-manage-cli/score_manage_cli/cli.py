# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
from score_manage_cli import (get_logger, load_config, save_config,
                              Configuration)
from login import login_to_score
from score_manage_cli import get_score_client
from approved_plugins import proceed_approved_plugins
from org_ids import proceed_org_ids
from keystore_urls import proceed_keystore_urls
from org_id_limits import proceed_org_id_limits
from keystore_url_limits import proceed_keystore_url_limits

default_operation = 'list'
LOGGER = 'logger'
CONFIG = 'config'
CLIENT = 'client'


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug
    ctx.obj[LOGGER].debug('cli')


@cli.command()
@click.pass_context
@click.argument('user')
@click.argument('password')
@click.argument('score-host')
def login(ctx, user, password, score_host):
    logger = ctx.obj[LOGGER]
    logger.debug('login')
    token = login_to_score(logger, user, password, score_host)
    if not token:
        print "Wrong credentials"
    manage = Configuration
    manage.user = user
    manage.token = token
    manage.score_host = score_host
    save_config(manage)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | delete]',
                type=click.Choice(['list', 'add', 'delete']))
@click.option('--org-id', 'org_id', metavar='<org-id>', help='Organization ID')
@click.option('--info', metavar='<info>', help='Organization info')
def org_ids(ctx, operation, org_id, info):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_score_client(config, logger)
    if not client:
        return
    proceed_org_ids(client, operation, org_id=org_id, info=info)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | update | delete]',
                type=click.Choice(['list', 'add', 'update', 'delete']))
@click.option('--org-id')
@click.option('--cloudify-host')
@click.option('--cloudify-port')
@click.option('--deployment-limits')
@click.option('--id')
@click.option('--number-of-deployments')
def org_id_limits(ctx, operation, org_id, cloudify_host, cloudify_port,
                  deployment_limits, id, number_of_deployments):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_score_client(config, logger)
    if not client:
        return
    proceed_org_id_limits(client, operation, org_id=org_id,
                          cloudify_host=cloudify_host,
                          cloudify_port=cloudify_port,
                          deployment_limits=deployment_limits,
                          id=id, number_of_deployments=number_of_deployments)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | delete]',
                type=click.Choice(['list', 'add', 'delete']))
@click.option('--name')
@click.option('--source')
@click.option('--type')
@click.option('--from-file')
def approved_plugins(ctx, operation, name, source, type, from_file):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_score_client(config, logger)
    if not client:
        return
    proceed_approved_plugins(client, operation, name=name,
                             source=source,
                             type=type, from_file=from_file)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | delete]',
                type=click.Choice(['list', 'add', 'delete']))
@click.option('--keystore-url')
@click.option('--info', metavar='<info>', help='Organization info')
def keystore_urls(ctx, operation, keystore_url, info):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_score_client(config, logger)
    if not client:
        return
    proceed_keystore_urls(client, operation, keystore_url=keystore_url,
                          info=info)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | update | delete]',
                type=click.Choice(['list', 'add', 'update', 'delete']))
@click.option('--keystore-url')
@click.option('--cloudify-host')
@click.option('--cloudify-port')
@click.option('--deployment-limits')
@click.option('--id')
@click.option('--number-of-deployments')
def keystore_url_limits(ctx, operation, keystore_url, cloudify_host,
                        cloudify_port, deployment_limits, id,
                        number_of_deployments):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_score_client(config, logger)
    if not client:
        return
    proceed_keystore_url_limits(client, operation,
                                keystore_url=keystore_url,
                                cloudify_host=cloudify_host,
                                cloudify_port=cloudify_port,
                                deployment_limits=deployment_limits,
                                id=id,
                                number_of_deployments=number_of_deployments)


def _get_score_client(config, logger):
    if not config:
        click.echo('Empty config')
        return None
    return get_score_client(config, logger)


def main():
    logger = get_logger()
    cli(obj={LOGGER: logger})


if __name__ == '__main__':
    main()
