from score_manage_cli import print_dict


def proceed_org_ids(client, operation, **kwargs):
    route = 'org_ids'
    operations = {'add': _add,
                  'delete': _delete,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    org_id = kwargs['org_id']
    if not org_id:
        client.logger.info('Please specify "org_id" parameter.')
        return
    data = {
        'org_id': org_id,
        'info': kwargs.get('info')
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    org_id = kwargs.get('org_id')
    if not org_id:
        client.logger.info('Please specify "org_id" parameter.')
        return
    print_dict(client.delete(route, org_id))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
