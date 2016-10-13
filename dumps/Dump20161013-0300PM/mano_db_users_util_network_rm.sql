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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:10
