from score_manage_cli import print_dict


def proceed_service_urls(client, operation, **kwargs):
    route = 'service_urls'
    operations = {'add': _add,
                  'delete': _delete,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    service_url = kwargs.get('service_url')
    tenant = kwargs.get('tenant')
    info = kwargs.get('info')
    if not service_url or not tenant:
        client.logger.info('Please specify "service_url"/"tenant" parameters.')
        return
    data = {
        'tenant': tenant,
        'service_url': service_url,
        'info': info
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    id = kwargs.get('id')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    print_dict(client.delete(route, id))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
