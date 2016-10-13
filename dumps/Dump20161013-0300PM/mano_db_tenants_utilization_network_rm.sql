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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:12
