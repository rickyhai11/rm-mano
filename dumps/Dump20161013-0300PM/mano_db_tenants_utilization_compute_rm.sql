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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:10
