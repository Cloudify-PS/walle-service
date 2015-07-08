# Copyright (c) 2015 VMware. All rights reserved


class FakeBlueprint(object):
    def __init__(self, obj_id, obj_blueprint_id, obj_deployment_id):
        self.id = obj_id
        self.blueprint_id = obj_blueprint_id
        self.deployment_id = obj_deployment_id

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
