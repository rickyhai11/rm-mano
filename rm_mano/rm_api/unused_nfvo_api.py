'''
NFVO API: RM api functions should be implemented here
'''

import collections
import pecan
from pecan import expose
from pecan import request

import restcomm
import six

from rm_mano.common import exceptions
from rm_mano.common.i18n import _
from rm_mano.common import utils
from rm_mano.db.sqlalchemy import api as db_api


class QuotaManagerController(object):

    def __init__(self, *args, **kwargs):
        super(QuotaManagerController, self).__init__(*args, **kwargs)

    @expose(generic=True, template='json')
    def index(self):
        # Route the request to specific methods with parameters
        pass

    @index.when(method='GET', template='json')
    def get(self, project_id, action=None):
        quota = collections.defaultdict(dict)
        context = restcomm.extract_context_from_environ()
        result = collections.defaultdict(dict)
        try:
            if project_id == 'defaults':
                # Get default quota limits from conf file
                result = self._get_defaults(context,
                                            CONF.playnetmano_rm_global_limit)
            else:
                if action and action != 'detail':
                    pecan.abort(404, _('Invalid request URL'))
                elif action == 'detail':
                    # Get the current quota usages for a project
                    result = self.rpc_client.get_total_usage_for_tenant(
                        context, project_id)
                else:
                    # Get quota limits for all the resources for a project
                    result = db_api.quota_get_all_by_project(
                        context, project_id)
            quota['quota_set'] = result
            return quota
        # Could be raised by get total usage call
        except exceptions.InternalError:
            pecan.abort(400, _('Error while requesting usage'))

    # Tries to update quota limits for a project, if it fails then
    # it creates a new entry in DB for that project
    @index.when(method='PUT', template='json')
    def put(self, project_id, action=None):
        quota = collections.defaultdict(dict)
        quota[project_id] = collections.defaultdict(dict)
        context = restcomm.extract_context_from_environ()
        if action and action != 'sync':
            pecan.abort(404, 'Invalid action, only sync is allowed')
        elif action == 'sync':
            return self.sync(project_id, context)
        if not context.is_admin:
            pecan.abort(403, _('Admin required'))
        if not request.body:
            pecan.abort(400, _('Body required'))
        payload = eval(request.body)
        payload = payload.get('quota_set')
        if not payload:
            pecan.abort(400, _('quota_set in body is required'))
        try:
            utils.validate_quota_limits(payload)
            for resource, limit in payload.iteritems():
                try:
                    # Update quota limit in DB
                    result = db_api.quota_update(
                        context,
                        project_id=project_id,
                        resource=resource,
                        limit=limit)
                except exceptions.ProjectQuotaNotFound:
                    # If update fails due to project/quota not found
                    # then create the quota limit
                    result = db_api.quota_create(
                        context,
                        project_id=project_id,
                        resource=resource,
                        limit=limit)
                quota[project_id][result.resource] = result.hard_limit
            return quota
        except exceptions.InvalidInputError:
            pecan.abort(400, _('Invalid input for quota limits'))

    @index.when(method='delete', template='json')
    def delete(self, project_id):
        context = restcomm.extract_context_from_environ()
        if not context.is_admin:
            pecan.abort(403, _('Admin required'))

        try:
            if request.body:
                # Delete the mentioned quota limit for the project
                payload = eval(request.body)
                payload = payload.get('quota_set')
                if not payload:
                    pecan.abort(400, _('quota_set in body required'))
                utils.validate_quota_limits(payload)
                for resource in payload:
                    db_api.quota_destroy(context, project_id, resource)
                return {'Deleted quota limits': payload}
            else:
                # Delete all quota limits for the project
                db_api.quota_destroy_all(context, project_id)
                return "Deleted all quota limits for the given project"
        except exceptions.ProjectQuotaNotFound:
            pecan.abort(404, _('Project quota not found'))
        except exceptions.InvalidInputError:
            pecan.abort(400, _('Invalid input for quota'))

    # Private method called by put method for on demand quota sync
    def sync(self, project_id, context):
        if pecan.request.method != 'PUT':
            pecan.abort(405, _('Bad method. Use PUT instead'))
        if not context.is_admin:
            pecan.abort(403, _('Admin required'))

        self.rpc_client.quota_sync_for_project(
            context, project_id)
        return 'triggered quota sync for ' + project_id

    @staticmethod
    def _get_defaults(context, config_defaults):
        """Get default quota values.

        If the default class is defined, use the values defined
        in the class, otherwise use the values from the config.

        :param context:
        :param config_defaults:
        :return:
        """
        quotas = {}
        default_quotas = {}
        if CONF.use_default_quota_class:
            default_quotas = db_api.quota_class_get_default(context)

        for resource, default in six.iteritems(config_defaults):
            # get rid of the 'quota_' prefix
            resource_name = resource[6:]
            if default_quotas:
                if resource_name not in default_quotas:
                    versionutils.report_deprecated_feature(LOG, _(
                        "Default quota for resource: %(res)s is set "
                        "by the default quota flag: quota_%(res)s, "
                        "it is now deprecated. Please use the "
                        "default quota class for default "
                        "quota.") % {'res': resource_name})
            quotas[resource_name] = default_quotas.get(resource_name, default)

        return quotas


# refer codes
# refer to this function that handles a lot of type of api requests
# when implementing rm api function
def _quota_action(self, action, **kw):

    context = t_context.extract_context_from_environ()
    context.project_id = self.owner_tenant_id
    target_tenant_id = self.target_tenant_id
    target_user_id = request.params.get('user_id', None)
    if target_user_id:
        target_user_id.strip()

    qs = quota.QuotaSetOperation(target_tenant_id,
                                 target_user_id)
    quotas = {}
    try:
        if action == 'put':
            quotas = qs.update(context, **kw)
        elif action == 'delete':
            qs.delete(context)
            response.status = 202
            return
        elif action == 'defaults':
            quotas = qs.show_default_quota(context)
        elif action == 'detail':
            quotas = qs.show_detail_quota(context, show_usage=True)

            # remove the allocated field which is not visible in Nova
            for k, v in quotas['quota_set'].iteritems():
                if k != 'id':
                    v.pop('allocated', None)

        elif action == 'quota-show':
            quotas = qs.show_detail_quota(context, show_usage=False)
        else:
            return Response('Resource not found', 404)
    except t_exceptions.NotFound as e:
        msg = str(e)
        LOG.exception(msg=msg)
        return Response(msg, 404)
    except (t_exceptions.AdminRequired,
            t_exceptions.NotAuthorized,
            t_exceptions.HTTPForbiddenError) as e:
        msg = str(e)
        LOG.exception(msg=msg)
        return Response(msg, 403)
    except Exception as e:
        msg = str(e)
        LOG.exception(msg=msg)
        return Response(msg, 400)

    return {'quota_set': self._build_visible_quota(quotas['quota_set'])}