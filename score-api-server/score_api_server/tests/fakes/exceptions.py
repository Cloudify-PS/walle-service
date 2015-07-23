# Copyright (c) 2015 VMware, Inc. All Rights Reserved.

"""Exception definitions.
"""


class Forbidden(Exception):
    """HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    http_status = 403
    message = "Forbidden"

    def __str__(self):
        formatted_string = "%s (HTTP %s)" % (self.message, self.http_status)
        return formatted_string


class Unauthorized(Exception):
    """HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = 401
    message = "Unauthorized"

    def __str__(self):
        formatted_string = "%s (HTTP %s)" % (self.message, self.http_status)
        return formatted_string
