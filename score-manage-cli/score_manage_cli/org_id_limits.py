from score_manage_cli import print_dict


def proceed_org_id_limits(client, operation, **kwargs):
    route = 'org_id_limits'
    operations = {'add': _add,
                  'delete': _delete,
                  'update': _update,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    org_id = kwargs.get('org_id')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    if not org_id or not cloudify_host or not cloudify_port or not deployment_limits:
        client.logger.info('Please specify: org-id, cloudify-host, cloudify-port, deployment-limits.')
        return
    data = {
        'org_id': org_id,
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
    org_id = kwargs.get('org_id')
    cloudify_host = kwargs.get('cloudify_host')
    cloudify_port = kwargs.get('cloudify_port')
    deployment_limits = kwargs.get('deployment_limits')
    number_of_deployments = kwargs.get('number_of_deployments')
    if not id:
        client.logger.info('Please specify "id" parameter.')
        return
    data = {
        'id': id,
        'org_id': org_id,
        'cloudify_host': cloudify_host,
        'cloudify_port': cloudify_port,
        'deployment_limits': deployment_limits,
        'number_of_deployments': number_of_deployments
    }
    print_dict(client.update(route, data))


def _list(client, route, **kwargs):
    print_dict(client.list(route))
