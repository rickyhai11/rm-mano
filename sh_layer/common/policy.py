
"""
Policy Engine For Playnetmano_rm
"""

# from oslo_concurrency import lockutils
from oslo_config import cfg
from oslo_policy import policy

from sh_layer.common import exceptions

POLICY_ENFORCER = None
CONF = cfg.CONF


# @lockutils.synchronized('policy_enforcer', 'playnetmano_rm-')
def _get_enforcer(policy_file=None, rules=None, default_rule=None):

    global POLICY_ENFORCER

    if POLICY_ENFORCER is None:
        POLICY_ENFORCER = policy.Enforcer(CONF,
                                          policy_file=policy_file,
                                          rules=rules,
                                          default_rule=default_rule)
    return POLICY_ENFORCER


def enforce(context, rule, target, do_raise=True, *args, **kwargs):

    enforcer = _get_enforcer()
    credentials = context.to_dict()
    target = target or {}
    if do_raise:
        kwargs.update(exc=exceptions.Forbidden)

    return enforcer.enforce(rule, target, credentials, do_raise,
                            *args, **kwargs)
