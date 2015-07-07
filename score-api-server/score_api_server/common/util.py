import copy

from flask import g


def add_org_prefix(name):
    return "{}_{}".format(g.org_id, name)


def remove_org_prefix(obj):
    obj_copy = copy.deepcopy(obj)
    if isinstance(obj, dict):
        replaced_id = obj['id'].replace("{}_".format(g.org_id), "", 1)
    else:
        replaced_id = obj.id.replace("{}_".format(g.org_id), "", 1)
    obj_copy['id'] = replaced_id
    obj_copy['blueprint_id'] = replaced_id
    obj_copy['deployment_id'] = replaced_id
    return obj_copy
