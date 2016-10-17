
NOVA_QUOTA_FIELDS = ("metadata_items",
                     "vcpus",
                     "vnfs",
                     "vmemory",
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
#                        "gigabytes")
#  gigabytes: t_disk_ephemeral= compute_summary['total_disk']+ compute_summary['total_ephemeral']


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

QUOTA_FIELDS = (  # compute quota
                "metadata_items",
                "vcpus",
                "vnfs",
                "vmemory",
                "key_pairs",
                "floating_ips",
                "fixed_ips",
                # cinder quota
                "volumes",
                "snapshots",
                "gigabytes",
                "backups",
                "backup_gigabytes",
                # neutron quota
                "network",
                "subnet",
                "port",
                "router",
                "floatingip",
                "security_group",
                "security_group_rule")
