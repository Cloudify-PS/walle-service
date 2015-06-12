from flask import g


def add_org_prefix(name):
    return "{}_{}".format(g.org_id, name)


def remove_org_prefix(obj):
    obj_copy = dict(obj)
    obj_copy['id'] = obj.id.replace("{}_".format(g.org_id), "", 1)
    obj_copy['blueprint_id'] = obj.id.replace("{}_".format(g.org_id), "", 1)
    obj_copy['deployment_id'] = obj.id.replace("{}_".format(g.org_id), "", 1)
    return obj_copy
