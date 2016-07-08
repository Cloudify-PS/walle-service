from walle_manage_cli import print_dict


def proceed_tenants(client, operation, **kwargs):
    route = 'tenants'
    operations = {'add': _add,
                  'delete': _delete,
                  'update': _update,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):

    endpoint_url = kwargs.get('endpoint_url')
    type = kwargs.get('type')
    tenant_name = kwargs.get('tenant_name')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    description = kwargs.get('description')

    if not endpoint_url or not tenant_name:
        client.logger.info(
            'Please specify "endpoint_url"/"tenant_name" parameters.'
        )
        return
    data = {
        'endpoint_url': endpoint_url,
        'type': type,
        'tenant_name': tenant_name,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'description': description
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    id = kwargs.get('id')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    print_dict(client.delete(route, id))


def _update(client, route, **kwargs):
    id = kwargs.get('id')
    endpoint_url = kwargs.get('endpoint_url')
    type = kwargs.get('type')
    tenant_name = kwargs.get('tenant_name')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    description = kwargs.get('description')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    data = {
        'id': id,
        'endpoint_url': endpoint_url,
        'type': type,
        'tenant_name': tenant_name,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'description': description
    }
    print_dict(client.update(route, data))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
