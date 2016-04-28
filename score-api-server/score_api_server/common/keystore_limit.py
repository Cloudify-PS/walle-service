# Copyright (c) 2016 VMware. All rights reserved
# Copyright (c) 2016 GigaSpaces Technologies 2016, All Rights Reserved.


def check_keystore_url(keystore_url):
    """Checks Keystore url for existence."""
    from score_api_server.db.models import AllowedKeyStoreUrl
    keystore_url = AllowedKeyStoreUrl.find_by(keystore_url=keystore_url)
    if keystore_url:
        return keystore_url


def get_keystore_url_limits(keystore_url):
    """Gets Cloudify credentials and current Keystore url limits."""
    from score_api_server.db.models import (
        KeyStoreUrlToCloudifyAssociationWithLimits)
    return KeyStoreUrlToCloudifyAssociationWithLimits.find_by(
        keystore_url=keystore_url)
