-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: rm_db
-- ------------------------------------------------------
-- Server version	5.7.11-log

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
-- Table structure for table `flavor`
--

DROP TABLE IF EXISTS `flavor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavor` (
  `flavor_id` varchar(20) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `ram` int(30) DEFAULT NULL,
  `disk` int(30) DEFAULT NULL,
  `vcpu` int(30) DEFAULT NULL,
  PRIMARY KEY (`flavor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavor`
--

LOCK TABLES `flavor` WRITE;
/*!40000 ALTER TABLE `flavor` DISABLE KEYS */;
INSERT INTO `flavor` VALUES ('1','m.tiny',512,1,1),('2','m1.small',2,20,1),('3','m.medium',4096,40,2);
/*!40000 ALTER TABLE `flavor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `image_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `image_status` enum('ACTIVE','DOWN','BUILD','ERROR') DEFAULT 'BUILD',
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES ('19f7025b-b78a-4bf0-bc37-0cba68e16b10','ubuntu_01','BUILD'),('3d356f2b-79da-468e-8e31-ec0c861190e1','cirros-0.3.4-x86_64-uec','ACTIVE');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `network_capacity`
--

DROP TABLE IF EXISTS `network_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `network_capacity` (
  `network_name` varchar(200) NOT NULL,
  `network_id` varchar(300) NOT NULL,
  `network_status` enum('ACTIVE','DOWN','BUILD','ERROR') NOT NULL DEFAULT 'BUILD',
  PRIMARY KEY (`network_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `network_capacity`
--

LOCK TABLES `network_capacity` WRITE;
/*!40000 ALTER TABLE `network_capacity` DISABLE KEYS */;
INSERT INTO `network_capacity` VALUES ('local_test','cdd0fd03-9205-4084-99e0-e9555477d23d','ACTIVE');
/*!40000 ALTER TABLE `network_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nfvo_ns`
--

DROP TABLE IF EXISTS `nfvo_ns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nfvo_ns` (
  `ns_id` varchar(100) NOT NULL,
  `ns_name` varchar(100) DEFAULT NULL,
  `user_id` varchar(100) NOT NULL,
  `tenant_id` varchar(100) NOT NULL,
  PRIMARY KEY (`ns_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `tenant_id_UNIQUE` (`tenant_id`),
  UNIQUE KEY `ns_name_UNIQUE` (`ns_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nfvo_ns`
--

LOCK TABLES `nfvo_ns` WRITE;
/*!40000 ALTER TABLE `nfvo_ns` DISABLE KEYS */;
/*!40000 ALTER TABLE `nfvo_ns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `reservation_id` varchar(100) NOT NULL,
  `label` varchar(100) NOT NULL,
  `host_id` varchar(100) NOT NULL,
  `host_name` varchar(100) DEFAULT NULL,
  `user_id` varchar(100) NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `tenant_id` varchar(100) NOT NULL,
  `tenant_name` varchar(100) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `flavor_id` int(20) NOT NULL,
  `image_id` varchar(100) NOT NULL,
  `instance_id` varchar(100) NOT NULL,
  `network_id` varchar(200) NOT NULL,
  `number_instance` varchar(45) DEFAULT NULL,
  `ns_id` varchar(100) NOT NULL,
  `status` enum('ACTIVE','DOWN','BUILD','ERROR') NOT NULL DEFAULT 'BUILD',
  `summary` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `image_id_idx` (`image_id`),
  KEY `flavor_id_idx` (`flavor_id`),
  KEY `user_id_idx` (`user_id`),
  KEY `tenant_id_idx` (`tenant_id`),
  KEY `ns_id_idx` (`ns_id`),
  CONSTRAINT `image_id` FOREIGN KEY (`image_id`) REFERENCES `image` (`image_id`) ON DELETE CASCADE,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
INSERT INTO `reservation` VALUES ('67810','test3','12212817268DJKHSAJD','hai_compute','48c70b9e59c240768bb2b88ffb1eb66c','admin','cfcb18eef55b4b03bb075ea106fe771f','admin','2016-05-23 18:04:00','2016-05-23 18:09:00',1,'3d356f2b-79da-468e-8e31-ec0c861190e1','null','f61491df-3ad8-4ac4-9974-6b6ea27bf5f0','1','SJDHS765327SDHJSG8236BSD826734','ACTIVE','reservation testing'),('67811','test4','12212817268DJKHSAJD','hai_compute','48c70b9e59c240768bb2b88ffb1eb66c','admin','cfcb18eef55b4b03bb075ea106fe771f','admin','2016-05-23 18:04:00','2016-05-23 18:09:00',1,'3d356f2b-79da-468e-8e31-ec0c861190e1','null','f61491df-3ad8-4ac4-9974-6b6ea27bf5f0','1','SJDHS765327SDHJSG8236BSD826734','ACTIVE','reservation testing'),('67816','test4','12212817268DJKHSAJD','hai_compute','48c70b9e59c240768bb2b88ffb1eb66c','admin','cfcb18eef55b4b03bb075ea106fe771f','admin','2016-05-23 18:04:00','2016-05-23 18:09:00',1,'3d356f2b-79da-468e-8e31-ec0c861190e1','null','f61491df-3ad8-4ac4-9974-6b6ea27bf5f0','1','SJDHS765327SDHJSG8236BSD826734','ACTIVE','reservation testing'),('6789','test2','12212817268DJKHSAJD','hai_compute','48c70b9e59c240768bb2b88ffb1eb66c','admin','cfcb18eef55b4b03bb075ea106fe771f','admin','2016-05-23 18:04:00','2016-05-23 18:09:00',1,'3d356f2b-79da-468e-8e31-ec0c861190e1','null','f61491df-3ad8-4ac4-9974-6b6ea27bf5f0','1','SJDHS765327SDHJSG8236BSD826734','ACTIVE','reservation testing');
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant`
--

DROP TABLE IF EXISTS `tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenant` (
  `tenant_name` varchar(100) NOT NULL,
  `tenant_id` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`tenant_id`),
  UNIQUE KEY `tenant_name_UNIQUE` (`tenant_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant`
--

LOCK TABLES `tenant` WRITE;
/*!40000 ALTER TABLE `tenant` DISABLE KEYS */;
INSERT INTO `tenant` VALUES ('admin','cfcb18eef55b4b03bb075ea106fe771f','2016-04-21 03:11:11','2016-04-21 03:11:11');
/*!40000 ALTER TABLE `tenant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_name` varchar(100) NOT NULL,
  `user_id` varchar(100) NOT NULL,
  `tenant_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `tenant_id_UNIQUE` (`tenant_id`),
  CONSTRAINT `tenant_id` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`tenant_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','48c70b9e59c240768bb2b88ffb1eb66c','cfcb18eef55b4b03bb075ea106fe771f');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vapps`
--

DROP TABLE IF EXISTS `vapps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vapps` (
  `ns_id` varchar(36) NOT NULL,
  `instance_id` varchar(36) NOT NULL,
  `instance_name` varchar(36) NOT NULL,
  `instance_floatingip` varchar(36) NOT NULL,
  `instance_floatingip_id` varchar(36) NOT NULL,
  `instance_ip` varchar(36) NOT NULL,
  `instance_mac_address` varchar(36) NOT NULL,
  `instance_network_id` varchar(36) NOT NULL,
  `instance_port_id` varchar(36) NOT NULL,
  `instance_cidr` varchar(36) NOT NULL,
  `instance_image_id` varchar(36) NOT NULL,
  PRIMARY KEY (`instance_id`),
  KEY `ns_id_idx` (`ns_id`),
  CONSTRAINT `ns_id` FOREIGN KEY (`ns_id`) REFERENCES `nfvo_ns` (`ns_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vapps`
--

LOCK TABLES `vapps` WRITE;
/*!40000 ALTER TABLE `vapps` DISABLE KEYS */;
/*!40000 ALTER TABLE `vapps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vcpu_capacity`
--

DROP TABLE IF EXISTS `vcpu_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcpu_capacity` (
  `uuid` int(20) NOT NULL AUTO_INCREMENT,
  `cpu_total` int(12) NOT NULL,
  `vcpu_total` int(12) NOT NULL,
  `vcpu_allocated` int(12) NOT NULL,
  `cpu_available` int(12) NOT NULL,
  `vcpu_available` int(12) NOT NULL,
  `vcpu_reserved` int(12) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vcpu_capacity`
--

LOCK TABLES `vcpu_capacity` WRITE;
/*!40000 ALTER TABLE `vcpu_capacity` DISABLE KEYS */;
INSERT INTO `vcpu_capacity` VALUES (32,4,64,3,4,0,1,'2016-05-27 18:15:58','2016-06-04 07:05:31');
/*!40000 ALTER TABLE `vcpu_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vdisk_capacity`
--

DROP TABLE IF EXISTS `vdisk_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vdisk_capacity` (
  `uuid` int(20) NOT NULL AUTO_INCREMENT,
  `disk_total` int(100) NOT NULL,
  `disk_allocated` int(100) NOT NULL,
  `disk_available` int(100) NOT NULL,
  `disk_reserved` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=12132 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vdisk_capacity`
--

LOCK TABLES `vdisk_capacity` WRITE;
/*!40000 ALTER TABLE `vdisk_capacity` DISABLE KEYS */;
INSERT INTO `vdisk_capacity` VALUES (12131,454,60,319,1,'2016-05-27 18:15:59','2016-05-31 04:09:42');
/*!40000 ALTER TABLE `vdisk_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vmem_capacity`
--

DROP TABLE IF EXISTS `vmem_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vmem_capacity` (
  `uuid` int(20) NOT NULL AUTO_INCREMENT,
  `mem_total` int(100) NOT NULL,
  `vmem_total` int(100) NOT NULL,
  `vmem_allocated` int(100) NOT NULL,
  `mem_available` int(100) NOT NULL,
  `vmem_available` int(100) NOT NULL,
  `vmem_reserved` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vmem_capacity`
--

LOCK TABLES `vmem_capacity` WRITE;
/*!40000 ALTER TABLE `vmem_capacity` DISABLE KEYS */;
INSERT INTO `vmem_capacity` VALUES (11,7858,11787,6656,1202,523,512,'2016-05-27 18:15:58','2016-05-27 18:15:58');
/*!40000 ALTER TABLE `vmem_capacity` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-07 22:20:21
