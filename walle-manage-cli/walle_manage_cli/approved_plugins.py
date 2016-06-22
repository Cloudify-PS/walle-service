from walle_manage_cli import print_dict
import yaml


def proceed_approved_plugins(client, operation, **kwargs):
    route = 'approved_plugins'
    operations = {'add': _add,
                  'delete': _delete,
                  'list': _list}
    try:
        operations[operation](client, route, **kwargs)
    except KeyError:
        client.logger.error('Unknown operation')


def _add(client, route, **kwargs):
    name = kwargs.get('name')
    source = kwargs.get('source')
    type = kwargs.get('type')
    from_file = kwargs.get('from_file')
    if from_file:
        _add_from_file(client, route, from_file)
        return
    if not(name and source and type):
        client.logger.error('Please cpecify "name, source, type"')
        return
    data = {
        'name': name,
        'source': source,
        'type': type,
    }
    print_dict(client.add(route, data))


def _add_from_file(client, route, from_file):
    route += '/from_file'
    data = {
        'from_file': _load_from_file(from_file)
    }
    print_dict(client.add(route, data))


def _delete(client, route, **kwargs):
    name = kwargs.get('name')
    if not name:
        client.logger.info('Please specify "name" parameter.')
        return
    print_dict(client.delete(route, name))


def _list(client, route, **kwargs):
    print_dict(client.list(route))


def _load_from_file(from_file):
    _plugins = []
    with open(from_file) as f:
        a_p = yaml.load(f.read())
        d_ps, w_ps = (a_p.get("deployment_plugins"),
                      a_p.get("workflow_plugins"))

        _plugins.extend(
            _register_plugin(d_ps, "deployment_plugins"))
        _plugins.extend(
            _register_plugin(w_ps, "workflow_plugins"))

        return _plugins


def _register_plugin(list_of_plugins, _type):
    _plugins = []
    for plugin in list_of_plugins:
        _name = plugin.keys()[0]
        _sources = plugin[_name]['source']
        _type = _type
        for _source in _sources:
            _plugins.append((_name, _source, _type))
    return _plugins
