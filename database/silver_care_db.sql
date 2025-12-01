-- MySQL dump 10.13  Distrib 8.0.43, for macos15 (x86_64)
--
-- Host: localhost    Database: silver_care_db
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `appointment_type` varchar(100) NOT NULL,
  `status` varchar(50) DEFAULT 'scheduled',
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (29,12,5,'2025-12-31','10:00:00','checkup','scheduled','hello','2025-11-06 18:14:04'),(34,38,6,'2025-11-21','10:30:00','medication','scheduled','4','2025-11-06 21:49:56'),(35,39,4,'2025-11-19','11:00:00','checkup','scheduled','','2025-11-06 22:39:12'),(37,11,2,'2026-02-05','11:00:00','checkup','scheduled','blah blah blah','2025-11-20 20:20:34'),(38,10,2,'2025-12-25','15:00:00','therapy','scheduled','testing <3','2025-11-20 23:12:10');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `phn` varchar(50) NOT NULL,
  `emergency_contact` varchar(255) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phn` (`phn`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (10,'lemon','meringue','lmeringue@gmail.com','7786810217','1975-10-04','LMNOP','strawberry shortcake',2,'2025-11-06 08:04:57',NULL,NULL,NULL),(11,'Elon','Musk','emusk@gmail.com','7785613456','1968-12-09','9690 992 27','mark zuk',2,'2025-11-06 08:06:41',NULL,NULL,NULL),(12,'bruno','mars','bmars@gmail.com','7785675432','1999-12-01','1234567','ebube',5,'2025-11-06 18:13:42',NULL,NULL,NULL),(36,'jewel','paing','jpaing@gmail.com','7786543211','2001-10-22','7786542','ebube',5,'2025-11-06 19:01:04',NULL,NULL,NULL),(37,'John','Mayor','jmayor@gmail.com','322657990','1983-11-06','6777709923','99067742239',4,'2025-11-06 19:23:02',NULL,NULL,NULL),(38,'Mike','Tyson','mtyson@gmail.com','7786810210','1998-10-27','88888888','luke',6,'2025-11-06 21:49:36',NULL,NULL,NULL),(39,'Johnny','Zhang','jzhang@gmail.com','788095432','1992-11-18','1111111111','9066754f3',4,'2025-11-06 22:38:33','What is your favorite food?','Pizza','scrypt:32768:8:1$bS40ZF4cJGLYRImr$67ae2328758773efb6da15cd70bad6d554cfed38ba056c266ca11a10b38789f15032ed5a86e890618c537cea313d711367d0cc1347c30612c0312290d9bf01dd'),(49,'helen','jacob','hjacob@gmail.com','7786815555','1998-10-10','54321','ebube',2,'2025-11-20 19:36:08',NULL,NULL,NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  `totp_secret` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (2,'ebube@silvercare.org','scrypt:32768:8:1$vBvqnaaGYaM8TIvo$60ac5581ad1a86c4395156f45c41dca14f3b41f7296d898e70f2ff8795879e387a62c2297b8e7f2f731edbf0c7f00b0d20e69bb42ae13203123ae1de097f5c29','Ebube','Nwasike','2025-10-25 04:48:32','What street did you grow up on?','Hastings','IFT7KEDJ2ZMERCIOCXEQJNHV75PXPEAQ'),(3,'mona@silvercare.org','scrypt:32768:8:1$Y9O4lHG7f1FslYQv$1ee062ca2053bbe8797bcd5e8960d0143171b16f4b49db68bacb61c707df4d4f8f70ea15fef11c7abdb2d48601d8a25ab8667612419879e12f483798e545a455','Mona','Bakhshoodeh','2025-10-25 04:50:44','What street did you grow up on?','Hastings','YWKCS6455WCZJQ2IQAF23E3SX4WHLENV'),(4,'jewel@silvercare.org','scrypt:32768:8:1$p3APF4Bf2kkf54Mc$3e5f34c6909b97f134578b41480523838c2aa2889a62badcc6f4a2764fa7a33d37e54386e3651ac40662bf7fc5a9188d48103d7e934cb68a55ea028a02be6c10','Jewel','Paing','2025-10-25 05:09:00','What is your favorite color?','Pink',NULL),(5,'priya@silvercare.org','scrypt:32768:8:1$GVDNJ5qXKVF5l3TR$b4a9a10a36d98ae5c3e1b666198141719f27bc2857ac2110640813bcb908d8f6795656814a8e7dfd1a62324173969c03d0a683b1d2c87dd67242a663bb43c243','Priya','Priya','2025-10-25 05:10:00','What is your favorite color?','Pink',NULL),(6,'shubnoor@silvercare.org','scrypt:32768:8:1$p8P93I2fnCs5R2T8$e5d6581d2e5a092e80ca01fd58dd7232d01f322b0ab8cf3aff1dfa82579e80ae6f44987dd505969c4648dc2a85e5124010a567760d597c63e6d148d0b27a2f6d','Shubnoor','Singh','2025-10-25 05:11:00','What is your first pet’s name?','anna','KVKHVISEDBZMWE3OSCOWG7G25YG7QZTM');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vitals`
--

DROP TABLE IF EXISTS `vitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vitals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `blood_pressure` varchar(20) DEFAULT NULL,
  `bmi` float DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `respiratory_rate` int DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `heart_rate` int DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `vitals_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `vitals_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vitals`
--

LOCK TABLES `vitals` WRITE;
/*!40000 ALTER TABLE `vitals` DISABLE KEYS */;
INSERT INTO `vitals` VALUES (2,10,2,'73',24.3,70,168,18,36,57,'2025-11-06 08:08:54'),(3,12,5,'73',25,70,170,6,2,2,'2025-11-06 18:15:39'),(4,11,2,'56',4,4,3,3,3,3,'2025-11-06 18:38:18'),(5,37,4,'120',24,75,165,30,36,75,'2025-11-06 19:24:45'),(6,38,6,'4',4,4,4,4,4,4,'2025-11-06 21:49:45'),(7,39,4,'120',85,85,170,80,37,35,'2025-11-06 22:40:14');
/*!40000 ALTER TABLE `vitals` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 11:38:36
