# Copyright (c) 2015 VMware. All rights reserved

class ListResponse(object):

    def __init__(self, items):
        self.items = items
        self.metadata = {}

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def sort(self, cmp=None, key=None, reverse=False):
        return self.items.sort(cmp, key, reverse)


class FakeBlueprint(dict):
    def __init__(self, obj_id, obj_blueprint_id, obj_deployment_id):
        self['id'] = obj_id
        self['blueprint_id'] = obj_blueprint_id
        self['deployment_id'] = obj_deployment_id

    @property
    def id(self):
        return self.get('id')

    @property
    def deployment_id(self):
        return self.get('deployment_id')

    @property
    def blueprint_id(self):
        return self.get('blueprint_id')


class FakeDeployment(dict):
    def __init__(self, data):
        self.update(data)

    @property
    def id(self):
        return self.get('id')

    @property
    def deployment_id(self):
        return self.get('deployment_id')

    @property
    def blueprint_id(self):
        return self.get('blueprint_id')
