# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""I totally stole most of this from melange, thx guys!!!"""

import logging
from reddwarf.openstack.common import exception as openstack_exception
from webob import exc


ClientConnectionError = openstack_exception.ClientConnectionError
ProcessExecutionError = openstack_exception.ProcessExecutionError
DatabaseMigrationError = openstack_exception.DatabaseMigrationError
LOG = logging.getLogger(__name__)
wrap_exception = openstack_exception.wrap_exception


class ReddwarfError(openstack_exception.OpenstackException):
    """Base exception that all custom reddwarf app exceptions inherit from."""
    internal_message = None

    def __init__(self, message=None, **kwargs):
        if message is not None:
            self.message = message
        if self.internal_message is not None:
            try:
                LOG.error(self.internal_message % kwargs)
            except Exception:
                LOG.error(self.internal_message)
        super(ReddwarfError, self).__init__(**kwargs)


class DBConstraintError(ReddwarfError):

    message = _("Failed to save %(model_name)s because: %(error)s")


class InvalidRPCConnectionReuse(ReddwarfError):

    message = _("Invalid RPC Connection Reuse")


class NotFound(ReddwarfError):

    message = _("Resource %(uuid)s cannot be found")


class ComputeInstanceNotFound(NotFound):

    internal_message = _("Cannot find compute instance %(server_id)s for "
                         "instance %(instance_id)s.")

    message = _("Resource %(instance_id)s can not be retrieved.")


class GuestError(ReddwarfError):

    message = _("An error occurred communicating with the guest: "
                "%(original_message).")


class BadRequest(ReddwarfError):

    message = _("The server could not comply with the request since it is "
                "either malformed or otherwise incorrect.")


class MissingKey(BadRequest):

    message = _("Required element/key - %(key)s was not specified")


class UnprocessableEntity(ReddwarfError):

    message = _("Unable to process the contained request")


class VolumeAttachmentsNotFound(NotFound):

    message = _("Cannot find the volumes attached to compute "
                "instance %(server_id)")
