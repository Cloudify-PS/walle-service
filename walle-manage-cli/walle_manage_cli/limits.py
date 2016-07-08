from walle_manage_cli import print_dict


def proceed_limits(client, operation, **kwargs):
    route = 'limits'
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
    tenant_name = kwargs.get('tenant')
    hard = kwargs.get('hard')
    soft = kwargs.get('soft')
    limit_type = kwargs.get('limit_type')

    if not endpoint_url or not tenant_name:
        client.logger.info(
            'Please specify "endpoint_url"/"tenant_name" parameters.'
        )
        return

    data = {
        'endpoint_url': endpoint_url,
        'type': type,
        'tenant_name': tenant_name,
        'soft': soft,
        'hard': hard,
        'limit_type': limit_type
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
    hard = kwargs.get('hard')
    soft = kwargs.get('soft')
    limit_type = kwargs.get('limit_type')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    data = {
        'id': id,
        'soft': soft,
        'hard': hard,
        'limit_type': limit_type
    }
    print_dict(client.update(route, data))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
