
"""
Playnetmano_rm base exception handling.
"""
import six

from oslo_utils import excutils

from sh_layer.common.i18n import _


class Playnetmano_rmException(Exception):
    """Base Playnetmano_rm Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super(Playnetmano_rmException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(Playnetmano_rmException, self).__init__(self.message)

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def use_fatal_exceptions(self):
        return False


class BadRequest(Playnetmano_rmException):
    message = _('Bad %(resource)s request: %(msg)s')


class NotFound(Playnetmano_rmException):
    pass


class Conflict(Playnetmano_rmException):
    pass


class NotAuthorized(Playnetmano_rmException):
    message = _("Not authorized.")


class ServiceUnavailable(Playnetmano_rmException):
    message = _("The service is unavailable")


class AdminRequired(NotAuthorized):
    message = _("User does not have admin privileges: %(reason)s")


class InUse(Playnetmano_rmException):
    message = _("The resource is inuse")


class InvalidConfigurationOption(Playnetmano_rmException):
    message = _("An invalid value was provided for %(opt_name)s: "
                "%(opt_value)s")


class ProjectQuotaNotFound(NotFound):
    message = _("Quota for project %(project_id) doesn't exist.")


class QuotaClassNotFound(NotFound):
    message = _("Quota class %(class_name) doesn't exist.")


class ConnectionRefused(Playnetmano_rmException):
    message = _("Connection to the service endpoint is refused")


class TimeOut(Playnetmano_rmException):
    message = _("Timeout when connecting to OpenStack Service")


class InternalError(Playnetmano_rmException):
    message = _("Error when performing operation")


class InvalidInputError(Playnetmano_rmException):
    message = _("An invalid value was provided")

####################################################################
# New adding exceptions
###################################################################

class OverQuota(Playnetmano_rmException):
    message = _("Quota exceeded for resources: %(overs)s")