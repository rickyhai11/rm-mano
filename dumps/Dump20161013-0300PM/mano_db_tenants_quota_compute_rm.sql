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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:11
