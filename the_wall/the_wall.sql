-- MySQL dump 10.13  Distrib 8.0.13, for macos10.14 (x86_64)
--
-- Host: localhost    Database: the_wall
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` text,
  `sid` int(11) DEFAULT NULL,
  `rid` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (5,'asdf',1,4,'2018-11-08 08:49:36','2018-11-08 08:49:36'),(10,'Hi Jane',1,2,'2018-11-08 10:40:15','2018-11-08 10:40:15'),(13,'Hi Elise',1,5,'2018-11-08 18:21:51','2018-11-08 18:21:51'),(14,'Hi Elise',1,2,'2018-11-08 18:22:27','2018-11-08 18:22:27'),(17,'hi jake',5,4,'2018-11-08 18:33:09','2018-11-08 18:33:09');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Alex','asdf','alex@email.com','$2b$12$KbSuc5neBQi1NRgfRLT5l.55j8gd3hsQ/ngDeHuQcNfC/aZerHCUS','2018-11-07 20:25:27','2018-11-07 20:25:27'),(2,'Jane','Doje','jane@email.com','$2b$12$0aC8CN3tZcvZxdgOfqzbcun4zwCSTiVLKnnwe4b26AOWKJffU2dba','2018-11-07 20:26:11','2018-11-07 20:26:11'),(3,'Joe','Schmoe','joe@email.com','$2b$12$MepHF/qGxIHFU3Rqxz36U.6g0NWRFjdRczvNCQlSSyK9MaYS/T6iS','2018-11-07 20:26:39','2018-11-07 20:26:39'),(4,'jake','smake','jake@email.com','$2b$12$kDT.1lLad7Foj6NyNVQFH.kYYJrfUCDUlP.cGpQSqBWxpbIxMF0Oi','2018-11-07 20:29:29','2018-11-07 20:29:29'),(5,'Elise','Smelise','elise@email.com','$2b$12$5c.kc7G3snntpevCSrePWujD5olscjs4Q/0NuZ/Yesrmka9nRqUO6','2018-11-07 20:30:11','2018-11-07 20:30:11');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-09  0:02:05
---
----minsmarf@yahoo.com Minsmarf1
----test@yahoo.com  Testtest1
