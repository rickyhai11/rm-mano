-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 116.89.184.43    Database: mano_db
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `flavors_rm`
--

DROP TABLE IF EXISTS `flavors_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavors_rm` (
  `flavor_id` varchar(20) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `ram` int(30) DEFAULT NULL,
  `disk` int(30) DEFAULT NULL,
  `vcpu` int(30) DEFAULT NULL,
  PRIMARY KEY (`flavor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flavour_info_rm`
--

DROP TABLE IF EXISTS `flavour_info_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavour_info_rm` (
  `uuid` varchar(36) NOT NULL COMMENT 'Flavour ID',
  `vMemory` int(10) NOT NULL DEFAULT '0' COMMENT 'MB',
  `numVirCpu` int(10) NOT NULL DEFAULT '0',
  `storageSize` int(10) NOT NULL DEFAULT '0' COMMENT 'GB',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `images_rm`
--

DROP TABLE IF EXISTS `images_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images_rm` (
  `image_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `image_status` enum('ACTIVE','DOWN','BUILD','ERROR') DEFAULT 'BUILD',
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `networks_details_rm`
--

DROP TABLE IF EXISTS `networks_details_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networks_details_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `network_name` varchar(200) NOT NULL,
  `network_id` varchar(200) NOT NULL,
  `network_status` enum('ACTIVE','DOWN','BUILD','ERROR') NOT NULL DEFAULT 'BUILD',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nfvo_ns_rm`
--

DROP TABLE IF EXISTS `nfvo_ns_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nfvo_ns_rm` (
  `ns_id` varchar(100) NOT NULL,
  `ns_name` varchar(100) DEFAULT NULL,
  `user_id` varchar(100) NOT NULL,
  `tenant_id` varchar(100) NOT NULL,
  `status` enum('ACTIVE','DOWN','BUILD','ERROR') DEFAULT NULL,
  PRIMARY KEY (`ns_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `tenant_id_UNIQUE` (`tenant_id`),
  UNIQUE KEY `ns_name_UNIQUE` (`ns_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nfvo_projects`
--

DROP TABLE IF EXISTS `nfvo_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nfvo_projects` (
  `uuid` varchar(36) NOT NULL,
  `userId` varchar(36) NOT NULL,
  `projectId` varchar(36) NOT NULL,
  `status` varchar(36) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='project_id defined by the user';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_rm`
--

DROP TABLE IF EXISTS `project_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_rm` (
  `project_name` varchar(100) NOT NULL,
  `project_id` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `tenant_name_UNIQUE` (`project_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quota_rm`
--

DROP TABLE IF EXISTS `quota_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quota_rm` (
  `uuid` varchar(36) NOT NULL,
  `project_id` varchar(36) NOT NULL,
  `resource` varchar(36) NOT NULL,
  `hard_limit` int(20) NOT NULL DEFAULT '0',
  `allocated` int(20) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='quotas for all resources';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `reservation_id` int(36) NOT NULL AUTO_INCREMENT,
  `usage_id` varchar(36) NOT NULL,
  `label` varchar(100) DEFAULT 'Default',
  `region_id` varchar(100) NOT NULL,
  `user_id` varchar(100) DEFAULT 'admin',
  `project_id` varchar(100) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `flavor_id` varchar(36) NOT NULL,
  `image_id` varchar(100) NOT NULL,
  `ns_id` varchar(100) DEFAULT '0',
  `network_id` varchar(200) NOT NULL,
  `number_vnfs` int(20) NOT NULL,
  `status` enum('ACTIVE','INACTIVE','BUILD','ERROR') NOT NULL DEFAULT 'INACTIVE',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `summary` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  UNIQUE KEY `usage_id_UNIQUE` (`usage_id`),
  KEY `flavor_id_idx` (`flavor_id`),
  KEY `tenant_id_idx` (`project_id`),
  KEY `ns_id_idx` (`ns_id`),
  CONSTRAINT `usage_id` FOREIGN KEY (`usage_id`) REFERENCES `resource_usage_rm` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5556 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `resource_usage_rm`
--

DROP TABLE IF EXISTS `resource_usage_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource_usage_rm` (
  `uuid` varchar(36) NOT NULL,
  `project_id` varchar(45) NOT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `resource` varchar(45) NOT NULL,
  `in_use` int(45) NOT NULL DEFAULT '0',
  `reserved` int(45) NOT NULL DEFAULT '0',
  `until_refresh` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='Resource Usage table';
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `rsv_vnf_rm`
--

DROP TABLE IF EXISTS `rsv_vnf_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rsv_vnf_rm` (
  `reservation_id` varchar(100) NOT NULL,
  `vnf_id` varchar(36) NOT NULL,
  PRIMARY KEY (`reservation_id`,`vnf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `tenants_quota_compute_rm`
--

DROP TABLE IF EXISTS `tenants_quota_compute_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants_quota_compute_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `max_vcpus` varchar(45) DEFAULT NULL,
  `max_vmem` varchar(45) DEFAULT NULL,
  `max_instances` varchar(45) DEFAULT NULL,
  `max_floating_ips` varchar(45) DEFAULT NULL,
  `max_fixed_ips` varchar(45) DEFAULT NULL,
  `max_key_pairs` varchar(45) DEFAULT NULL,
  `max_security_group_rules` varchar(45) DEFAULT NULL,
  `max_security_groups` varchar(45) DEFAULT NULL,
  `max_server_group_members` varchar(36) DEFAULT NULL,
  `max_server_groups` varchar(36) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tenants_utilization_compute_rm`
--

DROP TABLE IF EXISTS `tenants_utilization_compute_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants_utilization_compute_rm` (
  `uuid` varchar(36) NOT NULL,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `max_total_vcpus` varchar(45) DEFAULT NULL,
  `total_vcpus_allocated` varchar(45) DEFAULT NULL,
  `total_vcpus_used` varchar(45) DEFAULT NULL,
  `total_vcpus_available` varchar(45) DEFAULT NULL,
  `total_vcpus_reserved` varchar(45) DEFAULT NULL,
  `total_vcpus_active` varchar(45) DEFAULT NULL,
  `percentage_vcpus_used_by_users` varchar(45) DEFAULT NULL,
  `percentage_vcpus_reserved_by_users` varchar(45) DEFAULT NULL,
  `percentage_vcpus_total_util_by_users` varchar(45) DEFAULT NULL,
  `max_total_vmem_size` varchar(45) DEFAULT NULL,
  `total_vmem_allocated` varchar(45) DEFAULT NULL,
  `total_vmem_used` varchar(45) DEFAULT NULL,
  `total_vmem_available` varchar(45) DEFAULT NULL,
  `total_vmem_reserved` varchar(45) DEFAULT NULL,
  `total_vmem_active` varchar(45) DEFAULT NULL,
  `percentage_vmem_used_by_users` varchar(45) DEFAULT NULL,
  `percentage_vmem_reserved_by_users` varchar(45) DEFAULT NULL,
  `percentage_vmem_total_util_by_users` varchar(45) DEFAULT NULL,
  `max_total_instances` varchar(45) DEFAULT NULL,
  `total_instances_allocated` varchar(45) DEFAULT NULL,
  `total_instances_used` varchar(45) DEFAULT NULL,
  `total_instances_available` varchar(45) DEFAULT NULL,
  `total_instances_reserved` varchar(45) DEFAULT NULL,
  `total_instances_active` varchar(45) DEFAULT NULL,
  `percentage_instances_used_by_users` varchar(45) DEFAULT NULL,
  `percentage_instances_reserved_by_users` varchar(45) DEFAULT NULL,
  `percentage_instances_total_util_by_users` varchar(45) DEFAULT NULL,
  `max_total_floatingips` varchar(45) DEFAULT NULL,
  `total_floatingips_allocated` varchar(45) DEFAULT NULL,
  `total_floatingips_used` varchar(45) DEFAULT NULL,
  `total_floatingips_available` varchar(45) DEFAULT NULL,
  `total_floatingips_reserved` varchar(45) DEFAULT NULL,
  `total_floatingips_disassociated` varchar(45) DEFAULT NULL,
  `percentage_floatingips_used_by_users` varchar(45) DEFAULT NULL,
  `percentage_floatingips_reserved_by_users` varchar(45) DEFAULT NULL,
  `percentage_floatingips_total_util_by_users` varchar(45) DEFAULT NULL,
  `maxpersonality` varchar(45) DEFAULT NULL,
  `maxpersonalitysize` varchar(45) DEFAULT NULL,
  `maxservergroups` varchar(45) DEFAULT NULL,
  `totalservergroupsused` varchar(45) DEFAULT NULL,
  `maxsecuritygroups` varchar(45) DEFAULT NULL,
  `totalsecuritygroupsused` varchar(45) DEFAULT NULL,
  `maxservergroupmembers` varchar(45) DEFAULT NULL,
  `maxtotalkeypairs` varchar(45) DEFAULT NULL,
  `maxsecuritygrouprules` varchar(45) DEFAULT NULL,
  `maxservermeta` varchar(45) DEFAULT NULL,
  `maximagemeta` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `refresh` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tenants_utilization_network_rm`
--

DROP TABLE IF EXISTS `tenants_utilization_network_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants_utilization_network_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `max_network` varchar(45) DEFAULT NULL,
  `total_network_allocated` varchar(45) DEFAULT NULL,
  `total_network_used` varchar(45) DEFAULT NULL,
  `total_network_available` varchar(45) DEFAULT NULL,
  `total_network_reserved` varchar(45) DEFAULT NULL,
  `total_network_active` varchar(45) DEFAULT NULL,
  `total_network_inactive` varchar(45) DEFAULT NULL,
  `max_router` varchar(45) DEFAULT NULL,
  `total_router_allocated` varchar(45) DEFAULT NULL,
  `total_router_used` varchar(45) DEFAULT NULL,
  `total_router_available` varchar(45) DEFAULT NULL,
  `total_router_reserved` varchar(45) DEFAULT NULL,
  `total_router_active` varchar(45) DEFAULT NULL,
  `total_router_inactive` varchar(45) DEFAULT NULL,
  `max_port` varchar(45) DEFAULT NULL,
  `total_port_allocated` varchar(45) DEFAULT NULL,
  `total_port_used` varchar(45) DEFAULT NULL,
  `total_port_available` varchar(45) DEFAULT NULL,
  `total_port_reserved` varchar(45) DEFAULT NULL,
  `total_port_active` varchar(45) DEFAULT NULL,
  `total_port_inactive` varchar(45) DEFAULT NULL,
  `max_floatingip` varchar(45) DEFAULT NULL,
  `total_floatingip_allocated` varchar(45) DEFAULT NULL,
  `total_floatingip_used` varchar(45) DEFAULT NULL,
  `total_floatingip_available` varchar(45) DEFAULT NULL,
  `total_floatingip_reserved` varchar(45) DEFAULT NULL,
  `total_floatingip_active` varchar(45) DEFAULT NULL,
  `total_floatingip_inactive` varchar(45) DEFAULT NULL,
  `max_subnet` varchar(45) DEFAULT NULL,
  `total_subnet_allocated` varchar(45) DEFAULT NULL,
  `total_subnet_used` varchar(45) DEFAULT NULL,
  `total_subnet_available` varchar(45) DEFAULT NULL,
  `total_subnet_reserved` varchar(45) DEFAULT NULL,
  `max_subnetpool` varchar(45) DEFAULT NULL,
  `max_security_group_rule` varchar(45) DEFAULT NULL,
  `max_security_group` varchar(45) DEFAULT NULL,
  `max_rbac_policy` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  `refresh` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tenants_utilization_storage_rm`
--

DROP TABLE IF EXISTS `tenants_utilization_storage_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants_utilization_storage_rm` (
  `uuid` int(36) NOT NULL,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `max_total_gigabytes` varchar(45) DEFAULT NULL,
  `total_gigabytes_allocated` varchar(45) DEFAULT NULL,
  `total_gigabytes_used` varchar(45) DEFAULT NULL,
  `total_gigabytes_available` varchar(45) DEFAULT NULL,
  `total_gigabytes_reserved` varchar(45) DEFAULT NULL,
  `max_total_backup_gigabytes` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_allocated` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_used` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_available` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_reserved` varchar(45) DEFAULT NULL,
  `max_total_backup` varchar(45) DEFAULT NULL,
  `total_backup_allocated` varchar(45) DEFAULT NULL,
  `total_backup_used` varchar(45) DEFAULT NULL,
  `total_backup_available` varchar(45) DEFAULT NULL,
  `total_backup_reserved` varchar(45) DEFAULT NULL,
  `max_total_snapshots` varchar(45) DEFAULT NULL,
  `total_snapshots_allocated` varchar(45) DEFAULT NULL,
  `total_snapshots_used` varchar(45) DEFAULT NULL,
  `total_snapshots_available` varchar(45) DEFAULT NULL,
  `total_snapshots_reserved` varchar(45) DEFAULT NULL,
  `max_total_volumes` varchar(45) DEFAULT NULL,
  `total_volumes_allocated` varchar(45) DEFAULT NULL,
  `total_volumes_used` varchar(45) DEFAULT NULL,
  `total_volumes_available` varchar(45) DEFAULT NULL,
  `total_volumes_reserved` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `refresh` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_rm`
--

DROP TABLE IF EXISTS `users_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_rm` (
  `user_name` varchar(100) NOT NULL,
  `user_id` varchar(100) NOT NULL,
  `project_id` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  KEY `project_id_idx` (`project_id`),
  CONSTRAINT `project_id` FOREIGN KEY (`project_id`) REFERENCES `project_rm` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_util_compute_rm`
--

DROP TABLE IF EXISTS `users_util_compute_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_util_compute_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `max_vcpus` varchar(45) DEFAULT NULL,
  `used_vcpus` varchar(45) DEFAULT NULL,
  `available_vcpus` varchar(45) DEFAULT NULL,
  `reserved_vcpus` varchar(45) DEFAULT NULL,
  `percentage_vcpus_used` varchar(45) DEFAULT NULL,
  `percentage_vcpus_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_vcpus_usage` varchar(45) DEFAULT NULL,
  `max_vmem` varchar(45) DEFAULT NULL,
  `used_vmem` varchar(45) DEFAULT NULL,
  `available_vmem` varchar(45) DEFAULT NULL,
  `reserved_vmem` varchar(45) DEFAULT NULL,
  `percentage_vmem_used` varchar(45) DEFAULT NULL,
  `percentage_vmem_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_vmem_usage` varchar(45) DEFAULT NULL,
  `max_vnfs` varchar(45) DEFAULT NULL,
  `used_vnfs` varchar(45) DEFAULT NULL,
  `available_vnfs` varchar(45) DEFAULT NULL,
  `reserved_vnfs` varchar(45) DEFAULT NULL,
  `percentage_vnfs_used` varchar(45) DEFAULT NULL,
  `percentage_vnfs_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_vnfs_usage` varchar(45) DEFAULT NULL,
  `max_floating_ips` varchar(45) DEFAULT NULL,
  `used_floating_ips` varchar(45) DEFAULT NULL,
  `available_floating_ips` varchar(45) DEFAULT NULL,
  `reserved_floating_ips` varchar(45) DEFAULT NULL,
  `percentage_floating_ips_used` varchar(45) DEFAULT NULL,
  `percentage_floating_ips_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_floating_ips_usage` varchar(45) DEFAULT NULL,
  `max_fixed_ips` varchar(45) DEFAULT NULL,
  `max_key_pairs` varchar(45) DEFAULT NULL,
  `max_security_group_rules` varchar(45) DEFAULT NULL,
  `max_security_groups` varchar(45) DEFAULT NULL,
  `max_injected_file_content_bytes` varchar(45) DEFAULT NULL,
  `max_injected_file_path_bytes` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_util_network_rm`
--

DROP TABLE IF EXISTS `users_util_network_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_util_network_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `max_network` varchar(45) DEFAULT NULL,
  `used_network` varchar(45) DEFAULT NULL,
  `available_network` varchar(45) DEFAULT NULL,
  `reserved_network` varchar(45) DEFAULT NULL,
  `percentage_network_used` varchar(45) DEFAULT NULL,
  `percentage_network_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_network_usage` varchar(45) DEFAULT NULL,
  `max_floatingip` varchar(45) DEFAULT NULL,
  `used_floatingip` varchar(45) DEFAULT NULL,
  `available_floatingip` varchar(45) DEFAULT NULL,
  `reserved_floatingip` varchar(45) DEFAULT NULL,
  `percentage_floatingip_used` varchar(45) DEFAULT NULL,
  `percentage_floatingip_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_floatingip_usage` varchar(45) DEFAULT NULL,
  `max_subnet` varchar(45) DEFAULT NULL,
  `used_subnet` varchar(45) DEFAULT NULL,
  `available_subnet` varchar(45) DEFAULT NULL,
  `reserved_subnet` varchar(45) DEFAULT NULL,
  `percentage_subnet_used` varchar(45) DEFAULT NULL,
  `percentage_subnet_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_subnet_usage` varchar(45) DEFAULT NULL,
  `max_router` varchar(45) DEFAULT NULL,
  `used_router` varchar(45) DEFAULT NULL,
  `available_router` varchar(45) DEFAULT NULL,
  `reserved_router` varchar(45) DEFAULT NULL,
  `percentage_router_used` varchar(45) DEFAULT NULL,
  `percentage_router_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_router_usage` varchar(45) DEFAULT NULL,
  `max_port` varchar(45) DEFAULT NULL,
  `used_port` varchar(45) DEFAULT NULL,
  `available_port` varchar(45) DEFAULT NULL,
  `reserved_port` varchar(45) DEFAULT NULL,
  `percentage_port_used` varchar(45) DEFAULT NULL,
  `percentage_port_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_port_usage` varchar(45) DEFAULT NULL,
  `max_subnetpool` varchar(45) DEFAULT NULL,
  `used_subnetpool` varchar(45) DEFAULT NULL,
  `available_subnetpool` varchar(45) DEFAULT NULL,
  `reserved_subnetpool` varchar(45) DEFAULT NULL,
  `percentage_subnetpool_used` varchar(45) DEFAULT NULL,
  `percentage_subnetpool_reserved` varchar(45) DEFAULT NULL,
  `percentage_total_subnetpool_usage` varchar(45) DEFAULT NULL,
  `max_security_group` varchar(45) DEFAULT NULL,
  `max_security_group_rule` varchar(45) DEFAULT NULL,
  `max_rbac_policy` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcpu_capacity_rm`
--

DROP TABLE IF EXISTS `vcpu_capacity_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcpu_capacity_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `cpu_total` int(12) NOT NULL,
  `vcpu_total` int(12) NOT NULL,
  `vcpu_allocated` int(12) NOT NULL,
  `cpu_available` int(12) NOT NULL,
  `vcpu_available` int(12) NOT NULL,
  `vcpu_reserved` int(12) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vdisk_capacity_rm`
--

DROP TABLE IF EXISTS `vdisk_capacity_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vdisk_capacity_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `disk_total` int(100) NOT NULL,
  `disk_allocated` int(100) NOT NULL,
  `disk_available` int(100) NOT NULL,
  `disk_reserved` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=12132 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vmem_capacity_rm`
--

DROP TABLE IF EXISTS `vmem_capacity_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vmem_capacity_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `mem_total` int(100) NOT NULL,
  `vmem_total` int(100) NOT NULL,
  `vmem_allocated` int(100) NOT NULL,
  `mem_available` int(100) NOT NULL,
  `vmem_available` int(100) NOT NULL,
  `vmem_reserved` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vnfdid_rsv_rm`
--

DROP TABLE IF EXISTS `vnfdid_rsv_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vnfdid_rsv_rm` (
  `vnfdId` varchar(36) NOT NULL,
  `reservation_id` int(36) NOT NULL,
  PRIMARY KEY (`vnfdId`,`reservation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='VNF Descriptor and reservation info';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:23:54
