from flask import request, g

def add_org_prefix(name):
    return "{}_{}".format(g.org_id, name)

def remove_org_prefix(name):
    return name.replace("{}_".format(g.org_id), "", 1)
