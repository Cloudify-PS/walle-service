from walle_manage_cli import print_dict


def proceed_endpoint_urls(client, operation, **kwargs):
    route = 'endpoints'
    operations = {'add': _add,
                  'delete': _delete,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    endpoint_url = kwargs.get('endpoint_url')
    otype = kwargs.get('type')
    version = kwargs.get('version')
    description = kwargs.get('description')
    if not endpoint_url or not otype:
        client.logger.info('Please specify "endpoint_url"/"type" parameters.')
        return
    data = {
        'type': otype,
        'endpoint_url': endpoint_url,
        'version': version,
        'description': description
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    oid = kwargs.get('id')
    if not oid:
        client.logger.info('Please specify "id" parameter.')
        return
    print_dict(client.delete(route, oid))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
