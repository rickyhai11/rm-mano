
"""
Playnetmano_rm base exception handling.
"""
import six

from oslo_utils import excutils

from rm_mano.common.i18n import _


class RmManoException(Exception):
    """Base Playnetmano_rm Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super(RmManoException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(RmManoException, self).__init__(self.message)

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def use_fatal_exceptions(self):
        return False


class BadRequest(RmManoException):
    message = _('Bad %(resource)s request: %(msg)s')


class NotFound(RmManoException):
    pass


class Conflict(RmManoException):
    pass


class NotAuthorized(RmManoException):
    message = _("Not authorized.")


class ServiceUnavailable(RmManoException):
    message = _("The service is unavailable")


class AdminRequired(NotAuthorized):
    message = _("User does not have admin privileges: %(reason)s")


class InUse(RmManoException):
    message = _("The resource is inuse")


class InvalidConfigurationOption(RmManoException):
    message = _("An invalid value was provided for %(opt_name)s: "
                "%(opt_value)s")


class ProjectQuotaNotFound(NotFound):
    message = _("Quota for project %(project_id) doesn't exist.")


class QuotaClassNotFound(NotFound):
    message = _("Quota class %(class_name) doesn't exist.")


class ConnectionRefused(RmManoException):
    message = _("Connection to the service endpoint is refused")


class TimeOut(RmManoException):
    message = _("Timeout when connecting to OpenStack Service")


class InternalError(RmManoException):
    message = _("Error when performing operation")


class InvalidInputError(RmManoException):
    message = _("An invalid value was provided")


# recently added
############################


class OverQuota(RmManoException):
    message = _("Quota exceeded for resources: %(overs)s")


class SyncFailure(RmManoException):
    message = _("Failure when synchronizing actual resource usage from vim to nfvo")


class InvalidReservationExpiration(RmManoException):
    message = _("Invalid reservation expiration %(expire)s.")