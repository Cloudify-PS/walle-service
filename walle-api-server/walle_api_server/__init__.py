# Copyright (c) 2015 VMware. All rights reserved
import pkg_resources


def get_version():
    return pkg_resources.get_distribution("walle-service").version
