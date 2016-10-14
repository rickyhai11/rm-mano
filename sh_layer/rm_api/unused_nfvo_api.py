'''
NFVO API: RM api functions should be implemented here
'''


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