
NOVA_QUOTA_FIELDS = ("metadata_items",
                     "vcpus",
                     "vnfs",
                     "vmemory",
                     "key_pairs",
                     "floating_ips",
                     "fixed_ips",
                     "security_groups",)

CINDER_QUOTA_FIELDS = ("volumes",
                       "snapshots",
                       "gigabytes",
                       "backups",
                       "backup_gigabytes")



NEUTRON_QUOTA_FIELDS = ("network",
                        "subnet",
                        "port",
                        "router",
                        "floatingip",
                        "security_group",
                        "security_group_rule",
                        )

QUOTA_FIELDS = (  # compute quota
                "metadata_items",
                "vcpus",
                "vnfs",
                "vmemory",
                "key_pairs",
                "floating_ips",
                "fixed_ips",
                "security_groups",
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

NOVA_QUOTA_FIELDS_AT_VIM = ("metadata_items",
                     "cores",
                     "instances",
                     "ram",
                     "key_pairs",
                     "floating_ips",
                     "fixed_ips",
                     "security_groups",)

CINDER_QUOTA_FIELDS_AT_VIM = ("volumes",
                       "snapshots",
                       "gigabytes",
                       "backups",
                       "backup_gigabytes")

NEUTRON_QUOTA_FIELDS_AT_VIM = ("network",
                        "subnet",
                        "port",
                        "router",
                        "floatingip",
                        "security_group",
                        "security_group_rule",
                        )