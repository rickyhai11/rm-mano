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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:12
