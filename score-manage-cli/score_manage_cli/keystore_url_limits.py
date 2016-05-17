from score_manage_cli import print_dict


def proceed_keystore_url_limits(client, operation, **kwargs):
    route = 'keystore_url_limits'
    operations = {'add': _add,
                  'delete': _delete,
                  'update': _update,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    keystore_url = kwargs.get('keystore_url')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    if not keystore_url:
        client.logger.info('Please specify "org_id" parameter.')
        return
    data = {
        'keystore_url': keystore_url,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'deployment_limits': deployment_limits
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
    keystore_url = kwargs.get('keystore_url')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    number_of_deployments = kwargs.get('number_of_deployments')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    data = {
        'id': id,
        'keystore_url': keystore_url,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'deployment_limits': deployment_limits,
        'number_of_deployments': number_of_deployments
    }
    print_dict(client.update(route, data))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
