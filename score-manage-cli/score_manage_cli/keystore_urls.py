from score_manage_cli import print_dict


def proceed_keystore_urls(client, operation, **kwargs):
    route = 'keystore_urls'
    operations = {'add': _add,
                  'delete': _delete,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    keystore_url = kwargs.get('keystore_url')
    info = kwargs.get('info')
    if not keystore_url:
        client.logger.info('Please specify "keystore_url" parameter.')
        return
    data = {
        'keystore_url': keystore_url,
        'info': info
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    keystore_url = kwargs.get('keystore_url')
    if not keystore_url:
        client.logger.info('Please specify "keystore_url" parameter.')
        return
    print_dict(client.delete(route, keystore_url))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
