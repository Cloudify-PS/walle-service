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
from walle_manage_cli import (get_logger, load_config, save_config,
                              Configuration)
from login import login_to_walle
from walle_manage_cli import get_walle_client
from approved_plugins import proceed_approved_plugins
from endpoint_urls import proceed_endpoint_urls
from tenants import proceed_tenants
from limits import proceed_limits

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
@click.argument('walle-host')
@click.argument('verify', default=True)
def login(ctx, user, password, walle_host, verify):
    logger = ctx.obj[LOGGER]
    logger.debug('login')
    token = login_to_walle(logger, user, password, walle_host, verify)
    if not token:
        logger.error("Wrong credentials")
    manage = Configuration
    manage.user = user
    manage.token = token
    manage.walle_host = walle_host
    manage.verify = verify
    save_config(manage)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | delete]',
                type=click.Choice(['list', 'add', 'delete']))
@click.option('--name')
@click.option('--source')
@click.option('--type')
@click.option('--from-file')
@click.option('--id')
def approved_plugins(ctx, operation, name, source, type, from_file,
                     plugin_id):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_walle_client(config, logger)
    if not client:
        return
    proceed_approved_plugins(client, operation, name=name,
                             source=source, type=type,
                             from_file=from_file, plugin_id=plugin_id)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | delete]',
                type=click.Choice(['list', 'add', 'delete']))
@click.option('--endpoint-url', metavar='<endpoint_url>', help='Endpoint url')
@click.option('--type', metavar='<type>', help='Endpoint type')
@click.option('--version', metavar='<version>', help='Endpoint version')
@click.option('--description', metavar='<description>', help='Organization info')
@click.option('--id', metavar='<id>', help='Endpoint id')
def endpoint_urls(ctx, operation, endpoint_url, type, version, description, id):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_walle_client(config, logger)
    if not client:
        return
    proceed_endpoint_urls(client, operation, endpoint_url=endpoint_url, type=type, version=version, description=description, id=id)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | update | delete]',
                type=click.Choice(['list', 'add', 'update', 'delete']))
@click.option('--endpoint-url')
@click.option('--type')
@click.option('--tenant-name')
@click.option('--cloudify-host')
@click.option('--cloudify-port')
@click.option('--description')
@click.option('--id')
def tenants(ctx, operation, endpoint_url, type, tenant_name,
            cloudify_host, cloudify_port, description, id):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_walle_client(config, logger)
    if not client:
        return
    proceed_tenants(client, operation, endpoint_url=endpoint_url,
                    type=type, tenant_name=tenant_name,
                    cloudify_host=cloudify_host, cloudify_port=cloudify_port,
                    description=description, id=id)


@cli.command()
@click.pass_context
@click.argument('operation', default=default_operation,
                metavar='[list | add | update | delete]',
                type=click.Choice(['list', 'add', 'update', 'delete']))
@click.option('--endpoint-url')
@click.option('--type')
@click.option('--tenant')
@click.option('--hard')
@click.option('--soft')
@click.option('--limit-type')
@click.option('--id')
def limits(ctx, operation, endpoint_url, type, tenant, hard, soft, limit_type, id):
    logger = ctx.obj[LOGGER]
    logger.debug('manage')
    config = load_config(logger)
    client = _get_walle_client(config, logger)
    if not client:
        return
    proceed_limits(client, operation, endpoint_url=endpoint_url,
        type=type, tenant=tenant, hard=hard, soft=soft,
        limit_type=limit_type, id=id)


def _get_walle_client(config, logger):
    if not config:
        click.echo('Empty config')
        return None
    return get_walle_client(config, logger)


def main():
    logger = get_logger()
    cli(obj={LOGGER: logger})


if __name__ == '__main__':
    main()
