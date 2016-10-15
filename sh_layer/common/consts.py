
NOVA_QUOTA_FIELDS = ("metadata_items",
                     "cores",
                     "instances",
                     "ram",
                     "key_pairs",
                     "floating_ips",
                     "fixed_ips",
                     "security_groups",)
# NOVA_QUOTA_FIELDS = ("vcpus",
#                      "vnfs",
#                      "memory",
#                      "floatingip_default")

CINDER_QUOTA_FIELDS = ("volumes",
                       "snapshots",
                       "gigabytes",
                       "backups",
                       "backup_gigabytes")

# CINDER_QUOTA_FIELDS = ("volumes",
#                        "snapshots",
#                        "gigabytes") # t_disk_ephemeral= compute_summary['total_disk']+ compute_summary['total_ephemeral']


NEUTRON_QUOTA_FIELDS = ("network",
                        "subnet",
                        "port",
                        "router",
                        "floatingip",
                        "security_group",
                        "security_group_rule",
                        )
# NEUTRON_QUOTA_FIELDS = ("network",
#                         "subnet",
#                         "port",
#                         "router",
#                         "floatingip")

QUOTA_FIELDS = ("vcpus",
                "vnfs",
                "memory",
                "floatingip_default",  # in case neutron is disable and nova network is used
                                       # TODO(ricky) check if neutron is disabled or enabled
                "volumes",
                "snapshots",
                "gigabytes",
                "network",
                "subnet",
                "port",
                "router",
                "floatingip")
