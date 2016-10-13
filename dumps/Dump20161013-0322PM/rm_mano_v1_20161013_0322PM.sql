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
-- Dumping data for table `flavors_rm`
--

LOCK TABLES `flavors_rm` WRITE;
/*!40000 ALTER TABLE `flavors_rm` DISABLE KEYS */;
INSERT INTO `flavors_rm` VALUES ('1','m.tiny',512,1,1),('2','m1.small',2,20,1),('3','m.medium',4096,40,2);
/*!40000 ALTER TABLE `flavors_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `flavour_info_rm`
--

LOCK TABLES `flavour_info_rm` WRITE;
/*!40000 ALTER TABLE `flavour_info_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `flavour_info_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `images_rm`
--

LOCK TABLES `images_rm` WRITE;
/*!40000 ALTER TABLE `images_rm` DISABLE KEYS */;
INSERT INTO `images_rm` VALUES ('19f7025b-b78a-4bf0-bc37-0cba68e16b10','ubuntu_01','BUILD'),('68e9fa2a-afa2-4e32-8598-35cea0f704fa','cirros-0.3.4-x86_64-uec','ACTIVE');
/*!40000 ALTER TABLE `images_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `networks_details_rm`
--

LOCK TABLES `networks_details_rm` WRITE;
/*!40000 ALTER TABLE `networks_details_rm` DISABLE KEYS */;
INSERT INTO `networks_details_rm` VALUES (1,'local_test','2d54f36a-8569-4a71-806c-f563a9aa6367','ACTIVE');
/*!40000 ALTER TABLE `networks_details_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `nfvo_ns_rm`
--

LOCK TABLES `nfvo_ns_rm` WRITE;
/*!40000 ALTER TABLE `nfvo_ns_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `nfvo_ns_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `nfvo_projects`
--

LOCK TABLES `nfvo_projects` WRITE;
/*!40000 ALTER TABLE `nfvo_projects` DISABLE KEYS */;
INSERT INTO `nfvo_projects` VALUES ('1fe87562-0227-11e6-8773-0050568b54f4','hjhwang','1fe87562-0227-11e6-8773-0050568b54f4','created'),('74f195a0-0224-11e6-8773-0050568b54f4','hjhwang','74f195a0-0224-11e6-8773-0050568b54f4','created'),('94ed5736-02d3-11e6-8773-0050568b54f4','hjhwang','94ed5736-02d3-11e6-8773-0050568b54f4','created'),('ace5fe4e-3382-11e6-9183-0050568b54f4','krnet','ace5fe4e-3382-11e6-9183-0050568b54f4','created'),('b58b2bdc-0222-11e6-8773-0050568b54f4','hjhwang','b58b2bdc-0222-11e6-8773-0050568b54f4','created'),('c5c0ce94-0227-11e6-8773-0050568b54f4','hjhwang','c5c0ce94-0227-11e6-8773-0050568b54f4','created'),('cf2527c6-021f-11e6-8773-0050568b54f4','hjhwang','cf2527c6-021f-11e6-8773-0050568b54f4',''),('d181b9fc-02d4-11e6-8773-0050568b54f4','hjhwang','d181b9fc-02d4-11e6-8773-0050568b54f4','created');
/*!40000 ALTER TABLE `nfvo_projects` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `project_rm`
--

LOCK TABLES `project_rm` WRITE;
/*!40000 ALTER TABLE `project_rm` DISABLE KEYS */;
INSERT INTO `project_rm` VALUES ('demo','4a766494021447c7905b81adae050a97','2016-05-23 09:04:00','2016-05-23 09:04:00');
/*!40000 ALTER TABLE `project_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `quota_rm`
--

LOCK TABLES `quota_rm` WRITE;
/*!40000 ALTER TABLE `quota_rm` DISABLE KEYS */;
INSERT INTO `quota_rm` VALUES ('8b35ea30-903d-11e6-9710-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','port',11,0,'0000-00-00 00:00:00','2016-10-12 05:13:14','0000-00-00 00:00:00'),('8b3722b0-903d-11e6-bf63-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','vnfs',11,0,'0000-00-00 00:00:00','2016-10-12 05:13:14','0000-00-00 00:00:00'),('8b37e600-903d-11e6-bc27-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','vcpus',11,0,'0000-00-00 00:00:00','2016-10-12 05:13:14','0000-00-00 00:00:00'),('8b38a951-903d-11e6-94ed-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','network',11,0,'0000-00-00 00:00:00','2016-10-12 05:13:14','0000-00-00 00:00:00'),('8b396c9e-903d-11e6-8d64-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','memory',11,0,'0000-00-00 00:00:00','2016-10-12 05:13:14','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `quota_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
  `user_id` varchar(100) NOT NULL DEFAULT 'admin',
  `project_id` varchar(100) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `flavor_id` int(20) NOT NULL,
  `image_id` varchar(100) NOT NULL,
  `ns_id` varchar(100) DEFAULT '0',
  `network_id` varchar(200) NOT NULL,
  `number_vnfs` varchar(45) NOT NULL,
  `status` enum('ACTIVE','INACTIVE','BUILD','ERROR') NOT NULL DEFAULT 'INACTIVE',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `summary` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  UNIQUE KEY `usage_id_UNIQUE` (`usage_id`),
  KEY `image_id_idx` (`image_id`),
  KEY `flavor_id_idx` (`flavor_id`),
  KEY `tenant_id_idx` (`project_id`),
  KEY `ns_id_idx` (`ns_id`),
  CONSTRAINT `image_id` FOREIGN KEY (`image_id`) REFERENCES `images_rm` (`image_id`) ON DELETE CASCADE,
  CONSTRAINT `usage_id` FOREIGN KEY (`usage_id`) REFERENCES `resource_usage_rm` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5556 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `resource_usage_rm`
--

LOCK TABLES `resource_usage_rm` WRITE;
/*!40000 ALTER TABLE `resource_usage_rm` DISABLE KEYS */;
INSERT INTO `resource_usage_rm` VALUES ('8b36d48f-903d-11e6-b184-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'port',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b3797e1-903d-11e6-bd2d-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vnfs',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b385b30-903d-11e6-b13a-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vcpus',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b39458f-903d-11e6-a2be-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'network',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b39bac0-903d-11e6-a4c3-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'memory',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL);
/*!40000 ALTER TABLE `resource_usage_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `rsv_vnf_rm`
--

LOCK TABLES `rsv_vnf_rm` WRITE;
/*!40000 ALTER TABLE `rsv_vnf_rm` DISABLE KEYS */;
INSERT INTO `rsv_vnf_rm` VALUES ('23762sbdhgwshdg','haiupdated');
/*!40000 ALTER TABLE `rsv_vnf_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `tenants_quota_compute_rm`
--

LOCK TABLES `tenants_quota_compute_rm` WRITE;
/*!40000 ALTER TABLE `tenants_quota_compute_rm` DISABLE KEYS */;
INSERT INTO `tenants_quota_compute_rm` VALUES (11,'admin','24104f8dd8074d5aae884f25a583e3d4','20','51200','10','10','-1','100','20','10','10','10','2016-06-14 21:57:47','2016-07-08 05:09:31'),(12,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20','51200','10','10','-1','100','20','10','10','10','2016-06-14 21:57:47','2016-07-08 05:09:31'),(13,'admin','24104f8dd8074d5aae884f25a583e3d4','20','51200','10','10','-1','100','20','10','10','10','2016-06-14 23:42:52','2016-07-08 05:09:31'),(14,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20','51200','10','10','-1','100','20','10','10','10','2016-06-14 23:42:52','2016-07-08 05:09:31'),(15,'admin','24104f8dd8074d5aae884f25a583e3d4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 18:52:30','2016-07-08 05:09:31'),(16,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 18:52:30','2016-07-08 05:09:31');
/*!40000 ALTER TABLE `tenants_quota_compute_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `tenants_utilization_compute_rm`
--

LOCK TABLES `tenants_utilization_compute_rm` WRITE;
/*!40000 ALTER TABLE `tenants_utilization_compute_rm` DISABLE KEYS */;
INSERT INTO `tenants_utilization_compute_rm` VALUES ('1','admin','24104f8dd8074d5aae884f25a583e3d4','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','0000-00-00 00:00:00','2016-07-08 05:10:36',NULL),('10','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20','0','0','20','0',NULL,NULL,NULL,NULL,'51200','0','0','51200','0',NULL,NULL,NULL,NULL,'10','0','0','10','0',NULL,NULL,NULL,NULL,'10','0','0','10','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 10:43:05','2016-07-08 05:10:36',NULL),('11','admin','24104f8dd8074d5aae884f25a583e3d4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 13:21:45','2016-07-08 05:10:36',NULL),('12','demo','e4dd21953bfc4b98a80c5f56a36f9f8b',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 13:21:45','2016-07-08 05:10:36',NULL),('13','admin','24104f8dd8074d5aae884f25a583e3d4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 13:32:52','2016-07-08 05:10:36',NULL),('14','demo','e4dd21953bfc4b98a80c5f56a36f9f8b',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 13:32:52','2016-07-08 05:10:36',NULL),('15','admin','24104f8dd8074d5aae884f25a583e3d4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 15:32:16','2016-07-08 05:10:36',NULL),('16','demo','e4dd21953bfc4b98a80c5f56a36f9f8b',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-01 15:32:16','2016-07-08 05:10:36',NULL),('17','admin','24104f8dd8074d5aae884f25a583e3d4','20','0','0','20','0','0',NULL,NULL,NULL,'51200','0','0','51200','0','0',NULL,NULL,NULL,'10','0','0','10','0','0',NULL,NULL,NULL,'10','0','0','10','0','0',NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 15:41:22','2016-07-08 05:10:36',NULL),('18','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20','0','0','20','0','0',NULL,NULL,NULL,'51200','0','0','51200','0','0',NULL,NULL,NULL,'10','0','0','10','0','0',NULL,NULL,NULL,'10','0','0','10','0','0',NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 15:41:22','2016-07-08 05:10:36',NULL),('19','admin','24104f8dd8074d5aae884f25a583e3d4','20','0','0','20','0','0','0','0','0','51200','0','0','51200','0','0','0','0','0','10','0','0','10','0','0','0','0','0','10','0','0','10','0','0','0','0','0','5','10240','10','0','10','0','10','100','20','128','128','2016-07-05 09:33:16','2016-07-08 05:10:36',NULL),('2','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','0000-00-00 00:00:00','2016-07-08 05:10:36',NULL),('20','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20','55','0','20','0','0','0','0','0','51200','66','0','51200','0','0','0','0','0','10','0','0','10','0','0','0','0','0','10','0','0','10','0','0','0','0','0','5','10240','10','0','10','0','10','100','20','128','128','2016-07-05 09:33:16','2016-07-08 05:10:36',NULL),('3','admin','24104f8dd8074d5aae884f25a583e3d4','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'0',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-06-14 15:04:06','2016-07-08 05:10:36',NULL),('4','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'0',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-06-14 15:04:06','2016-07-08 05:10:36',NULL),('5','admin','24104f8dd8074d5aae884f25a583e3d4','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-06-14 15:07:36','2016-07-08 05:10:36',NULL),('6','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20',NULL,'0','0','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-06-14 15:07:36','2016-07-08 05:10:36',NULL),('7','admin','24104f8dd8074d5aae884f25a583e3d4','20',NULL,'0','20','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 09:59:18','2016-07-08 05:10:36',NULL),('8','demo','e4dd21953bfc4b98a80c5f56a36f9f8b','20',NULL,'0','20','0',NULL,NULL,NULL,NULL,'51200',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'10',NULL,'0','0','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 09:59:18','2016-07-08 05:10:36',NULL),('9','admin','24104f8dd8074d5aae884f25a583e3d4','20','0','0','20','0',NULL,NULL,NULL,NULL,'51200','0','0','51200','0',NULL,NULL,NULL,NULL,'10','0','0','10','0',NULL,NULL,NULL,NULL,'10','0','0','10','0',NULL,NULL,NULL,NULL,'5','10240','10','0','10','0','10','100','20','128','128','2016-07-01 10:43:05','2016-07-08 05:10:36',NULL);
/*!40000 ALTER TABLE `tenants_utilization_compute_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `tenants_utilization_network_rm`
--

LOCK TABLES `tenants_utilization_network_rm` WRITE;
/*!40000 ALTER TABLE `tenants_utilization_network_rm` DISABLE KEYS */;
INSERT INTO `tenants_utilization_network_rm` VALUES (1,'admin','24104f8dd8074d5aae884f25a583e3d4','10',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,'-1','100','10','10','2016-06-15 06:52:30',NULL,0),(2,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','10',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,'-1','100','10','10','2016-06-15 06:52:30',NULL,0),(3,'admin','24104f8dd8074d5aae884f25a583e3d4','10',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,'-1','100','10','10','2016-07-01 09:02:29',NULL,0),(4,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','10',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'50',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL,NULL,NULL,'-1','100','10','10','2016-07-01 09:02:29',NULL,0),(5,'admin','24104f8dd8074d5aae884f25a583e3d4','10','0','2','8','0','2','0','10','0',NULL,'9','0','1','0','50','0','4','46','0','4','0','50','0','0','50','0','0','0','10','0','4','6','0','-1','100','10','10','2016-07-01 15:27:53',NULL,0),(6,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','10','0','2','8','0','2','0','10','0',NULL,'9','0','1','0','50','0','4','46','0','4','0','50','0','0','50','0','0','0','10','0','4','6','0','-1','100','10','10','2016-07-01 15:27:53',NULL,0),(7,'admin','24104f8dd8074d5aae884f25a583e3d4','10','0','2','8','0','2','0','10','0','1','9','0','1','0','50','0','4','46','0','4','0','50','0','0','50','0','0','0','10','0','4','6','0','-1','100','10','10','2016-07-01 15:29:42',NULL,0),(8,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','10','0','2','8','0','2','0','10','0','1','9','0','1','0','50','0','4','46','0','4','0','50','0','0','50','0','0','0','10','0','4','6','0','-1','100','10','10','2016-07-01 15:29:42',NULL,0);
/*!40000 ALTER TABLE `tenants_utilization_network_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `tenants_utilization_storage_rm`
--

LOCK TABLES `tenants_utilization_storage_rm` WRITE;
/*!40000 ALTER TABLE `tenants_utilization_storage_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenants_utilization_storage_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `users_rm`
--

LOCK TABLES `users_rm` WRITE;
/*!40000 ALTER TABLE `users_rm` DISABLE KEYS */;
INSERT INTO `users_rm` VALUES ('demo','ffbc3c72aa9f44769f3430093c59c457','4a766494021447c7905b81adae050a97','2016-05-23 09:04:00','2016-05-23 09:04:00');
/*!40000 ALTER TABLE `users_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `users_util_compute_rm`
--

LOCK TABLES `users_util_compute_rm` WRITE;
/*!40000 ALTER TABLE `users_util_compute_rm` DISABLE KEYS */;
INSERT INTO `users_util_compute_rm` VALUES (1,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:36:47','2016-07-07 08:36:29'),(2,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:36:47','2016-07-07 08:36:29'),(3,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:36:47','2016-07-07 08:36:29'),(4,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:38:17','2016-07-07 08:36:29'),(5,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:38:17','2016-07-07 08:36:29'),(6,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:38:17','2016-07-07 08:36:29'),(7,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 12:45:41','2016-07-07 08:36:29'),(8,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 12:45:41','2016-07-07 08:36:29'),(9,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 12:45:41','2016-07-07 08:36:29'),(10,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:50:38','2016-07-07 08:36:29'),(11,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:50:38','2016-07-07 08:36:29'),(12,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:50:38','2016-07-07 08:36:29'),(13,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:51:47','2016-07-07 08:36:29'),(14,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:51:47','2016-07-07 08:36:29'),(15,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:51:47','2016-07-07 08:36:29'),(16,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:52:35','2016-07-07 08:36:29'),(17,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:52:35','2016-07-07 08:36:29'),(18,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 12:52:35','2016-07-07 08:36:29'),(19,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:19:08','2016-07-07 08:36:29'),(20,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:19:08','2016-07-07 08:36:29'),(21,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:16','2016-07-07 08:36:29'),(22,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:16','2016-07-07 08:36:29'),(23,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:16','2016-07-07 08:36:29'),(24,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:54','2016-07-07 08:36:29'),(25,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:54','2016-07-07 08:36:29'),(26,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:42:54','2016-07-07 08:36:29'),(27,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:46:07','2016-07-07 08:36:29'),(28,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:46:07','2016-07-07 08:36:29'),(29,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 13:46:07','2016-07-07 08:36:29'),(30,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 15:22:55','2016-07-07 08:36:29'),(31,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 15:22:55','2016-07-07 08:36:29'),(32,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 15:22:55','2016-07-07 08:36:29'),(33,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:34','2016-07-07 08:36:29'),(34,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:34','2016-07-07 08:36:29'),(35,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:34','2016-07-07 08:36:29'),(36,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:54','2016-07-07 08:36:29'),(37,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:54','2016-07-07 08:36:29'),(38,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 16:43:54','2016-07-07 08:36:29'),(39,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:01:31','2016-07-07 08:36:29'),(40,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:01:31','2016-07-07 08:36:29'),(41,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:01:31','2016-07-07 08:36:29'),(42,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:04:27','2016-07-07 08:36:29'),(43,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:04:27','2016-07-07 08:36:29'),(44,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:16:26','2016-07-07 08:36:29'),(45,'admin','24104f8dd8074d5aae884f25a583e3d4','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:30:21','2016-07-07 08:36:29'),(46,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','demo','6b4159076dba441d8c5bc46d510fdc15',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:30:21','2016-07-07 08:36:29'),(47,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:30:21','2016-07-07 08:36:29'),(48,'admin','24104f8dd8074d5aae884f25a583e3d4','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:36:09','2016-07-07 08:36:29'),(49,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','demo','6b4159076dba441d8c5bc46d510fdc15',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:36:09','2016-07-07 08:36:29'),(50,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2016-07-06 18:36:09','2016-07-07 08:36:29'),(51,'admin','24104f8dd8074d5aae884f25a583e3d4','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 18:43:07','2016-07-07 08:36:29'),(52,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','demo','6b4159076dba441d8c5bc46d510fdc15','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 18:43:07','2016-07-07 08:36:29'),(53,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-06 18:43:07','2016-07-07 08:36:29'),(54,'admin','24104f8dd8074d5aae884f25a583e3d4','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:08:26','2016-07-07 08:36:29'),(55,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','demo','6b4159076dba441d8c5bc46d510fdc15','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:08:26','2016-07-07 08:36:29'),(56,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:08:26','2016-07-07 08:36:29'),(57,'admin','24104f8dd8074d5aae884f25a583e3d4','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:12:53','2016-07-07 08:36:29'),(58,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','demo','6b4159076dba441d8c5bc46d510fdc15','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:12:53','2016-07-07 08:36:29'),(59,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:12:53','2016-07-07 08:36:29'),(60,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:15:45','2016-07-07 08:36:29'),(61,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:15:45','2016-07-07 08:36:29'),(62,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:15:45','2016-07-07 08:36:29'),(63,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 12:15:45','2016-07-07 08:36:29'),(64,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','21','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','500','2016-07-07 12:15:45','2016-07-07 08:39:29'),(65,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 17:52:24','2016-07-07 08:40:12'),(66,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 17:52:24','2016-07-07 08:40:12'),(67,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 17:52:24','2016-07-07 08:40:12'),(68,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 17:52:24','2016-07-07 08:40:12'),(69,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-07 17:52:24','2016-07-07 08:40:12'),(70,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:54:37'),(71,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:54:37'),(72,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:54:37'),(73,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:54:37'),(74,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:54:37'),(75,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:57:07'),(76,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:57:07'),(77,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:57:07'),(78,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:57:07'),(79,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 08:57:07'),(80,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 09:04:56'),(81,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 09:04:56'),(82,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 09:04:56'),(83,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 09:04:56'),(84,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-07 09:04:56'),(85,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:41:20'),(86,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:41:20'),(87,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:41:20'),(88,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:41:20'),(89,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:41:20'),(90,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:54:23'),(91,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','12','0','0','0','0','8888','0','8888','0','0','0','0','8','0','8','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:54:23'),(92,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:54:23'),(93,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:54:23'),(94,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 18:54:23'),(95,'admin','1975c8ee1c7c4229bdd909ad662fcbe6','admin','bdc8512033bf41b8aad21cb7716774d8','3','0','3','0','0','0','0','6144','0','6144','0','0','0','0','5','0','5','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 19:16:57'),(96,'demo','4a766494021447c7905b81adae050a97','demo','ffbc3c72aa9f44769f3430093c59c457','12','0','5','1','0','0','0','8888','0','3256','512','0','0','0','8','0','6','1','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','2016-07-23 15:47:03','2016-07-23 06:24:57'),(97,'demo','4a766494021447c7905b81adae050a97','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 19:16:57'),(98,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','admin','bdc8512033bf41b8aad21cb7716774d8','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 19:16:57'),(99,'alt_demo','eee7524f2a02492f8097ffbf8b45ad80','alt_demo','700d7159054246869d0dd500d102c263','20','0','0','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-07-08 20:35:46'),(100,'demo','25970fbcfb0a4c2fb42ccc18f1bccde3','admin','1c06f7e6cecb4652b4f16893535ce192','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 01:36:55'),(101,'demo','25970fbcfb0a4c2fb42ccc18f1bccde3','demo','72bee913ee0e49ebac926e199d94c5a9','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 01:36:55'),(102,'alt_demo','9eb6ce2d913a46e3931aa651fccf3d76','alt_demo','096a1f886f1345fa932a0143ab058b7a','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 01:36:55'),(103,'alt_demo','9eb6ce2d913a46e3931aa651fccf3d76','admin','1c06f7e6cecb4652b4f16893535ce192','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 01:36:55'),(104,'admin','f4211c8eee044bfb9dea2050fef2ace5','admin','1c06f7e6cecb4652b4f16893535ce192','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 01:36:55'),(105,'demo','25970fbcfb0a4c2fb42ccc18f1bccde3','admin','1c06f7e6cecb4652b4f16893535ce192','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 02:04:05'),(106,'demo','25970fbcfb0a4c2fb42ccc18f1bccde3','demo','72bee913ee0e49ebac926e199d94c5a9','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 02:04:05'),(107,'alt_demo','9eb6ce2d913a46e3931aa651fccf3d76','alt_demo','096a1f886f1345fa932a0143ab058b7a','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 02:04:05'),(108,'alt_demo','9eb6ce2d913a46e3931aa651fccf3d76','admin','1c06f7e6cecb4652b4f16893535ce192','20','0','20','0','0','0','0','51200','0','51200','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','100','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 02:04:05'),(109,'admin','f4211c8eee044bfb9dea2050fef2ace5','admin','1c06f7e6cecb4652b4f16893535ce192','221','0','221','0','0','0','0','2222','0','2222','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','-1','22','20','10','10240','255','0000-00-00 00:00:00','2016-09-12 02:04:05');
/*!40000 ALTER TABLE `users_util_compute_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `users_util_network_rm`
--

LOCK TABLES `users_util_network_rm` WRITE;
/*!40000 ALTER TABLE `users_util_network_rm` DISABLE KEYS */;
INSERT INTO `users_util_network_rm` VALUES (1,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','10','0','10','0','0','0','0','50','0','50','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','50','0','50','0','0','0','0','-1','0','-1','0','0','0','0','10','100','10','2016-07-06 03:46:24',NULL),(2,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','10','0','10','0','0','0','0','50','0','50','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','50','0','50','0','0','0','0','-1','0','-1','0','0','0','0','10','100','10','2016-07-06 03:46:24',NULL),(3,'demo','e4dd21953bfc4b98a80c5f56a36f9f8b','admin','e1e78d696e7045da82256cd1e221f9e6','10','0','10','0','0','0','0','50','0','50','0','0','0','0','10','0','10','0','0','0','0','10','0','10','0','0','0','0','50','0','50','0','0','0','0','-1','0','-1','0','0','0','0','10','100','10','2016-07-06 03:46:24',NULL);
/*!40000 ALTER TABLE `users_util_network_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `vcpu_capacity_rm`
--

LOCK TABLES `vcpu_capacity_rm` WRITE;
/*!40000 ALTER TABLE `vcpu_capacity_rm` DISABLE KEYS */;
INSERT INTO `vcpu_capacity_rm` VALUES (32,4,64,3,4,0,1,'2016-05-27 18:15:58','2016-06-08 06:02:02');
/*!40000 ALTER TABLE `vcpu_capacity_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `vdisk_capacity_rm`
--

LOCK TABLES `vdisk_capacity_rm` WRITE;
/*!40000 ALTER TABLE `vdisk_capacity_rm` DISABLE KEYS */;
INSERT INTO `vdisk_capacity_rm` VALUES (12131,454,60,390,1,'2016-05-27 18:15:59','2016-06-08 05:20:23');
/*!40000 ALTER TABLE `vdisk_capacity_rm` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `vmem_capacity_rm`
--

LOCK TABLES `vmem_capacity_rm` WRITE;
/*!40000 ALTER TABLE `vmem_capacity_rm` DISABLE KEYS */;
INSERT INTO `vmem_capacity_rm` VALUES (11,7858,11787,6656,0,3083,512,'2016-05-27 18:15:58','2016-06-08 05:47:10');
/*!40000 ALTER TABLE `vmem_capacity_rm` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Dumping data for table `vnfdid_rsv_rm`
--

LOCK TABLES `vnfdid_rsv_rm` WRITE;
/*!40000 ALTER TABLE `vnfdid_rsv_rm` DISABLE KEYS */;
INSERT INTO `vnfdid_rsv_rm` VALUES ('sjhdgsjdh121',23762);
/*!40000 ALTER TABLE `vnfdid_rsv_rm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:23:54
