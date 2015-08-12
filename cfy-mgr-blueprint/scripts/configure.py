import tempfile
import json

import fabric

import vcloud_plugin_common
from cloudify import ctx


def configure(vcloud_config):
    """
        copy configuration to managment host,
        install docker
        and save current context to .cloudify/context
        For now - we have saved only managment network name
    """
    _copy_vsphere_configuration_to_manager(vcloud_config)
    _install_docker()


def _copy_vsphere_configuration_to_manager(vcloud_config):
    """
        Copy current config to remote node
    """
    tmp = tempfile.mktemp()
    with open(tmp, 'w') as f:
        json.dump(vcloud_config, f)
    fabric.api.put(tmp,
                   vcloud_plugin_common.Config.VCLOUD_CONFIG_PATH_DEFAULT)


def _install_docker():
    """
        install docker from https://get.docker.com/
    """
    distro = fabric.api.run(
        'python -c "import platform; print platform.dist()[0]"')
    kernel_version = fabric.api.run(
        'python -c "import platform; print platform.release()"')
    if kernel_version.startswith("3.13") and 'Ubuntu' in distro:
        fabric.api.run("wget -qO- https://get.docker.com/ | sudo sh")

