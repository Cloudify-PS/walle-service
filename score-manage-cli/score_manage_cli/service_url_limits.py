from score_manage_cli import print_dict


def proceed_service_url_limits(client, operation, **kwargs):
    route = 'service_url_limits'
    operations = {'add': _add,
                  'delete': _delete,
                  'update': _update,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    service_url = kwargs.get('service_url')
    tenant = kwargs.get('tenant')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    if not service_url or not tenant:
        client.logger.info(
            'Please specify "service_url"/"service" parameters.'
        )
        return
    data = {
        'service_url': service_url,
        'tenant': tenant,
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
    service_url = kwargs.get('service_url')
    tenant = kwargs.get('tenant')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    number_of_deployments = kwargs.get('number_of_deployments')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    data = {
        'id': id,
        'service_url': service_url,
        'tenant': tenant,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'deployment_limits': deployment_limits,
        'number_of_deployments': number_of_deployments
    }
    print_dict(client.update(route, data))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
