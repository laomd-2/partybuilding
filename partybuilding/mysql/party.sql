-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: party
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

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
-- Table structure for table `address_address`
--

DROP TABLE IF EXISTS `address_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street_number` varchar(20) NOT NULL,
  `route` varchar(100) NOT NULL,
  `raw` varchar(200) NOT NULL,
  `formatted` varchar(200) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `locality_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `address_address_locality_id_5dd79609_fk_address_locality_id` (`locality_id`),
  CONSTRAINT `address_address_locality_id_5dd79609_fk_address_locality_id` FOREIGN KEY (`locality_id`) REFERENCES `address_locality` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_address`
--

LOCK TABLES `address_address` WRITE;
/*!40000 ALTER TABLE `address_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_country`
--

DROP TABLE IF EXISTS `address_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `code` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_country`
--

LOCK TABLES `address_country` WRITE;
/*!40000 ALTER TABLE `address_country` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_locality`
--

DROP TABLE IF EXISTS `address_locality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_locality` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(165) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `state_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address_locality_name_postal_code_state_id_d1e927c2_uniq` (`name`,`postal_code`,`state_id`),
  KEY `address_locality_state_id_8dc32b8e_fk_address_state_id` (`state_id`),
  CONSTRAINT `address_locality_state_id_8dc32b8e_fk_address_state_id` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_locality`
--

LOCK TABLES `address_locality` WRITE;
/*!40000 ALTER TABLE `address_locality` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_locality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_state`
--

DROP TABLE IF EXISTS `address_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(165) NOT NULL,
  `code` varchar(3) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address_state_name_country_id_a46a5987_uniq` (`name`,`country_id`),
  KEY `address_state_country_id_0a4efd43_fk_address_country_id` (`country_id`),
  CONSTRAINT `address_state_country_id_0a4efd43_fk_address_country_id` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_state`
--

LOCK TABLES `address_state` WRITE;
/*!40000 ALTER TABLE `address_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'党辅'),(2,'支书'),(1,'普通成员');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,2),(2,1,4),(3,1,12),(4,1,14),(5,1,16),(6,1,20),(8,1,24),(10,1,28),(43,1,49),(44,1,50),(45,1,51),(46,1,52),(7,1,54),(9,1,56),(42,2,2),(11,2,3),(12,2,4),(14,2,12),(15,2,13),(16,2,14),(17,2,15),(18,2,16),(19,2,20),(20,2,21),(41,2,22),(22,2,24),(23,2,25),(24,2,26),(25,2,27),(26,2,28),(21,2,54),(13,2,56),(47,2,68),(27,3,4),(28,3,9),(29,3,10),(30,3,11),(31,3,12),(32,3,16),(33,3,20),(34,3,21),(35,3,22),(36,3,23),(37,3,24),(40,3,28),(38,3,54),(39,3,56),(48,3,65),(49,3,66),(50,3,67),(51,3,68);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add 我的账号',1,'add_user'),(2,'Can change 我的账号',1,'change_user'),(3,'Can delete 我的账号',1,'delete_user'),(4,'Can view 我的账号',1,'view_user'),(5,'Can add application',2,'add_application'),(6,'Can change application',2,'change_application'),(7,'Can delete application',2,'delete_application'),(8,'Can view application',2,'view_application'),(9,'Can add 党支部',3,'add_branch'),(10,'Can change 党支部',3,'change_branch'),(11,'Can delete 党支部',3,'delete_branch'),(12,'Can view 党支部',3,'view_branch'),(13,'Can add 成员信息',4,'add_member'),(14,'Can change 成员信息',4,'change_member'),(15,'Can delete 成员信息',4,'delete_member'),(16,'Can view 成员信息',4,'view_member'),(17,'Can add school',5,'add_school'),(18,'Can change school',5,'change_school'),(19,'Can delete school',5,'delete_school'),(20,'Can view school',5,'view_school'),(21,'Can add 党建活动',6,'add_activity'),(22,'Can change 党建活动',6,'change_activity'),(23,'Can delete 党建活动',6,'delete_activity'),(24,'Can view 党建活动',6,'view_activity'),(25,'Can add 学时统计',7,'add_takepartin'),(26,'Can change 学时统计',7,'change_takepartin'),(27,'Can delete 学时统计',7,'delete_takepartin'),(28,'Can view 学时统计',7,'view_takepartin'),(29,'Can add log entry',8,'add_logentry'),(30,'Can change log entry',8,'change_logentry'),(31,'Can delete log entry',8,'delete_logentry'),(32,'Can view log entry',8,'view_logentry'),(33,'Can add permission',9,'add_permission'),(34,'Can change permission',9,'change_permission'),(35,'Can delete permission',9,'delete_permission'),(36,'Can view permission',9,'view_permission'),(37,'Can add group',10,'add_group'),(38,'Can change group',10,'change_group'),(39,'Can delete group',10,'delete_group'),(40,'Can view group',10,'view_group'),(41,'Can add content type',11,'add_contenttype'),(42,'Can change content type',11,'change_contenttype'),(43,'Can delete content type',11,'delete_contenttype'),(44,'Can view content type',11,'view_contenttype'),(45,'Can add session',12,'add_session'),(46,'Can change session',12,'change_session'),(47,'Can delete session',12,'delete_session'),(48,'Can view session',12,'view_session'),(49,'Can add Bookmark',13,'add_bookmark'),(50,'Can change Bookmark',13,'change_bookmark'),(51,'Can delete Bookmark',13,'delete_bookmark'),(52,'Can view Bookmark',13,'view_bookmark'),(53,'Can add User Setting',14,'add_usersettings'),(54,'Can change User Setting',14,'change_usersettings'),(55,'Can delete User Setting',14,'delete_usersettings'),(56,'Can view User Setting',14,'view_usersettings'),(57,'Can add User Widget',15,'add_userwidget'),(58,'Can change User Widget',15,'change_userwidget'),(59,'Can delete User Widget',15,'delete_userwidget'),(60,'Can view User Widget',15,'view_userwidget'),(61,'Can add log entry',16,'add_log'),(62,'Can change log entry',16,'change_log'),(63,'Can delete log entry',16,'delete_log'),(64,'Can view log entry',16,'view_log'),(65,'Can add 发展流程依赖',17,'add_dependency'),(66,'Can change 发展流程依赖',17,'change_dependency'),(67,'Can delete 发展流程依赖',17,'delete_dependency'),(68,'Can view 发展流程依赖',17,'view_dependency');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_user_username` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1086 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2019-02-09 23:06:24.899682','16337109','计算机本科生第二党支部 柯司博',1,'new through import_export',4,'000000'),(2,'2019-02-09 23:06:24.900453','16337113','计算机本科生第二党支部 劳马东',1,'new through import_export',4,'000000'),(3,'2019-02-09 23:06:24.900882','17341061','计算机本科生第二党支部 黄勇',1,'new through import_export',4,'000000'),(4,'2019-02-09 23:06:24.901242','15336117','计算机本科生第二党支部 刘展宏',1,'new through import_export',4,'000000'),(5,'2019-02-09 23:06:24.901626','15336141','计算机本科生第二党支部 彭博东',1,'new through import_export',4,'000000'),(6,'2019-02-09 23:06:24.901985','15336095','计算机本科生第二党支部 梁沛霖',1,'new through import_export',4,'000000'),(7,'2019-02-09 23:06:24.902321','15336101','计算机本科生第二党支部 林建涛',1,'new through import_export',4,'000000'),(8,'2019-02-09 23:06:24.902657','15336102','计算机本科生第二党支部 林民钊',1,'new through import_export',4,'000000'),(9,'2019-02-09 23:06:24.903011','15336121','计算机本科生第二党支部 陆剑',1,'new through import_export',4,'000000'),(10,'2019-02-09 23:06:24.903345','16337071','计算机本科生第二党支部 郭如意',1,'new through import_export',4,'000000'),(11,'2019-02-09 23:06:24.903678','16337098','计算机本科生第二党支部 黄义凯',1,'new through import_export',4,'000000'),(12,'2019-02-09 23:06:24.904025','16337108','计算机本科生第二党支部 金牧',1,'new through import_export',4,'000000'),(13,'2019-02-09 23:06:24.904356','15336142','计算机本科生第二党支部 彭诗煜',1,'new through import_export',4,'000000'),(14,'2019-02-09 23:06:24.904684','16337094','计算机本科生第二党支部 黄凯欢',1,'new through import_export',4,'000000'),(15,'2019-02-09 23:06:24.905127','16337099','计算机本科生第二党支部 黄亦安',1,'new through import_export',4,'000000'),(16,'2019-02-09 23:06:24.905501','16337106','计算机本科生第二党支部 解锐',1,'new through import_export',4,'000000'),(17,'2019-02-09 23:06:24.905856','16337112','计算机本科生第二党支部 兰楠',1,'new through import_export',4,'000000'),(18,'2019-02-09 23:06:24.906192','16337129','计算机本科生第二党支部 李智源',1,'new through import_export',4,'000000'),(19,'2019-02-09 23:06:24.906521','16337154','计算机本科生第二党支部 刘海',1,'new through import_export',4,'000000'),(20,'2019-02-09 23:06:24.906869','17341073','计算机本科生第二党支部 蓝靖瑜',1,'new through import_export',4,'000000'),(21,'2019-02-09 23:06:24.907204','17341074','计算机本科生第二党支部 蓝煜航',1,'new through import_export',4,'000000'),(22,'2019-02-09 23:06:24.907534','17341095','计算机本科生第二党支部 廖德洋',1,'new through import_export',4,'000000'),(23,'2019-02-09 23:06:24.907881','17341096','计算机本科生第二党支部 廖浩淳',1,'new through import_export',4,'000000'),(24,'2019-02-09 23:06:24.908216','17341097','计算机本科生第二党支部 廖永滨',1,'new through import_export',4,'000000'),(25,'2019-02-09 23:06:24.908545','17341099','计算机本科生第二党支部 廖泽祥',1,'new through import_export',4,'000000'),(26,'2019-02-09 23:06:24.908897','17341105','计算机本科生第二党支部 刘晨飞',1,'new through import_export',4,'000000'),(27,'2019-02-09 23:06:24.909233','17341114','计算机本科生第二党支部 刘雨萱',1,'new through import_export',4,'000000'),(28,'2019-02-09 23:06:24.909603','17341117','计算机本科生第二党支部 卢曼宁',1,'new through import_export',4,'000000'),(29,'2019-02-09 23:06:24.909953','18340069','计算机本科生第二党支部 黄轩腾',1,'new through import_export',4,'000000'),(30,'2019-02-09 23:06:24.910287','18340075','计算机本科生第二党支部 黄卓燊',1,'new through import_export',4,'000000'),(31,'2019-02-09 23:06:24.910617','18340076','计算机本科生第二党支部 黄子聿',1,'new through import_export',4,'000000'),(32,'2019-02-09 23:14:24.325373','32','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 柯司博',1,'new through import_export',7,'16337113'),(33,'2019-02-09 23:14:24.325938','33','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 劳马东',1,'new through import_export',7,'16337113'),(34,'2019-02-09 23:14:24.326316','34','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄勇',1,'new through import_export',7,'16337113'),(35,'2019-02-09 23:14:24.326693','35','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 刘展宏',1,'new through import_export',7,'16337113'),(36,'2019-02-09 23:14:24.327114','36','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 彭博东',1,'new through import_export',7,'16337113'),(37,'2019-02-09 23:14:24.327491','37','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 梁沛霖',1,'new through import_export',7,'16337113'),(38,'2019-02-09 23:14:24.327916','38','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 林建涛',1,'new through import_export',7,'16337113'),(39,'2019-02-09 23:14:24.328272','39','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 林民钊',1,'new through import_export',7,'16337113'),(40,'2019-02-09 23:14:24.328616','40','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 陆剑',1,'new through import_export',7,'16337113'),(41,'2019-02-09 23:14:24.329017','41','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 郭如意',1,'new through import_export',7,'16337113'),(42,'2019-02-09 23:14:24.329440','42','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄义凯',1,'new through import_export',7,'16337113'),(43,'2019-02-09 23:14:24.329826','43','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 金牧',1,'new through import_export',7,'16337113'),(44,'2019-02-09 23:14:24.330187','44','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 彭诗煜',1,'new through import_export',7,'16337113'),(45,'2019-02-09 23:14:24.330527','45','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄凯欢',1,'new through import_export',7,'16337113'),(46,'2019-02-09 23:14:24.330912','46','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄亦安',1,'new through import_export',7,'16337113'),(47,'2019-02-09 23:14:24.331262','47','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 解锐',1,'new through import_export',7,'16337113'),(48,'2019-02-09 23:14:24.331601','48','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 兰楠',1,'new through import_export',7,'16337113'),(49,'2019-02-09 23:14:24.331991','49','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 李智源',1,'new through import_export',7,'16337113'),(50,'2019-02-09 23:14:24.332336','50','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 刘海',1,'new through import_export',7,'16337113'),(51,'2019-02-09 23:14:24.332671','51','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 蓝靖瑜',1,'new through import_export',7,'16337113'),(52,'2019-02-09 23:14:24.333098','52','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 蓝煜航',1,'new through import_export',7,'16337113'),(53,'2019-02-09 23:14:24.333594','53','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 廖德洋',1,'new through import_export',7,'16337113'),(54,'2019-02-09 23:14:24.333994','54','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 廖浩淳',1,'new through import_export',7,'16337113'),(55,'2019-02-09 23:14:24.334347','55','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 廖永滨',1,'new through import_export',7,'16337113'),(56,'2019-02-09 23:14:24.334687','56','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 廖泽祥',1,'new through import_export',7,'16337113'),(57,'2019-02-09 23:14:24.335072','57','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 刘晨飞',1,'new through import_export',7,'16337113'),(58,'2019-02-09 23:14:24.335420','58','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 刘雨萱',1,'new through import_export',7,'16337113'),(59,'2019-02-09 23:14:24.335767','59','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 卢曼宁',1,'new through import_export',7,'16337113'),(60,'2019-02-09 23:14:24.336148','60','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄轩腾',1,'new through import_export',7,'16337113'),(61,'2019-02-09 23:14:24.336497','61','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄卓燊',1,'new through import_export',7,'16337113'),(62,'2019-02-09 23:14:24.336850','62','组织生活会(2019-01-03 20:00:00): 计算机本科生第二党支部 黄子聿',1,'new through import_export',7,'16337113'),(63,'2019-02-10 18:33:27.577068','406','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(64,'2019-02-10 18:33:27.577657','407','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(65,'2019-02-10 18:33:27.578077','408','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(66,'2019-02-10 18:33:27.578446','409','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(67,'2019-02-10 18:33:27.578830','410','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(68,'2019-02-10 18:33:27.579225','411','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(69,'2019-02-10 18:33:27.579710','412','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(70,'2019-02-10 18:33:27.580080','413','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(71,'2019-02-10 18:33:27.580495','414','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(72,'2019-02-10 18:33:27.580901','415','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(73,'2019-02-10 18:33:27.581314','416','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(74,'2019-02-10 18:33:27.581715','417','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(75,'2019-02-10 18:33:27.582102','418','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(76,'2019-02-10 18:33:27.582493','419','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(77,'2019-02-10 18:33:27.582921','420','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(78,'2019-02-10 18:33:27.583352','421','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(79,'2019-02-10 18:33:27.583780','422','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(80,'2019-02-10 18:33:27.584174','423','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(81,'2019-02-10 18:33:27.584579','424','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(82,'2019-02-10 18:33:27.585023','425','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(83,'2019-02-10 18:33:27.585443','426','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(84,'2019-02-10 18:33:27.585862','427','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(85,'2019-02-10 18:33:27.586248','428','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(86,'2019-02-10 18:33:27.586607','429','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(87,'2019-02-10 18:33:27.587013','430','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(88,'2019-02-10 18:33:27.587421','431','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(89,'2019-02-10 18:33:27.587851','432','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(90,'2019-02-10 18:33:27.588253','433','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(91,'2019-02-10 18:33:27.588642','434','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(92,'2019-02-10 18:33:27.589026','435','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(93,'2019-02-10 18:33:27.589454','436','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(94,'2019-02-10 18:35:52.833251','468','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(95,'2019-02-10 18:35:52.833847','469','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(96,'2019-02-10 18:35:52.834284','470','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(97,'2019-02-10 18:35:52.834656','471','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(98,'2019-02-10 18:35:52.835052','472','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(99,'2019-02-10 18:35:52.835409','473','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(100,'2019-02-10 18:35:52.835809','474','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(101,'2019-02-10 18:35:52.836253','475','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(102,'2019-02-10 18:35:52.836612','476','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(103,'2019-02-10 18:35:52.837007','477','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(104,'2019-02-10 18:35:52.837424','478','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(105,'2019-02-10 18:35:52.837835','479','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(106,'2019-02-10 18:35:52.840645','480','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(107,'2019-02-10 18:35:52.842062','481','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(108,'2019-02-10 18:35:52.842479','482','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(109,'2019-02-10 18:35:52.842943','483','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(110,'2019-02-10 18:35:52.843452','484','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(111,'2019-02-10 18:35:52.843900','485','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(112,'2019-02-10 18:35:52.844356','486','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(113,'2019-02-10 18:35:52.844739','487','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(114,'2019-02-10 18:35:52.845113','488','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(115,'2019-02-10 18:35:52.845512','489','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(116,'2019-02-10 18:35:52.845906','490','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(117,'2019-02-10 18:35:52.846290','491','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(118,'2019-02-10 18:35:52.846721','492','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(119,'2019-02-10 18:35:52.847091','493','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(120,'2019-02-10 18:35:52.847611','494','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(121,'2019-02-10 18:35:52.848026','495','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(122,'2019-02-10 18:35:52.848382','496','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(123,'2019-02-10 18:35:52.848746','497','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(124,'2019-02-10 18:35:52.849099','498','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(125,'2019-02-10 19:44:04.886665','530','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(126,'2019-02-10 19:44:04.887241','531','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(127,'2019-02-10 19:44:04.887659','532','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(128,'2019-02-10 19:44:04.888035','533','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(129,'2019-02-10 19:44:04.888384','534','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(130,'2019-02-10 19:44:04.888736','535','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(131,'2019-02-10 19:44:04.889085','536','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(132,'2019-02-10 19:44:04.889478','537','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(133,'2019-02-10 19:44:04.889864','538','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(134,'2019-02-10 19:44:04.890217','539','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(135,'2019-02-10 19:44:04.890564','540','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(136,'2019-02-10 19:44:04.890922','541','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(137,'2019-02-10 19:44:04.891264','542','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(138,'2019-02-10 19:44:04.891598','543','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(139,'2019-02-10 19:44:04.891952','544','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(140,'2019-02-10 19:44:04.892311','545','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(141,'2019-02-10 19:44:04.892648','546','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(142,'2019-02-10 19:44:04.893042','547','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(143,'2019-02-10 19:44:04.893417','548','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(144,'2019-02-10 19:44:04.893775','549','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(145,'2019-02-10 19:44:04.894122','550','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(146,'2019-02-10 19:44:04.894458','551','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(147,'2019-02-10 19:44:04.894807','552','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(148,'2019-02-10 19:44:04.895147','553','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(149,'2019-02-10 19:44:04.895482','554','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(150,'2019-02-10 19:44:04.895834','555','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(151,'2019-02-10 19:44:04.896172','556','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(152,'2019-02-10 19:44:04.896506','557','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(153,'2019-02-10 19:44:04.896859','558','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(154,'2019-02-10 19:44:04.897200','559','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(155,'2019-02-10 19:44:04.897575','560','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(156,'2019-02-10 19:51:17.118876','592','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(157,'2019-02-10 19:51:17.119448','593','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(158,'2019-02-10 19:51:17.119841','594','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(159,'2019-02-10 19:51:17.120195','595','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(160,'2019-02-10 19:51:17.120538','596','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(161,'2019-02-10 19:51:17.120895','597','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(162,'2019-02-10 19:51:17.121234','598','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(163,'2019-02-10 19:51:17.121616','599','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(164,'2019-02-10 19:51:17.121971','600','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(165,'2019-02-10 19:51:17.122312','601','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(166,'2019-02-10 19:51:17.122649','602','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(167,'2019-02-10 19:51:17.123002','603','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(168,'2019-02-10 19:51:17.123339','604','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(169,'2019-02-10 19:51:17.123674','605','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(170,'2019-02-10 19:51:17.124027','606','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(171,'2019-02-10 19:51:17.124362','607','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(172,'2019-02-10 19:51:17.124700','608','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(173,'2019-02-10 19:51:17.125055','609','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(174,'2019-02-10 19:51:17.125430','610','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(175,'2019-02-10 19:51:17.128490','611','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(176,'2019-02-10 19:51:17.129240','612','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(177,'2019-02-10 19:51:17.129754','613','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(178,'2019-02-10 19:51:17.130126','614','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(179,'2019-02-10 19:51:17.130469','615','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(180,'2019-02-10 19:51:17.130823','616','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(181,'2019-02-10 19:51:17.131165','617','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(182,'2019-02-10 19:51:17.131504','618','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(183,'2019-02-10 19:51:17.131891','619','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(184,'2019-02-10 19:51:17.132244','620','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(185,'2019-02-10 19:51:17.132579','621','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(186,'2019-02-10 19:51:17.132935','622','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(187,'2019-02-10 19:59:56.488216','655','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(188,'2019-02-10 19:59:56.488713','656','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(189,'2019-02-10 19:59:56.489093','657','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(190,'2019-02-10 19:59:56.489488','658','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(191,'2019-02-10 19:59:56.493015','659','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(192,'2019-02-10 19:59:56.493418','660','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(193,'2019-02-10 19:59:56.493770','661','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(194,'2019-02-10 19:59:56.494124','662','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(195,'2019-02-10 19:59:56.494456','663','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(196,'2019-02-10 19:59:56.494787','664','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(197,'2019-02-10 19:59:56.495132','665','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(198,'2019-02-10 19:59:56.495461','666','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(199,'2019-02-10 19:59:56.495788','667','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(200,'2019-02-10 19:59:56.496131','668','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(201,'2019-02-10 19:59:56.496459','669','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(202,'2019-02-10 19:59:56.496835','670','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(203,'2019-02-10 19:59:56.497169','671','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(204,'2019-02-10 19:59:56.497518','672','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(205,'2019-02-10 19:59:56.497862','673','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(206,'2019-02-10 19:59:56.498194','674','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(207,'2019-02-10 19:59:56.498520','675','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(208,'2019-02-10 19:59:56.498859','676','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(209,'2019-02-10 19:59:56.499214','677','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(210,'2019-02-10 19:59:56.499543','678','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(211,'2019-02-10 19:59:56.499888','679','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(212,'2019-02-10 19:59:56.500220','680','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(213,'2019-02-10 19:59:56.500586','681','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(214,'2019-02-10 19:59:56.500941','682','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(215,'2019-02-10 19:59:56.501294','683','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(216,'2019-02-10 19:59:56.501629','684','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(217,'2019-02-10 19:59:56.501975','685','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(218,'2019-02-10 20:08:21.212949','717','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(219,'2019-02-10 20:08:21.213533','718','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(220,'2019-02-10 20:08:21.213922','719','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(221,'2019-02-10 20:08:21.214273','720','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(222,'2019-02-10 20:08:21.214620','721','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(223,'2019-02-10 20:08:21.214976','722','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(224,'2019-02-10 20:08:21.215315','723','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(225,'2019-02-10 20:08:21.215648','724','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(226,'2019-02-10 20:08:21.216004','725','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(227,'2019-02-10 20:08:21.216338','726','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(228,'2019-02-10 20:08:21.216668','727','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(229,'2019-02-10 20:08:21.217022','728','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(230,'2019-02-10 20:08:21.217394','729','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(231,'2019-02-10 20:08:21.217737','730','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(232,'2019-02-10 20:08:21.218092','731','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(233,'2019-02-10 20:08:21.218427','732','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(234,'2019-02-10 20:08:21.218760','733','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(235,'2019-02-10 20:08:21.219108','734','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(236,'2019-02-10 20:08:21.219443','735','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(237,'2019-02-10 20:08:21.219774','736','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(238,'2019-02-10 20:08:21.220125','737','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(239,'2019-02-10 20:08:21.220457','738','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(240,'2019-02-10 20:08:21.220789','739','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(241,'2019-02-10 20:08:21.221138','740','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(242,'2019-02-10 20:08:21.221504','741','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(243,'2019-02-10 20:08:21.221851','742','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(244,'2019-02-10 20:08:21.222213','743','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(245,'2019-02-10 20:08:21.222549','744','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(246,'2019-02-10 20:08:21.222897','745','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(247,'2019-02-10 20:08:21.223234','746','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(248,'2019-02-10 20:08:21.223566','747','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(249,'2019-02-10 20:11:29.635253','779','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(250,'2019-02-10 20:11:29.635750','780','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(251,'2019-02-10 20:11:29.636170','781','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(252,'2019-02-10 20:11:29.636529','782','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(253,'2019-02-10 20:11:29.636902','783','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(254,'2019-02-10 20:11:29.637306','784','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(255,'2019-02-10 20:11:29.637664','785','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(256,'2019-02-10 20:11:29.638078','786','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(257,'2019-02-10 20:11:29.638441','787','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(258,'2019-02-10 20:11:29.638798','788','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(259,'2019-02-10 20:11:29.639199','789','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(260,'2019-02-10 20:11:29.639555','790','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(261,'2019-02-10 20:11:29.639944','791','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(262,'2019-02-10 20:11:29.640329','792','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(263,'2019-02-10 20:11:29.640686','793','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(264,'2019-02-10 20:11:29.641076','794','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(265,'2019-02-10 20:11:29.641475','795','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(266,'2019-02-10 20:11:29.641868','796','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(267,'2019-02-10 20:11:29.642230','797','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(268,'2019-02-10 20:11:29.642605','798','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(269,'2019-02-10 20:11:29.642992','799','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(270,'2019-02-10 20:11:29.643370','800','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(271,'2019-02-10 20:11:29.643747','801','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(272,'2019-02-10 20:11:29.644133','802','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(273,'2019-02-10 20:11:29.644488','803','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(274,'2019-02-10 20:11:29.644894','804','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(275,'2019-02-10 20:11:29.645318','805','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(276,'2019-02-10 20:11:29.645731','806','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(277,'2019-02-10 20:11:29.646129','807','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(278,'2019-02-10 20:11:29.648904','808','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(279,'2019-02-10 20:11:29.651531','809','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(373,'2019-02-10 20:20:05.290595','1027','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(374,'2019-02-10 20:20:05.291142','1028','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(375,'2019-02-10 20:20:05.291544','1029','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(376,'2019-02-10 20:20:05.291924','1030','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(377,'2019-02-10 20:20:05.292284','1031','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(378,'2019-02-10 20:20:05.292638','1032','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(379,'2019-02-10 20:20:05.293053','1033','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(380,'2019-02-10 20:20:05.293442','1034','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(381,'2019-02-10 20:20:05.293835','1035','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(382,'2019-02-10 20:20:05.294204','1036','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(383,'2019-02-10 20:20:05.294558','1037','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(384,'2019-02-10 20:20:05.294998','1038','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(385,'2019-02-10 20:20:05.295359','1039','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(386,'2019-02-10 20:20:05.295721','1040','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(387,'2019-02-10 20:20:05.296132','1041','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(388,'2019-02-10 20:20:05.296493','1042','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(389,'2019-02-10 20:20:05.296888','1043','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(390,'2019-02-10 20:20:05.297253','1044','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(391,'2019-02-10 20:20:05.297632','1045','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(392,'2019-02-10 20:20:05.298022','1046','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(393,'2019-02-10 20:20:05.298378','1047','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(394,'2019-02-10 20:20:05.298756','1048','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(395,'2019-02-10 20:20:05.299173','1049','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(396,'2019-02-10 20:20:05.299544','1050','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(397,'2019-02-10 20:20:05.299943','1051','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(398,'2019-02-10 20:20:05.300306','1052','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(399,'2019-02-10 20:20:05.300660','1053','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(400,'2019-02-10 20:20:05.301051','1054','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(401,'2019-02-10 20:20:05.301426','1055','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(402,'2019-02-10 20:20:05.301784','1056','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(403,'2019-02-10 20:20:05.302153','1057','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(404,'2019-02-10 20:21:15.155612','1089','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(405,'2019-02-10 20:21:15.156138','1090','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(406,'2019-02-10 20:21:15.156526','1091','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(407,'2019-02-10 20:21:15.156908','1092','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(408,'2019-02-10 20:21:15.157314','1093','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(409,'2019-02-10 20:21:15.157719','1094','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(410,'2019-02-10 20:21:15.158104','1095','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(411,'2019-02-10 20:21:15.158468','1096','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(412,'2019-02-10 20:21:15.158841','1097','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(413,'2019-02-10 20:21:15.159206','1098','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(414,'2019-02-10 20:21:15.159567','1099','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(415,'2019-02-10 20:21:15.162471','1100','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(416,'2019-02-10 20:21:15.162891','1101','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(417,'2019-02-10 20:21:15.163326','1102','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(418,'2019-02-10 20:21:15.163706','1103','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(419,'2019-02-10 20:21:15.164087','1104','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(420,'2019-02-10 20:21:15.164451','1105','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(421,'2019-02-10 20:21:15.164812','1106','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(422,'2019-02-10 20:21:15.165192','1107','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(423,'2019-02-10 20:21:15.165584','1108','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(424,'2019-02-10 20:21:15.165965','1109','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(425,'2019-02-10 20:21:15.166330','1110','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(426,'2019-02-10 20:21:15.166691','1111','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(427,'2019-02-10 20:21:15.167073','1112','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(428,'2019-02-10 20:21:15.167434','1113','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(429,'2019-02-10 20:21:15.167794','1114','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(430,'2019-02-10 20:21:15.168173','1115','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(431,'2019-02-10 20:21:15.168534','1116','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(432,'2019-02-10 20:21:15.168909','1117','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(433,'2019-02-10 20:21:15.169292','1118','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(434,'2019-02-10 20:21:15.169683','1119','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(466,'2019-02-10 20:46:13.417753','1213','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(467,'2019-02-10 20:46:13.418476','1214','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(468,'2019-02-10 20:46:13.418893','1215','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(469,'2019-02-10 20:46:13.419265','1216','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(470,'2019-02-10 20:46:13.419634','1217','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(471,'2019-02-10 20:46:13.420011','1218','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(472,'2019-02-10 20:46:13.420366','1219','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(473,'2019-02-10 20:46:13.420773','1220','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(474,'2019-02-10 20:46:13.421168','1221','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(475,'2019-02-10 20:46:13.421588','1222','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(476,'2019-02-10 20:46:13.421970','1223','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(477,'2019-02-10 20:46:13.422333','1224','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(478,'2019-02-10 20:46:13.422687','1225','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(479,'2019-02-10 20:46:13.423060','1226','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(480,'2019-02-10 20:46:13.423420','1227','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(481,'2019-02-10 20:46:13.423879','1228','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(482,'2019-02-10 20:46:13.424263','1229','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(483,'2019-02-10 20:46:13.424660','1230','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(484,'2019-02-10 20:46:13.425055','1231','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(485,'2019-02-10 20:46:13.425451','1232','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(486,'2019-02-10 20:46:13.425849','1233','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(487,'2019-02-10 20:46:13.426220','1234','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(488,'2019-02-10 20:46:13.426578','1235','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(489,'2019-02-10 20:46:13.426975','1236','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(490,'2019-02-10 20:46:13.427371','1237','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(491,'2019-02-10 20:46:13.427739','1238','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(492,'2019-02-10 20:46:13.428152','1239','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(493,'2019-02-10 20:46:13.428515','1240','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(494,'2019-02-10 20:46:13.428922','1241','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(495,'2019-02-10 20:46:13.429377','1242','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(496,'2019-02-10 20:46:13.429743','1243','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(497,'2019-02-10 20:52:02.885705','1306','组织生活会(33): 16337109 柯司博',1,'new through import_export',7,'16337113'),(498,'2019-02-10 20:52:02.886331','1307','组织生活会(33): 16337113 劳马东',1,'new through import_export',7,'16337113'),(499,'2019-02-10 20:52:02.886738','1308','组织生活会(33): 17341061 黄勇',1,'new through import_export',7,'16337113'),(500,'2019-02-10 20:52:02.887216','1309','组织生活会(33): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(501,'2019-02-10 20:52:02.887653','1310','组织生活会(33): 15336141 彭博东',1,'new through import_export',7,'16337113'),(502,'2019-02-10 20:52:02.888098','1311','组织生活会(33): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(503,'2019-02-10 20:52:02.888552','1312','组织生活会(33): 15336101 林建涛',1,'new through import_export',7,'16337113'),(504,'2019-02-10 20:52:02.888958','1313','组织生活会(33): 15336102 林民钊',1,'new through import_export',7,'16337113'),(505,'2019-02-10 20:52:02.889355','1314','组织生活会(33): 15336121 陆剑',1,'new through import_export',7,'16337113'),(506,'2019-02-10 20:52:02.889775','1315','组织生活会(33): 16337071 郭如意',1,'new through import_export',7,'16337113'),(507,'2019-02-10 20:52:02.890252','1316','组织生活会(33): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(508,'2019-02-10 20:52:02.890658','1317','组织生活会(33): 16337108 金牧',1,'new through import_export',7,'16337113'),(509,'2019-02-10 20:52:02.891064','1318','组织生活会(33): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(510,'2019-02-10 20:52:02.891519','1319','组织生活会(33): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(511,'2019-02-10 20:52:02.891940','1320','组织生活会(33): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(512,'2019-02-10 20:52:02.892347','1321','组织生活会(33): 16337106 解锐',1,'new through import_export',7,'16337113'),(513,'2019-02-10 20:52:02.892730','1322','组织生活会(33): 16337112 兰楠',1,'new through import_export',7,'16337113'),(514,'2019-02-10 20:52:02.893164','1323','组织生活会(33): 16337129 李智源',1,'new through import_export',7,'16337113'),(515,'2019-02-10 20:52:02.893602','1324','组织生活会(33): 16337154 刘海',1,'new through import_export',7,'16337113'),(516,'2019-02-10 20:52:02.894012','1325','组织生活会(33): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(517,'2019-02-10 20:52:02.894392','1326','组织生活会(33): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(518,'2019-02-10 20:52:02.894759','1327','组织生活会(33): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(519,'2019-02-10 20:52:02.895166','1328','组织生活会(33): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(520,'2019-02-10 20:52:02.895532','1329','组织生活会(33): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(521,'2019-02-10 20:52:02.895988','1330','组织生活会(33): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(522,'2019-02-10 20:52:02.896386','1331','组织生活会(33): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(523,'2019-02-10 20:52:02.896751','1332','组织生活会(33): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(524,'2019-02-10 20:52:02.897180','1333','组织生活会(33): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(525,'2019-02-10 20:52:02.897580','1334','组织生活会(33): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(526,'2019-02-10 20:52:02.897995','1335','组织生活会(33): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(527,'2019-02-10 20:52:02.898432','1336','组织生活会(33): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(528,'2019-02-10 21:16:25.837144','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(529,'2019-02-10 21:16:25.837673','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(530,'2019-02-10 21:16:25.838064','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(531,'2019-02-10 21:16:25.838414','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(532,'2019-02-10 21:16:25.838755','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(533,'2019-02-10 21:16:25.839117','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(534,'2019-02-10 21:16:25.839455','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(535,'2019-02-10 21:16:25.839815','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(536,'2019-02-10 21:16:25.840212','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(537,'2019-02-10 21:16:25.840560','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(538,'2019-02-10 21:16:25.840975','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(539,'2019-02-10 21:16:25.841431','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(540,'2019-02-10 21:16:25.841794','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(541,'2019-02-10 21:16:25.842145','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(542,'2019-02-10 21:16:25.842483','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(543,'2019-02-10 21:16:25.842834','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(544,'2019-02-10 21:16:25.843177','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(545,'2019-02-10 21:16:25.843516','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(546,'2019-02-10 21:16:25.843865','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(547,'2019-02-10 21:16:25.844203','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(548,'2019-02-10 21:16:25.844536','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(549,'2019-02-10 21:16:25.844891','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(550,'2019-02-10 21:16:25.845231','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(551,'2019-02-10 21:16:25.845589','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(552,'2019-02-10 21:16:25.845981','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(553,'2019-02-10 21:16:25.846390','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(554,'2019-02-10 21:16:25.846734','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(555,'2019-02-10 21:16:25.847156','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(556,'2019-02-10 21:16:25.847508','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(557,'2019-02-10 21:16:25.847865','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(558,'2019-02-10 21:16:25.848209','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(559,'2019-02-10 21:19:30.131627','32','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(560,'2019-02-10 21:19:30.132076','33','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(561,'2019-02-10 21:19:30.132435','34','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(562,'2019-02-10 21:19:30.132773','35','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(563,'2019-02-10 21:19:30.133130','36','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(564,'2019-02-10 21:19:30.133490','37','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(565,'2019-02-10 21:19:30.133838','38','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(566,'2019-02-10 21:19:30.134177','39','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(567,'2019-02-10 21:19:30.134512','40','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(568,'2019-02-10 21:19:30.134856','41','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(569,'2019-02-10 21:19:30.135194','42','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(570,'2019-02-10 21:19:30.135527','43','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(571,'2019-02-10 21:19:30.135875','44','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(572,'2019-02-10 21:19:30.136211','45','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(573,'2019-02-10 21:19:30.136542','46','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(574,'2019-02-10 21:19:30.136959','47','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(575,'2019-02-10 21:19:30.137312','48','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(576,'2019-02-10 21:19:30.137650','49','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(577,'2019-02-10 21:19:30.138003','50','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(578,'2019-02-10 21:19:30.138337','51','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(579,'2019-02-10 21:19:30.138671','52','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(580,'2019-02-10 21:19:30.139019','53','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(581,'2019-02-10 21:19:30.139396','54','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(582,'2019-02-10 21:19:30.139744','55','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(583,'2019-02-10 21:19:30.140100','56','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(584,'2019-02-10 21:19:30.140439','57','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(585,'2019-02-10 21:19:30.140774','58','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(586,'2019-02-10 21:19:30.141124','59','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(587,'2019-02-10 21:19:30.141477','60','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(588,'2019-02-10 21:19:30.141823','61','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(589,'2019-02-10 21:19:30.142158','62','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(590,'2019-02-10 21:21:16.221490','94','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(591,'2019-02-10 21:21:16.222048','95','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(592,'2019-02-10 21:21:16.222468','96','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(593,'2019-02-10 21:21:16.222863','97','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(594,'2019-02-10 21:21:16.223242','98','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(595,'2019-02-10 21:21:16.223591','99','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(596,'2019-02-10 21:21:16.223975','100','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(597,'2019-02-10 21:21:16.224353','101','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(598,'2019-02-10 21:21:16.224699','102','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(599,'2019-02-10 21:21:16.225102','103','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(600,'2019-02-10 21:21:16.225501','104','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(601,'2019-02-10 21:21:16.225898','105','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(602,'2019-02-10 21:21:16.226271','106','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(603,'2019-02-10 21:21:16.226650','107','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(604,'2019-02-10 21:21:16.227015','108','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(605,'2019-02-10 21:21:16.227411','109','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(606,'2019-02-10 21:21:16.227773','110','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(607,'2019-02-10 21:21:16.228198','111','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(608,'2019-02-10 21:21:16.228584','112','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(609,'2019-02-10 21:21:16.229025','113','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(610,'2019-02-10 21:21:16.229426','114','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(611,'2019-02-10 21:21:16.229892','115','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(612,'2019-02-10 21:21:16.230332','116','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(613,'2019-02-10 21:21:16.230736','117','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(614,'2019-02-10 21:21:16.231239','118','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(615,'2019-02-10 21:21:16.231763','119','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(616,'2019-02-10 21:21:16.232184','120','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(617,'2019-02-10 21:21:16.232560','121','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(618,'2019-02-10 21:21:16.232937','122','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(619,'2019-02-10 21:21:16.233345','123','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(620,'2019-02-10 21:21:16.233851','124','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(621,'2019-02-10 22:57:05.775284','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(622,'2019-02-10 22:57:05.775867','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(623,'2019-02-10 22:57:05.776257','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(624,'2019-02-10 22:57:05.776626','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(625,'2019-02-10 22:57:05.777006','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(626,'2019-02-10 22:57:05.777401','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(627,'2019-02-10 22:57:05.777780','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(628,'2019-02-10 22:57:05.778185','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(629,'2019-02-10 22:57:05.778562','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(630,'2019-02-10 22:57:05.778973','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(631,'2019-02-10 22:57:05.779346','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(632,'2019-02-10 22:57:05.779755','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(633,'2019-02-10 22:57:05.780134','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(634,'2019-02-10 22:57:05.780491','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(635,'2019-02-10 22:57:05.780909','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(636,'2019-02-10 22:57:05.781339','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(637,'2019-02-10 22:57:05.781706','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(638,'2019-02-10 22:57:05.782135','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(639,'2019-02-10 22:57:05.782498','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(640,'2019-02-10 22:57:05.782889','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(641,'2019-02-10 22:57:05.783251','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(642,'2019-02-10 22:57:05.783604','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(643,'2019-02-10 22:57:05.784017','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(644,'2019-02-10 22:57:05.784384','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(645,'2019-02-10 22:57:05.784741','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(646,'2019-02-10 22:57:05.785114','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(647,'2019-02-10 22:57:05.785500','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(648,'2019-02-10 22:57:05.785877','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(649,'2019-02-10 22:57:05.786238','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(650,'2019-02-10 22:57:05.786591','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(651,'2019-02-10 22:57:05.786962','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(652,'2019-02-10 23:00:48.115754','32','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(653,'2019-02-10 23:00:48.116292','33','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(654,'2019-02-10 23:00:48.116715','34','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(655,'2019-02-10 23:00:48.117117','35','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(656,'2019-02-10 23:00:48.117529','36','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(657,'2019-02-10 23:00:48.117965','37','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(658,'2019-02-10 23:00:48.118336','38','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(659,'2019-02-10 23:00:48.118733','39','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(660,'2019-02-10 23:00:48.119121','40','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(661,'2019-02-10 23:00:48.119484','41','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(662,'2019-02-10 23:00:48.119905','42','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(663,'2019-02-10 23:00:48.120277','43','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(664,'2019-02-10 23:00:48.120640','44','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(665,'2019-02-10 23:00:48.121069','45','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(666,'2019-02-10 23:00:48.121467','46','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(667,'2019-02-10 23:00:48.121881','47','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(668,'2019-02-10 23:00:48.122261','48','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(669,'2019-02-10 23:00:48.122625','49','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(670,'2019-02-10 23:00:48.123049','50','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(671,'2019-02-10 23:00:48.123419','51','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(672,'2019-02-10 23:00:48.123797','52','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(673,'2019-02-10 23:00:48.124251','53','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(674,'2019-02-10 23:00:48.124619','54','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(675,'2019-02-10 23:00:48.125032','55','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(676,'2019-02-10 23:00:48.125440','56','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(677,'2019-02-10 23:00:48.125820','57','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(678,'2019-02-10 23:00:48.126240','58','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(679,'2019-02-10 23:00:48.126607','59','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(680,'2019-02-10 23:00:48.127011','60','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(681,'2019-02-10 23:00:48.127397','61','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(682,'2019-02-10 23:00:48.127760','62','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(683,'2019-02-11 14:00:38.531521','32','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(684,'2019-02-11 14:00:38.532022','33','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(685,'2019-02-11 14:00:38.532532','34','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(686,'2019-02-11 14:00:38.532893','35','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(687,'2019-02-11 14:00:38.533236','36','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(688,'2019-02-11 14:00:38.533644','37','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(689,'2019-02-11 14:00:38.533990','38','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(690,'2019-02-11 14:00:38.534329','39','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(691,'2019-02-11 14:00:38.534684','40','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(692,'2019-02-11 14:00:38.535021','41','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(693,'2019-02-11 14:00:38.535355','42','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(694,'2019-02-11 14:00:38.535708','43','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(695,'2019-02-11 14:00:38.536042','44','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(696,'2019-02-11 14:00:38.536375','45','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(697,'2019-02-11 14:00:38.536727','46','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(698,'2019-02-11 14:00:38.537059','47','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(699,'2019-02-11 14:00:38.537418','48','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(700,'2019-02-11 14:00:38.537774','49','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(701,'2019-02-11 14:00:38.538108','50','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(702,'2019-02-11 14:00:38.538438','51','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(703,'2019-02-11 14:00:38.538788','52','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(704,'2019-02-11 14:00:38.539122','53','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(705,'2019-02-11 14:00:38.539463','54','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(706,'2019-02-11 14:00:38.539876','55','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(707,'2019-02-11 14:00:38.540218','56','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(708,'2019-02-11 14:00:38.540565','57','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(709,'2019-02-11 14:00:38.540905','58','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(710,'2019-02-11 14:00:38.541241','59','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(711,'2019-02-11 14:00:38.541643','60','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(712,'2019-02-11 14:00:38.542008','61','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(713,'2019-02-11 14:00:38.542374','62','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(714,'2019-02-11 14:37:22.154267','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(715,'2019-02-11 14:37:22.154778','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(716,'2019-02-11 14:37:22.155148','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(717,'2019-02-11 14:37:22.155496','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(718,'2019-02-11 14:37:22.159410','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(719,'2019-02-11 14:37:22.159915','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(720,'2019-02-11 14:37:22.160312','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(721,'2019-02-11 14:37:22.160750','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(722,'2019-02-11 14:37:22.161111','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(723,'2019-02-11 14:37:22.161481','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(724,'2019-02-11 14:37:22.161843','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(725,'2019-02-11 14:37:22.162187','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(726,'2019-02-11 14:37:22.162524','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(727,'2019-02-11 14:37:22.162881','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(728,'2019-02-11 14:37:22.163262','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(729,'2019-02-11 14:37:22.163607','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(730,'2019-02-11 14:37:22.163997','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(731,'2019-02-11 14:37:22.164339','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(732,'2019-02-11 14:37:22.164676','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(733,'2019-02-11 14:37:22.165074','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(734,'2019-02-11 14:37:22.165443','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(735,'2019-02-11 14:37:22.165804','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(736,'2019-02-11 14:37:22.166145','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(737,'2019-02-11 14:37:22.166480','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(738,'2019-02-11 14:37:22.166834','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(739,'2019-02-11 14:37:22.167173','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(740,'2019-02-11 14:37:22.167509','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(741,'2019-02-11 14:37:22.167865','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(742,'2019-02-11 14:37:22.168203','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(743,'2019-02-11 14:37:22.168538','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(744,'2019-02-11 14:37:22.168918','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(745,'2019-02-11 14:38:52.165615','32','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(746,'2019-02-11 14:38:52.166077','33','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(747,'2019-02-11 14:38:52.166451','34','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(748,'2019-02-11 14:38:52.166825','35','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(749,'2019-02-11 14:38:52.167170','36','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(750,'2019-02-11 14:38:52.167533','37','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(751,'2019-02-11 14:38:52.167897','38','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(752,'2019-02-11 14:38:52.168240','39','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(753,'2019-02-11 14:38:52.168622','40','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(754,'2019-02-11 14:38:52.169002','41','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(755,'2019-02-11 14:38:52.169378','42','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(756,'2019-02-11 14:38:52.169750','43','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(757,'2019-02-11 14:38:52.170097','44','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(758,'2019-02-11 14:38:52.170452','45','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(759,'2019-02-11 14:38:52.170821','46','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(760,'2019-02-11 14:38:52.171166','47','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(761,'2019-02-11 14:38:52.171522','48','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(762,'2019-02-11 14:38:52.171889','49','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(763,'2019-02-11 14:38:52.172230','50','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(764,'2019-02-11 14:38:52.172597','51','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(765,'2019-02-11 14:38:52.172962','52','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(766,'2019-02-11 14:38:52.173323','53','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(767,'2019-02-11 14:38:52.173716','54','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(768,'2019-02-11 14:38:52.174080','55','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(769,'2019-02-11 14:38:52.174437','56','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(770,'2019-02-11 14:38:52.174801','57','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(771,'2019-02-11 14:38:52.175142','58','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(772,'2019-02-11 14:38:52.175504','59','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(773,'2019-02-11 14:38:52.175873','60','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(774,'2019-02-11 14:38:52.176250','61','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(775,'2019-02-11 14:38:52.176621','62','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(776,'2019-02-14 19:49:15.107653','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(777,'2019-02-14 19:49:15.108222','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(778,'2019-02-14 19:49:15.108629','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(779,'2019-02-14 19:49:15.109049','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(780,'2019-02-14 19:49:15.109532','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(781,'2019-02-14 19:49:15.109955','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(782,'2019-02-14 19:49:15.110326','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(783,'2019-02-14 19:49:15.110720','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(784,'2019-02-14 19:49:15.111102','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(785,'2019-02-14 19:49:15.111489','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(786,'2019-02-14 19:49:15.111878','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(787,'2019-02-14 19:49:15.112244','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(788,'2019-02-14 19:49:15.112604','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(789,'2019-02-14 19:49:15.112989','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(790,'2019-02-14 19:49:15.113374','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(791,'2019-02-14 19:49:15.113740','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(792,'2019-02-14 19:49:15.114207','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(793,'2019-02-14 19:49:15.114579','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(794,'2019-02-14 19:49:15.114960','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(795,'2019-02-14 19:49:15.115323','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(796,'2019-02-14 19:49:15.115681','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(797,'2019-02-14 19:49:15.116056','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(798,'2019-02-14 19:49:15.116413','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(799,'2019-02-14 19:49:15.116771','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(800,'2019-02-14 19:49:15.117148','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(801,'2019-02-14 19:49:15.117546','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(802,'2019-02-14 19:49:15.117928','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(803,'2019-02-14 19:49:15.118293','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(804,'2019-02-14 19:49:15.118651','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(805,'2019-02-14 19:49:15.119024','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(806,'2019-02-14 19:49:15.119383','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(807,'2019-02-14 19:58:45.728553','94','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(808,'2019-02-14 19:58:45.729092','95','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(809,'2019-02-14 19:58:45.729610','96','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(810,'2019-02-14 19:58:45.730007','97','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(811,'2019-02-14 19:58:45.730410','98','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(812,'2019-02-14 19:58:45.730770','99','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(813,'2019-02-14 19:58:45.731147','100','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(814,'2019-02-14 19:58:45.731547','101','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(815,'2019-02-14 19:58:45.731939','102','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(816,'2019-02-14 19:58:45.732299','103','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(817,'2019-02-14 19:58:45.732655','104','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(818,'2019-02-14 19:58:45.733039','105','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(819,'2019-02-14 19:58:45.733422','106','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(820,'2019-02-14 19:58:45.733782','107','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(821,'2019-02-14 19:58:45.734154','108','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(822,'2019-02-14 19:58:45.734511','109','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(823,'2019-02-14 19:58:45.734882','110','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(824,'2019-02-14 19:58:45.735241','111','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(825,'2019-02-14 19:58:45.735596','112','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(826,'2019-02-14 19:58:45.735971','113','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(827,'2019-02-14 19:58:45.736329','114','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(828,'2019-02-14 19:58:45.736684','115','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(829,'2019-02-14 19:58:45.737060','116','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(830,'2019-02-14 19:58:45.737450','117','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(831,'2019-02-14 19:58:45.737820','118','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(832,'2019-02-14 19:58:45.738180','119','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(833,'2019-02-14 19:58:45.738535','120','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(834,'2019-02-14 19:58:45.738901','121','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(835,'2019-02-14 19:58:45.739262','122','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(836,'2019-02-14 19:58:45.739619','123','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(837,'2019-02-14 19:58:45.739999','124','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(838,'2019-02-14 20:23:10.278928','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(839,'2019-02-14 20:23:10.279486','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(840,'2019-02-14 20:23:10.279873','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(841,'2019-02-14 20:23:10.280259','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(842,'2019-02-14 20:23:10.280606','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(843,'2019-02-14 20:23:10.280960','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(844,'2019-02-14 20:23:10.281317','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(845,'2019-02-14 20:23:10.281658','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(846,'2019-02-14 20:23:10.282009','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(847,'2019-02-14 20:23:10.282340','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(848,'2019-02-14 20:23:10.282669','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(849,'2019-02-14 20:23:10.283015','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(850,'2019-02-14 20:23:10.283343','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(851,'2019-02-14 20:23:10.283674','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(852,'2019-02-14 20:23:10.284025','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(853,'2019-02-14 20:23:10.284358','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(854,'2019-02-14 20:23:10.284688','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(855,'2019-02-14 20:23:10.285038','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(856,'2019-02-14 20:23:10.285393','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(857,'2019-02-14 20:23:10.285823','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(858,'2019-02-14 20:23:10.286167','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(859,'2019-02-14 20:23:10.286498','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(860,'2019-02-14 20:23:10.286841','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(861,'2019-02-14 20:23:10.291413','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(862,'2019-02-14 20:23:10.291817','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(863,'2019-02-14 20:23:10.292171','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(864,'2019-02-14 20:23:10.292606','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(865,'2019-02-14 20:23:10.293087','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(866,'2019-02-14 20:23:10.293515','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(867,'2019-02-14 20:23:10.293935','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(868,'2019-02-14 20:23:10.294370','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(869,'2019-02-14 20:51:56.249350','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(870,'2019-02-14 20:51:56.249944','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(871,'2019-02-14 20:51:56.250329','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(872,'2019-02-14 20:51:56.250685','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(873,'2019-02-14 20:51:56.251055','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(874,'2019-02-14 20:51:56.251420','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(875,'2019-02-14 20:51:56.251857','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(876,'2019-02-14 20:51:56.252229','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(877,'2019-02-14 20:51:56.252580','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(878,'2019-02-14 20:51:56.252965','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(879,'2019-02-14 20:51:56.253348','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(880,'2019-02-14 20:51:56.253737','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(881,'2019-02-14 20:51:56.254111','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(882,'2019-02-14 20:51:56.254455','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(883,'2019-02-14 20:51:56.254808','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(884,'2019-02-14 20:51:56.255176','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(885,'2019-02-14 20:51:56.255520','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(886,'2019-02-14 20:51:56.255878','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(887,'2019-02-14 20:51:56.256224','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(888,'2019-02-14 20:51:56.256567','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(889,'2019-02-14 20:51:56.256928','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(890,'2019-02-14 20:51:56.257289','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(891,'2019-02-14 20:51:56.257639','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(892,'2019-02-14 20:51:56.257999','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(893,'2019-02-14 20:51:56.258343','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(894,'2019-02-14 20:51:56.258682','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(895,'2019-02-14 20:51:56.259040','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(896,'2019-02-14 20:51:56.259382','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(897,'2019-02-14 20:51:56.259726','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(898,'2019-02-14 20:51:56.260086','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(899,'2019-02-14 20:51:56.260432','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(900,'2019-02-14 20:54:12.496139','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(901,'2019-02-14 20:54:12.496593','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(902,'2019-02-14 20:54:12.496977','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(903,'2019-02-14 20:54:12.497350','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(904,'2019-02-14 20:54:12.497701','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(905,'2019-02-14 20:54:12.498059','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(906,'2019-02-14 20:54:12.498398','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(907,'2019-02-14 20:54:12.498738','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(908,'2019-02-14 20:54:12.499090','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(909,'2019-02-14 20:54:12.499429','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(910,'2019-02-14 20:54:12.499827','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(911,'2019-02-14 20:54:12.500170','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(912,'2019-02-14 20:54:12.500510','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(913,'2019-02-14 20:54:12.500868','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(914,'2019-02-14 20:54:12.501210','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(915,'2019-02-14 20:54:12.501576','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(916,'2019-02-14 20:54:12.501934','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(917,'2019-02-14 20:54:12.502277','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(918,'2019-02-14 20:54:12.502616','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(919,'2019-02-14 20:54:12.503018','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(920,'2019-02-14 20:54:12.503363','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(921,'2019-02-14 20:54:12.503703','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(922,'2019-02-14 20:54:12.504061','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(923,'2019-02-14 20:54:12.504402','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(924,'2019-02-14 20:54:12.504785','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(925,'2019-02-14 20:54:12.505132','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(926,'2019-02-14 20:54:12.505495','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(927,'2019-02-14 20:54:12.505848','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(928,'2019-02-14 20:54:12.506188','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(929,'2019-02-14 20:54:12.506524','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(930,'2019-02-14 20:54:12.506924','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(931,'2019-02-14 20:55:10.664264','156','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(932,'2019-02-14 20:55:10.664723','157','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(933,'2019-02-14 20:55:10.665146','158','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(934,'2019-02-14 20:55:10.665599','159','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(935,'2019-02-14 20:55:10.665973','160','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(936,'2019-02-14 20:55:10.666323','161','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(937,'2019-02-14 20:55:10.666669','162','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(938,'2019-02-14 20:55:10.667030','163','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(939,'2019-02-14 20:55:10.667373','164','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(940,'2019-02-14 20:55:10.667715','165','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(941,'2019-02-14 20:55:10.668077','166','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(942,'2019-02-14 20:55:10.668423','167','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(943,'2019-02-14 20:55:10.668781','168','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(944,'2019-02-14 20:55:10.669162','169','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(945,'2019-02-14 20:55:10.669538','170','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(946,'2019-02-14 20:55:10.669907','171','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(947,'2019-02-14 20:55:10.670256','172','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(948,'2019-02-14 20:55:10.670637','173','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(949,'2019-02-14 20:55:10.671003','174','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(950,'2019-02-14 20:55:10.671347','175','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(951,'2019-02-14 20:55:10.671691','176','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(952,'2019-02-14 20:55:10.672058','177','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(953,'2019-02-14 20:55:10.672403','178','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(954,'2019-02-14 20:55:10.672745','179','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(955,'2019-02-14 20:55:10.673138','180','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(956,'2019-02-14 20:55:10.673542','181','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(957,'2019-02-14 20:55:10.673952','182','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(958,'2019-02-14 20:55:10.674306','183','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(959,'2019-02-14 20:55:10.674652','184','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(960,'2019-02-14 20:55:10.675017','185','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(961,'2019-02-14 20:55:10.675361','186','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(962,'2019-02-14 21:24:02.911636','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(963,'2019-02-14 21:24:02.912251','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(964,'2019-02-14 21:24:02.912673','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(965,'2019-02-14 21:24:02.913069','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(966,'2019-02-14 21:24:02.913459','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(967,'2019-02-14 21:24:02.913836','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(968,'2019-02-14 21:24:02.914200','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(969,'2019-02-14 21:24:02.914559','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(970,'2019-02-14 21:24:02.914965','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(971,'2019-02-14 21:24:02.915325','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(972,'2019-02-14 21:24:02.915681','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(973,'2019-02-14 21:24:02.916054','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(974,'2019-02-14 21:24:02.916412','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(975,'2019-02-14 21:24:02.916779','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(976,'2019-02-14 21:24:02.917141','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(977,'2019-02-14 21:24:02.917553','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(978,'2019-02-14 21:24:02.917930','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(979,'2019-02-14 21:24:02.918290','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(980,'2019-02-14 21:24:02.918653','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(981,'2019-02-14 21:24:02.919029','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(982,'2019-02-14 21:24:02.919389','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(983,'2019-02-14 21:24:02.919775','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(984,'2019-02-14 21:24:02.920147','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(985,'2019-02-14 21:24:02.920506','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(986,'2019-02-14 21:24:02.920877','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(987,'2019-02-14 21:24:02.921235','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(988,'2019-02-14 21:24:02.921638','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(989,'2019-02-14 21:24:02.922017','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(990,'2019-02-14 21:24:02.922394','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(991,'2019-02-14 21:24:02.922783','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(992,'2019-02-14 21:24:02.923185','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(993,'2019-02-14 21:24:55.216555','218','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(994,'2019-02-14 21:24:55.217049','219','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(995,'2019-02-14 21:24:55.217468','220','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(996,'2019-02-14 21:24:55.217872','221','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(997,'2019-02-14 21:24:55.218255','222','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(998,'2019-02-14 21:24:55.218628','223','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(999,'2019-02-14 21:24:55.219018','224','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(1000,'2019-02-14 21:24:55.219390','225','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(1001,'2019-02-14 21:24:55.219858','226','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(1002,'2019-02-14 21:24:55.220241','227','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(1003,'2019-02-14 21:24:55.220613','228','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(1004,'2019-02-14 21:24:55.220998','229','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(1005,'2019-02-14 21:24:55.221391','230','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(1006,'2019-02-14 21:24:55.224573','231','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(1007,'2019-02-14 21:24:55.227443','232','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(1008,'2019-02-14 21:24:55.227899','233','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(1009,'2019-02-14 21:24:55.228328','234','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(1010,'2019-02-14 21:24:55.228735','235','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(1011,'2019-02-14 21:24:55.229136','236','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(1012,'2019-02-14 21:24:55.229546','237','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(1013,'2019-02-14 21:24:55.229963','238','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(1014,'2019-02-14 21:24:55.230336','239','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(1015,'2019-02-14 21:24:55.230780','240','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(1016,'2019-02-14 21:24:55.231162','241','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(1017,'2019-02-14 21:24:55.231606','242','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(1018,'2019-02-14 21:24:55.232004','243','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(1019,'2019-02-14 21:24:55.232375','244','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(1020,'2019-02-14 21:24:55.232744','245','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(1021,'2019-02-14 21:24:55.233151','246','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(1022,'2019-02-14 21:24:55.233592','247','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(1023,'2019-02-14 21:24:55.233984','248','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113'),(1024,'2019-02-15 12:21:40.874423','15336095','15336095 梁沛霖',1,'new through import_export',4,'16337113'),(1025,'2019-02-15 12:21:40.874965','15336101','15336101 林建涛',1,'new through import_export',4,'16337113'),(1026,'2019-02-15 12:21:40.875389','15336102','15336102 林民钊',1,'new through import_export',4,'16337113'),(1027,'2019-02-15 12:21:40.875790','15336117','15336117 刘展宏',1,'new through import_export',4,'16337113'),(1028,'2019-02-15 12:21:40.876166','15336121','15336121 陆剑',1,'new through import_export',4,'16337113'),(1029,'2019-02-15 12:21:40.876588','15336141','15336141 彭博东',1,'new through import_export',4,'16337113'),(1030,'2019-02-15 12:21:40.877008','15336142','15336142 彭诗煜',1,'new through import_export',4,'16337113'),(1031,'2019-02-15 12:21:40.877421','16337071','16337071 郭如意',1,'new through import_export',4,'16337113'),(1032,'2019-02-15 12:21:40.877845','16337094','16337094 黄凯欢',1,'new through import_export',4,'16337113'),(1033,'2019-02-15 12:21:40.878224','16337098','16337098 黄义凯',1,'new through import_export',4,'16337113'),(1034,'2019-02-15 12:21:40.878613','16337099','16337099 黄亦安',1,'new through import_export',4,'16337113'),(1035,'2019-02-15 12:21:40.879100','16337106','16337106 解锐',1,'new through import_export',4,'16337113'),(1036,'2019-02-15 12:21:40.879478','16337108','16337108 金牧',1,'new through import_export',4,'16337113'),(1037,'2019-02-15 12:21:40.879904','16337109','16337109 柯司博',1,'new through import_export',4,'16337113'),(1038,'2019-02-15 12:21:40.880288','16337112','16337112 兰楠',1,'new through import_export',4,'16337113'),(1039,'2019-02-15 12:21:40.880738','16337113','16337113 劳马东',1,'new through import_export',4,'16337113'),(1040,'2019-02-15 12:21:40.881171','16337129','16337129 李智源',1,'new through import_export',4,'16337113'),(1041,'2019-02-15 12:21:40.881650','16337154','16337154 刘海',1,'new through import_export',4,'16337113'),(1042,'2019-02-15 12:21:40.882074','17341061','17341061 黄勇',1,'new through import_export',4,'16337113'),(1043,'2019-02-15 12:21:40.882469','17341073','17341073 蓝靖瑜',1,'new through import_export',4,'16337113'),(1044,'2019-02-15 12:21:40.882871','17341074','17341074 蓝煜航',1,'new through import_export',4,'16337113'),(1045,'2019-02-15 12:21:40.883297','17341095','17341095 廖德洋',1,'new through import_export',4,'16337113'),(1046,'2019-02-15 12:21:40.883670','17341096','17341096 廖浩淳',1,'new through import_export',4,'16337113'),(1047,'2019-02-15 12:21:40.884104','17341097','17341097 廖永滨',1,'new through import_export',4,'16337113'),(1048,'2019-02-15 12:21:40.884484','17341099','17341099 廖泽祥',1,'new through import_export',4,'16337113'),(1049,'2019-02-15 12:21:40.884892','17341105','17341105 刘晨飞',1,'new through import_export',4,'16337113'),(1050,'2019-02-15 12:21:40.885311','17341114','17341114 刘雨萱',1,'new through import_export',4,'16337113'),(1051,'2019-02-15 12:21:40.885692','17341117','17341117 卢曼宁',1,'new through import_export',4,'16337113'),(1052,'2019-02-15 12:21:40.886119','18340069','18340069 黄轩腾',1,'new through import_export',4,'16337113'),(1053,'2019-02-15 12:21:40.886524','18340075','18340075 黄卓燊',1,'new through import_export',4,'16337113'),(1054,'2019-02-15 12:21:40.887031','18340076','18340076 黄子聿',1,'new through import_export',4,'16337113'),(1055,'2019-02-15 12:41:12.314264','32','组织生活会(1): 16337109 柯司博',1,'new through import_export',7,'16337113'),(1056,'2019-02-15 12:41:12.314828','33','组织生活会(1): 16337113 劳马东',1,'new through import_export',7,'16337113'),(1057,'2019-02-15 12:41:12.315237','34','组织生活会(1): 17341061 黄勇',1,'new through import_export',7,'16337113'),(1058,'2019-02-15 12:41:12.315679','35','组织生活会(1): 15336117 刘展宏',1,'new through import_export',7,'16337113'),(1059,'2019-02-15 12:41:12.316054','36','组织生活会(1): 15336141 彭博东',1,'new through import_export',7,'16337113'),(1060,'2019-02-15 12:41:12.316441','37','组织生活会(1): 15336095 梁沛霖',1,'new through import_export',7,'16337113'),(1061,'2019-02-15 12:41:12.316798','38','组织生活会(1): 15336101 林建涛',1,'new through import_export',7,'16337113'),(1062,'2019-02-15 12:41:12.317143','39','组织生活会(1): 15336102 林民钊',1,'new through import_export',7,'16337113'),(1063,'2019-02-15 12:41:12.317519','40','组织生活会(1): 15336121 陆剑',1,'new through import_export',7,'16337113'),(1064,'2019-02-15 12:41:12.317882','41','组织生活会(1): 16337071 郭如意',1,'new through import_export',7,'16337113'),(1065,'2019-02-15 12:41:12.318225','42','组织生活会(1): 16337098 黄义凯',1,'new through import_export',7,'16337113'),(1066,'2019-02-15 12:41:12.318606','43','组织生活会(1): 16337108 金牧',1,'new through import_export',7,'16337113'),(1067,'2019-02-15 12:41:12.318979','44','组织生活会(1): 15336142 彭诗煜',1,'new through import_export',7,'16337113'),(1068,'2019-02-15 12:41:12.319324','45','组织生活会(1): 16337094 黄凯欢',1,'new through import_export',7,'16337113'),(1069,'2019-02-15 12:41:12.319669','46','组织生活会(1): 16337099 黄亦安',1,'new through import_export',7,'16337113'),(1070,'2019-02-15 12:41:12.320029','47','组织生活会(1): 16337106 解锐',1,'new through import_export',7,'16337113'),(1071,'2019-02-15 12:41:12.320370','48','组织生活会(1): 16337112 兰楠',1,'new through import_export',7,'16337113'),(1072,'2019-02-15 12:41:12.320708','49','组织生活会(1): 16337129 李智源',1,'new through import_export',7,'16337113'),(1073,'2019-02-15 12:41:12.321066','50','组织生活会(1): 16337154 刘海',1,'new through import_export',7,'16337113'),(1074,'2019-02-15 12:41:12.321446','51','组织生活会(1): 17341073 蓝靖瑜',1,'new through import_export',7,'16337113'),(1075,'2019-02-15 12:41:12.321869','52','组织生活会(1): 17341074 蓝煜航',1,'new through import_export',7,'16337113'),(1076,'2019-02-15 12:41:12.322220','53','组织生活会(1): 17341095 廖德洋',1,'new through import_export',7,'16337113'),(1077,'2019-02-15 12:41:12.322563','54','组织生活会(1): 17341096 廖浩淳',1,'new through import_export',7,'16337113'),(1078,'2019-02-15 12:41:12.322921','55','组织生活会(1): 17341097 廖永滨',1,'new through import_export',7,'16337113'),(1079,'2019-02-15 12:41:12.323264','56','组织生活会(1): 17341099 廖泽祥',1,'new through import_export',7,'16337113'),(1080,'2019-02-15 12:41:12.323603','57','组织生活会(1): 17341105 刘晨飞',1,'new through import_export',7,'16337113'),(1081,'2019-02-15 12:41:12.323962','58','组织生活会(1): 17341114 刘雨萱',1,'new through import_export',7,'16337113'),(1082,'2019-02-15 12:41:12.324303','59','组织生活会(1): 17341117 卢曼宁',1,'new through import_export',7,'16337113'),(1083,'2019-02-15 12:41:12.324640','60','组织生活会(1): 18340069 黄轩腾',1,'new through import_export',7,'16337113'),(1084,'2019-02-15 12:41:12.324999','61','组织生活会(1): 18340075 黄卓燊',1,'new through import_export',7,'16337113'),(1085,'2019-02-15 12:41:12.325421','62','组织生活会(1): 18340076 黄子聿',1,'new through import_export',7,'16337113');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'admin','logentry'),(10,'auth','group'),(9,'auth','permission'),(11,'contenttypes','contenttype'),(2,'info','application'),(3,'info','branch'),(17,'info','dependency'),(4,'info','member'),(5,'info','school'),(12,'sessions','session'),(6,'teaching','activity'),(7,'teaching','takepartin'),(1,'user','user'),(13,'xadmin','bookmark'),(16,'xadmin','log'),(14,'xadmin','usersettings'),(15,'xadmin','userwidget');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-02-09 22:46:43.441976'),(2,'contenttypes','0002_remove_content_type_name','2019-02-09 22:46:43.514207'),(3,'auth','0001_initial','2019-02-09 22:46:43.794041'),(4,'auth','0002_alter_permission_name_max_length','2019-02-09 22:46:43.843172'),(5,'auth','0003_alter_user_email_max_length','2019-02-09 22:46:43.852793'),(6,'auth','0004_alter_user_username_opts','2019-02-09 22:46:43.861660'),(7,'auth','0005_alter_user_last_login_null','2019-02-09 22:46:43.870147'),(8,'auth','0006_require_contenttypes_0002','2019-02-09 22:46:43.874501'),(9,'auth','0007_alter_validators_add_error_messages','2019-02-09 22:46:43.884344'),(10,'auth','0008_alter_user_username_max_length','2019-02-09 22:46:43.894711'),(11,'auth','0009_alter_user_last_name_max_length','2019-02-09 22:46:43.903103'),(12,'user','0001_initial','2019-02-09 22:46:44.242150'),(13,'admin','0001_initial','2019-02-09 22:46:44.338569'),(14,'admin','0002_logentry_remove_auto_add','2019-02-09 22:46:44.350396'),(15,'admin','0003_logentry_add_action_flag_choices','2019-02-09 22:46:44.361128'),(18,'sessions','0001_initial','2019-02-09 22:46:44.668668'),(20,'xadmin','0001_initial','2019-02-09 22:46:45.233019'),(21,'xadmin','0002_log','2019-02-09 22:46:45.337927'),(22,'xadmin','0003_auto_20160715_0100','2019-02-09 22:46:45.385381'),(28,'user','0002_auto_20190210_2106','2019-02-10 21:06:23.210372'),(37,'user','0003_auto_20190210_2109','2019-02-10 21:09:37.832401'),(41,'user','0004_auto_20190210_2242','2019-02-10 22:43:02.179975'),(53,'address','0001_initial','2019-02-11 15:03:28.267125'),(54,'address','0002_auto_20160213_1726','2019-02-11 15:03:28.301395'),(69,'info','0001_initial','2019-02-15 11:48:44.594464'),(70,'teaching','0001_initial','2019-02-15 11:48:44.878771'),(71,'info','0002_auto_20190215_1153','2019-02-15 11:53:19.875715'),(72,'info','0003_auto_20190215_1154','2019-02-15 11:54:50.900104'),(73,'info','0004_auto_20190215_1201','2019-02-15 12:01:54.002421'),(74,'info','0005_auto_20190215_1216','2019-02-15 12:16:19.262875'),(75,'info','0006_auto_20190215_1217','2019-02-15 12:17:47.376164'),(76,'info','0007_auto_20190215_1225','2019-02-15 12:25:16.268793');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('exb60i8k8fsj5tdl4t77uzofetj136tm','OGE4ZTYwOTAwNDIxOGI4ZWNjNTU1ZTI2YzUyNzJkZWQxNWYyMjUwMTp7Il9hdXRoX3VzZXJfaWQiOiIxNjMzNzExMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjBkZWQ3ZjE5OWQ1ODJkNzBmMDZjMTNlNjBiNTA5OTkyOWMxYzU3NCIsIm5hdl9tZW51IjoiW3tcInRpdGxlXCI6IFwiXHU1MTVhXHU1NDU4XHU1M2QxXHU1YzU1XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU1YjY2XHU5NjYyXCIsIFwidXJsXCI6IFwiL2luZm8vc2Nob29sL1wiLCBcImljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwib3JkZXJcIjogNn0sIHtcInRpdGxlXCI6IFwiXHU1MTVhXHU2NTJmXHU5MGU4XCIsIFwidXJsXCI6IFwiL2luZm8vYnJhbmNoL1wiLCBcImljb25cIjogXCJmYSBmYS11c2VyXCIsIFwib3JkZXJcIjogN30sIHtcInRpdGxlXCI6IFwiXHU1M2QxXHU1YzU1XHU2ZDQxXHU3YTBiXHU0ZjlkXHU4ZDU2XCIsIFwidXJsXCI6IFwiL2luZm8vZGVwZW5kZW5jeS9cIiwgXCJpY29uXCI6IG51bGwsIFwib3JkZXJcIjogOH0sIHtcInRpdGxlXCI6IFwiXHU2MjEwXHU1NDU4XHU0ZmUxXHU2MDZmXCIsIFwidXJsXCI6IFwiL2luZm8vbWVtYmVyL1wiLCBcImljb25cIjogXCJmYSBmYS1pbmZvXCIsIFwib3JkZXJcIjogOX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwiZmlyc3RfdXJsXCI6IFwiL2luZm8vc2Nob29sL1wifSwge1widGl0bGVcIjogXCJcdTUxNWFcdTU0NThcdTY1NTlcdTgwYjJcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTRmMWFcdThiYWUvXHU2ZDNiXHU1MmE4XCIsIFwidXJsXCI6IFwiL3RlYWNoaW5nL2FjdGl2aXR5L1wiLCBcImljb25cIjogXCJmYSBmYS11c2Vyc1wiLCBcIm9yZGVyXCI6IDEwfSwge1widGl0bGVcIjogXCJcdTViNjZcdTY1ZjZcdTdlZGZcdThiYTFcIiwgXCJ1cmxcIjogXCIvdGVhY2hpbmcvdGFrZXBhcnRpbi9cIiwgXCJpY29uXCI6IFwiZmEgZmEtYmFyLWNoYXJ0XCIsIFwib3JkZXJcIjogMTF9XSwgXCJmaXJzdF9pY29uXCI6IFwiZmEgZmEtdXNlcnNcIiwgXCJmaXJzdF91cmxcIjogXCIvdGVhY2hpbmcvYWN0aXZpdHkvXCJ9LCB7XCJ0aXRsZVwiOiBcIlx1NzUyOFx1NjIzN1wiLCBcIm1lbnVzXCI6IFt7XCJ0aXRsZVwiOiBcIlx1NjIxMVx1NzY4NFx1OGQyNlx1NTNmN1wiLCBcInVybFwiOiBcIi91c2VyL3VzZXIvXCIsIFwiaWNvblwiOiBcImZhIGZhLXZjYXJkXCIsIFwib3JkZXJcIjogNX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS12Y2FyZFwiLCBcImZpcnN0X3VybFwiOiBcIi91c2VyL3VzZXIvXCJ9XSIsIndpemFyZF9pbmZvbWVtYmVyX2FkbWluX3dpemFyZF9mb3JtX3BsdWdpbiI6eyJzdGVwIjoiXHU1N2ZhXHU2NzJjXHU0ZmUxXHU2MDZmIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9fSwiTElTVF9RVUVSWSI6W1siaW5mbyIsImRlcGVuZGVuY3kiXSwiIl19','2019-03-01 12:42:21.841512'),('hsoz4rfnccyhmuxh7tl86kngife5j0wm','NTNiOWIwY2VhZjczOGFkMTEzN2RlYjRhZjBhNWMwYzVlMzkxNzIyMTp7Il9hdXRoX3VzZXJfaWQiOiIxNjMzNzA3MSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzdjZjc5NThhY2UzOWQ3MWY5NDg0YzUxMWQ2MDIxYTZhMzQwMjNlZiIsIm5hdl9tZW51IjoiW3tcInRpdGxlXCI6IFwiXHU1MTVhXHU1NDU4XHU1M2QxXHU1YzU1XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU1YjY2XHU5NjYyXCIsIFwidXJsXCI6IFwiL2luZm8vc2Nob29sL1wiLCBcImljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwib3JkZXJcIjogNn0sIHtcInRpdGxlXCI6IFwiXHU1MTVhXHU2NTJmXHU5MGU4XCIsIFwidXJsXCI6IFwiL2luZm8vYnJhbmNoL1wiLCBcImljb25cIjogXCJmYSBmYS11c2VyXCIsIFwib3JkZXJcIjogN30sIHtcInRpdGxlXCI6IFwiXHU2MjEwXHU1NDU4XHU0ZmUxXHU2MDZmXCIsIFwidXJsXCI6IFwiL2luZm8vbWVtYmVyL1wiLCBcImljb25cIjogXCJmYSBmYS1pbmZvXCIsIFwib3JkZXJcIjogOH1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwiZmlyc3RfdXJsXCI6IFwiL2luZm8vc2Nob29sL1wifSwge1widGl0bGVcIjogXCJcdTUxNWFcdTU0NThcdTY1NTlcdTgwYjJcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTRmMWFcdThiYWUvXHU2ZDNiXHU1MmE4XCIsIFwidXJsXCI6IFwiL3RlYWNoaW5nL2FjdGl2aXR5L1wiLCBcImljb25cIjogXCJmYSBmYS11c2Vyc1wiLCBcIm9yZGVyXCI6IDl9LCB7XCJ0aXRsZVwiOiBcIlx1NWI2Nlx1NjVmNlx1N2VkZlx1OGJhMVwiLCBcInVybFwiOiBcIi90ZWFjaGluZy90YWtlcGFydGluL1wiLCBcImljb25cIjogXCJmYSBmYS1iYXItY2hhcnRcIiwgXCJvcmRlclwiOiAxMH1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11c2Vyc1wiLCBcImZpcnN0X3VybFwiOiBcIi90ZWFjaGluZy9hY3Rpdml0eS9cIn0sIHtcInRpdGxlXCI6IFwiXHU3NTI4XHU2MjM3XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU2MjExXHU3Njg0XHU4ZDI2XHU1M2Y3XCIsIFwidXJsXCI6IFwiL3VzZXIvdXNlci9cIiwgXCJpY29uXCI6IFwiZmEgZmEtdmNhcmRcIiwgXCJvcmRlclwiOiA1fV0sIFwiZmlyc3RfaWNvblwiOiBcImZhIGZhLXZjYXJkXCIsIFwiZmlyc3RfdXJsXCI6IFwiL3VzZXIvdXNlci9cIn1dIiwiTElTVF9RVUVSWSI6W1siaW5mbyIsIm1lbWJlciJdLCIiXSwid2l6YXJkX2luZm9tZW1iZXJfYWRtaW5fd2l6YXJkX2Zvcm1fcGx1Z2luIjp7InN0ZXAiOiJcdTU3ZmFcdTY3MmNcdTRmZTFcdTYwNmYiLCJzdGVwX2RhdGEiOnt9LCJzdGVwX2ZpbGVzIjp7fSwiZXh0cmFfZGF0YSI6e319fQ==','2019-02-28 16:25:20.424218'),('ic8gd6dluur373itl6xoizq1vj34zf5f','ODM1MTNjOTZjYzkzODE3M2YzNDAyMGE0NmVjYjZmOWNmNzhhYmE4Nzp7Il9hdXRoX3VzZXJfaWQiOiIxNjMzNzExMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjBkZWQ3ZjE5OWQ1ODJkNzBmMDZjMTNlNjBiNTA5OTkyOWMxYzU3NCIsIm5hdl9tZW51IjoiW3tcInRpdGxlXCI6IFwiXHU1MTVhXHU1NDU4XHU1M2QxXHU1YzU1XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU1YjY2XHU5NjYyXCIsIFwidXJsXCI6IFwiL2luZm8vc2Nob29sL1wiLCBcImljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwib3JkZXJcIjogNn0sIHtcInRpdGxlXCI6IFwiXHU1MTVhXHU2NTJmXHU5MGU4XCIsIFwidXJsXCI6IFwiL2luZm8vYnJhbmNoL1wiLCBcImljb25cIjogXCJmYSBmYS11c2VyXCIsIFwib3JkZXJcIjogN30sIHtcInRpdGxlXCI6IFwiXHU2MjEwXHU1NDU4XHU0ZmUxXHU2MDZmXCIsIFwidXJsXCI6IFwiL2luZm8vbWVtYmVyL1wiLCBcImljb25cIjogXCJmYSBmYS1pbmZvXCIsIFwib3JkZXJcIjogOH1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwiZmlyc3RfdXJsXCI6IFwiL2luZm8vc2Nob29sL1wifSwge1widGl0bGVcIjogXCJcdTUxNWFcdTU0NThcdTY1NTlcdTgwYjJcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTUxNWFcdTVlZmFcdTZkM2JcdTUyYThcIiwgXCJ1cmxcIjogXCIvdGVhY2hpbmcvYWN0aXZpdHkvXCIsIFwiaWNvblwiOiBcImZhIGZhLXVzZXJzXCIsIFwib3JkZXJcIjogOX0sIHtcInRpdGxlXCI6IFwiXHU1YjY2XHU2NWY2XHU3ZWRmXHU4YmExXCIsIFwidXJsXCI6IFwiL3RlYWNoaW5nL3Rha2VwYXJ0aW4vXCIsIFwiaWNvblwiOiBcImZhIGZhLWJhci1jaGFydFwiLCBcIm9yZGVyXCI6IDEwfV0sIFwiZmlyc3RfaWNvblwiOiBcImZhIGZhLXVzZXJzXCIsIFwiZmlyc3RfdXJsXCI6IFwiL3RlYWNoaW5nL2FjdGl2aXR5L1wifSwge1widGl0bGVcIjogXCJcdTc1MjhcdTYyMzdcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTYyMTFcdTc2ODRcdThkMjZcdTUzZjdcIiwgXCJ1cmxcIjogXCIvdXNlci91c2VyL1wiLCBcImljb25cIjogXCJmYSBmYS12Y2FyZFwiLCBcIm9yZGVyXCI6IDV9XSwgXCJmaXJzdF9pY29uXCI6IFwiZmEgZmEtdmNhcmRcIiwgXCJmaXJzdF91cmxcIjogXCIvdXNlci91c2VyL1wifV0iLCJMSVNUX1FVRVJZIjpbWyJpbmZvIiwic2Nob29sIl0sIiJdfQ==','2019-02-24 17:52:39.967242');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_application`
--

DROP TABLE IF EXISTS `info_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `netid` varchar(8) NOT NULL,
  `application_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_application`
--

LOCK TABLES `info_application` WRITE;
/*!40000 ALTER TABLE `info_application` DISABLE KEYS */;
/*!40000 ALTER TABLE `info_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_branch`
--

DROP TABLE IF EXISTS `info_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_branch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(50) NOT NULL,
  `date_create` date DEFAULT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `info_branch_school_id_a22b8f0c_fk_info_school_id` (`school_id`),
  CONSTRAINT `info_branch_school_id_a22b8f0c_fk_info_school_id` FOREIGN KEY (`school_id`) REFERENCES `info_school` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_branch`
--

LOCK TABLES `info_branch` WRITE;
/*!40000 ALTER TABLE `info_branch` DISABLE KEYS */;
INSERT INTO `info_branch` VALUES (1,'计算机本科生第二党支部',NULL,1),(2,'保密党支部',NULL,1),(3,'计算机本科生第三党支部',NULL,1);
/*!40000 ALTER TABLE `info_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_dependency`
--

DROP TABLE IF EXISTS `info_dependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_dependency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_1` varchar(50) NOT NULL,
  `to` varchar(50) NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `info_dependency_from_1_to_07a0d4eb_uniq` (`from_1`,`to`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_dependency`
--

LOCK TABLES `info_dependency` WRITE;
/*!40000 ALTER TABLE `info_dependency` DISABLE KEYS */;
INSERT INTO `info_dependency` VALUES (2,'birth_date','application_date',6570),(3,'application_date','activist_date',180),(4,'activist_date','key_develop_person_date',365),(5,'league_promotion_date','democratic_appraisal_date',1),(6,'democratic_appraisal_date','key_develop_person_date',1),(7,'key_develop_person_date','first_branch_conference',90),(8,'first_branch_conference','second_branch_conference',365),(9,'application_fullmember_date','second_branch_conference',60);
/*!40000 ALTER TABLE `info_dependency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_member`
--

DROP TABLE IF EXISTS `info_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_member` (
  `netid` varchar(8) NOT NULL,
  `name` varchar(20) NOT NULL,
  `birth_date` date NOT NULL,
  `gender` varchar(1) NOT NULL,
  `group` varchar(20) NOT NULL,
  `family_address` varchar(50) DEFAULT NULL,
  `phone_number` varchar(128) DEFAULT NULL,
  `credit_card_id` varchar(25) DEFAULT NULL,
  `major_in` varchar(30) NOT NULL,
  `youth_league_date` date DEFAULT NULL,
  `constitution_group_date` date DEFAULT NULL,
  `application_date` date DEFAULT NULL,
  `activist_date` date DEFAULT NULL,
  `league_promotion_date` date DEFAULT NULL,
  `democratic_appraisal_date` date DEFAULT NULL,
  `political_check_date` date DEFAULT NULL,
  `key_develop_person_date` date DEFAULT NULL,
  `graduated_party_school_date` date DEFAULT NULL,
  `recommenders_date` date DEFAULT NULL,
  `recommenders` varchar(50) DEFAULT NULL,
  `autobiography_date` date DEFAULT NULL,
  `application_form_date` date DEFAULT NULL,
  `first_branch_conference` date DEFAULT NULL,
  `pro_conversation_date` date DEFAULT NULL,
  `talker` varchar(50) DEFAULT NULL,
  `probationary_approval_date` date DEFAULT NULL,
  `oach_date` date DEFAULT NULL,
  `application_fullmember_date` date DEFAULT NULL,
  `second_branch_conference` date DEFAULT NULL,
  `fullmember_approval_date` date DEFAULT NULL,
  `branch_id` int(11) NOT NULL,
  PRIMARY KEY (`netid`),
  KEY `info_member_branch_id_90c6294a_fk_info_branch_id` (`branch_id`),
  KEY `info_member_name_0c14d67c` (`name`),
  CONSTRAINT `info_member_branch_id_90c6294a_fk_info_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `info_branch` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_member`
--

LOCK TABLES `info_member` WRITE;
/*!40000 ALTER TABLE `info_member` DISABLE KEYS */;
INSERT INTO `info_member` VALUES ('15336095','梁沛霖','1997-05-27','男','汉',NULL,NULL,'','计算机',NULL,'2016-10-20','2016-10-23','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-23','劳马东 柯司博',NULL,NULL,'2018-12-22',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('15336101','林建涛','1996-09-06','男','汉','',NULL,'','计算机类',NULL,NULL,'2016-10-21','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336102','林民钊','1997-06-25','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-11-29','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336117','刘展宏','1997-08-28','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-10-10','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-05-12','2018-06-04','劳马东 柯司博',NULL,NULL,'2018-06-04','2018-06-12','胡凤娟','2018-06-27','2019-06-12',NULL,NULL,NULL,1),('15336121','陆剑','1997-04-18','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-11-30','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336141','彭博东','1996-12-24','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-09-28','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-05-12','2018-06-04','劳马东 柯司博',NULL,NULL,'2018-06-04','2018-06-12','胡凤娟','2018-06-27','2019-06-12',NULL,NULL,NULL,1),('15336142','彭诗煜','1996-04-10','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-10-10','2017-09-16',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337071','郭如意','1998-01-09','女','汉','',NULL,'','计算机',NULL,'2016-10-13','2016-10-14','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337094','黄凯欢','1997-12-19','男','汉','',NULL,'','计算机类',NULL,'2016-10-10','2017-03-02','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337098','黄义凯','1997-10-25','男','汉','',NULL,'','计算机类',NULL,'2016-10-20','2016-10-25','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337099','黄亦安','1997-08-05','男','汉','',NULL,'','计算机类',NULL,'2016-10-10','2017-02-28','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337106','解锐','1998-12-13','男','汉','',NULL,'','计算机类',NULL,'2016-10-10','2017-04-07','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337108','金牧','1998-08-18','女','汉','',NULL,'','计算机科学与技术',NULL,'2016-10-25','2016-10-31','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337109','柯司博','1996-12-24','男','汉','',NULL,'','计算机类',NULL,'2016-09-01','2015-03-01','2015-03-10','2015-03-08','2016-03-14','2016-03-15','2016-03-15','2016-03-16','2016-03-20','徐亦春 范瑞莲',NULL,NULL,'2016-03-21','2016-03-29','莫宇贵','2016-03-31','1949-10-01','2017-03-14','2017-04-23','2017-05-24',1),('16337112','兰楠','1999-10-14','女','汉','',NULL,'','计算机类',NULL,'2017-10-15','2017-10-24','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337113','劳马东','1997-02-14','男','汉','',NULL,'','计算机类',NULL,'2016-09-01','2015-02-19','2015-03-08','2015-04-01','2015-04-01','2016-03-01','2016-03-01','2016-03-10','2016-03-10','陈成文 郑康明',NULL,NULL,'2016-04-05','2016-04-10','骆国丰','2016-04-20','2016-06-24','2017-03-25','2017-04-23','2017-05-24',1),('16337129','李智源','1997-07-15','男','汉','',NULL,'','计算机科学与技术',NULL,'2016-10-11','2018-03-03','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337154','刘海','1997-09-20','男','汉','',NULL,'','计算机类',NULL,'2016-10-19','2017-10-10','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341061','黄勇','1997-11-01','男','汉','',NULL,'','计算机类',NULL,'2017-10-20','2016-01-18','2016-02-28','2017-03-08','2017-03-08','2017-03-14','2017-03-14','2017-05-18','2017-05-18','汪绍银 席永红',NULL,NULL,'2017-05-19','2017-05-25','席永红','2017-06-20','2017-06-30','2018-05-03','2018-07-18','2020-06-27',1),('17341073','蓝靖瑜','1999-01-22','男','汉','',NULL,'','计算机类',NULL,'2017-09-01','2017-12-22','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341074','蓝煜航','1999-09-06','男','汉','',NULL,'','计算机类',NULL,'2017-11-20','2018-03-16','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341095','廖德洋','1997-10-27','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341096','廖浩淳','1999-08-27','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341097','廖永滨','1999-02-05','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341099','廖泽祥','1998-08-26','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341105','刘晨飞','1999-12-01','男','汉','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341114','刘雨萱','1999-07-22','女','汉族','',NULL,'','计算机类',NULL,NULL,'2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341117','卢曼宁','1999-06-29','女','汉','',NULL,'','计算机类',NULL,NULL,'2018-03-27',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('18340069','黄轩腾','2000-08-15','男','汉','',NULL,'','计算机类',NULL,'2018-10-19','2018-10-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('18340075','黄卓燊','1999-10-03','男','汉','',NULL,'','计算机类',NULL,'2018-10-19','2018-10-12',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('18340076','黄子聿','2000-02-13','男','汉','',NULL,'','计算机类',NULL,'2018-10-19','2018-10-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `info_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_school`
--

DROP TABLE IF EXISTS `info_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_school`
--

LOCK TABLES `info_school` WRITE;
/*!40000 ALTER TABLE `info_school` DISABLE KEYS */;
INSERT INTO `info_school` VALUES (1,'数据科学与计算机学院');
/*!40000 ALTER TABLE `info_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaching_activity`
--

DROP TABLE IF EXISTS `teaching_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teaching_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `date` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `credit` double NOT NULL,
  `visualable_others` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teaching_activity_name_date_8b93b872_uniq` (`name`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaching_activity`
--

LOCK TABLES `teaching_activity` WRITE;
/*!40000 ALTER TABLE `teaching_activity` DISABLE KEYS */;
INSERT INTO `teaching_activity` VALUES (1,'组织生活会','2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,0);
/*!40000 ALTER TABLE `teaching_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaching_activity_branch`
--

DROP TABLE IF EXISTS `teaching_activity_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teaching_activity_branch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `branch_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teaching_activity_branch_activity_id_branch_id_ac2e2548_uniq` (`activity_id`,`branch_id`),
  KEY `teaching_activity_branch_branch_id_f5603176_fk_info_branch_id` (`branch_id`),
  CONSTRAINT `teaching_activity_br_activity_id_f5ddd2e9_fk_teaching_` FOREIGN KEY (`activity_id`) REFERENCES `teaching_activity` (`id`),
  CONSTRAINT `teaching_activity_branch_branch_id_f5603176_fk_info_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `info_branch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaching_activity_branch`
--

LOCK TABLES `teaching_activity_branch` WRITE;
/*!40000 ALTER TABLE `teaching_activity_branch` DISABLE KEYS */;
INSERT INTO `teaching_activity_branch` VALUES (1,1,1);
/*!40000 ALTER TABLE `teaching_activity_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaching_takepartin`
--

DROP TABLE IF EXISTS `teaching_takepartin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teaching_takepartin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `credit` double DEFAULT NULL,
  `activity_id` int(11) NOT NULL,
  `member_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teaching_takepartin_activity_id_member_id_3b4305ab_uniq` (`activity_id`,`member_id`),
  KEY `teaching_takepartin_member_id_79f6fabe_fk_info_member_netid` (`member_id`),
  CONSTRAINT `teaching_takepartin_activity_id_10744c51_fk_teaching_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `teaching_activity` (`id`),
  CONSTRAINT `teaching_takepartin_member_id_79f6fabe_fk_info_member_netid` FOREIGN KEY (`member_id`) REFERENCES `info_member` (`netid`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaching_takepartin`
--

LOCK TABLES `teaching_takepartin` WRITE;
/*!40000 ALTER TABLE `teaching_takepartin` DISABLE KEYS */;
INSERT INTO `teaching_takepartin` VALUES (32,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337109'),(33,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337113'),(34,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341061'),(35,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336117'),(36,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336141'),(37,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336095'),(38,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336101'),(39,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336102'),(40,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336121'),(41,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337071'),(42,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337098'),(43,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337108'),(44,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'15336142'),(45,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337094'),(46,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337099'),(47,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337106'),(48,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337112'),(49,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337129'),(50,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'16337154'),(51,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341073'),(52,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341074'),(53,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341095'),(54,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341096'),(55,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341097'),(56,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341099'),(57,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341105'),(58,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341114'),(59,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'17341117'),(60,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'18340069'),(61,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'18340075'),(62,'2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,1,'18340076');
/*!40000 ALTER TABLE `teaching_takepartin` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER TRI_Credit_INSERT 
BEFORE INSERT ON teaching_takepartin
FOR EACH ROW 
BEGIN 
	DECLARE L_date datetime;
	DECLARE L_date2 datetime;
	DECLARE L_credit real;
	SELECT date, end_time, credit INTO L_date, L_date2, L_credit FROM teaching_activity WHERE id=NEW.activity_id;
	SET NEW.date = L_date;
	SET NEW.end_time = L_date2;
  SET NEW.credit = L_credit;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `user_user`
--

DROP TABLE IF EXISTS `user_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user` (
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(8) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user`
--

LOCK TABLES `user_user` WRITE;
/*!40000 ALTER TABLE `user_user` DISABLE KEYS */;
INSERT INTO `user_user` VALUES (1,'000000','pbkdf2_sha256$120000$4IfAQhOuzuME$1+fY5YL8tDvjgH2q8zBHF64DMCJFrzBXVVro4Rlnp7g=','2019-02-15 12:32:36.347999','965524991@qq.com',1,1,'2019-02-09 22:47:34.804629'),(0,'16337071','pbkdf2_sha256$120000$iJ4DDXKRPYsz$V6bYqeEu4RN27AInxxllkrQmzNgCziCJW+A8vwUbbQg=','2019-02-15 12:37:52.645630','guory@mail2.sysu.edu.cn',1,1,'2019-02-09 23:59:40.662562'),(0,'16337113','pbkdf2_sha256$120000$CAoxKRgSXQuH$uw6ReylBgE+E4hCorgsmgTyHUrR/Qf/iknezESz083w=','2019-02-15 12:38:26.195786','laomd@mail2.sysu.edu.cn',1,1,'2019-02-09 23:12:00.000000'),(0,'16337260','pbkdf2_sha256$120000$LYPE6Snw1FkL$lxFa60f+YjmJVEgkzp7lJ4WYf9SM63g+95Rsx4lX020=','2019-02-15 00:15:00.000000','1053331679@qq.com',1,1,'2019-02-15 00:15:00.000000');
/*!40000 ALTER TABLE `user_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_groups`
--

DROP TABLE IF EXISTS `user_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(8) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_groups_user_id_group_id_bb60391f_uniq` (`user_id`,`group_id`),
  KEY `user_user_groups_group_id_c57f13c0_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_user_groups_group_id_c57f13c0_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_user_groups_user_id_13f9a20d_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_groups`
--

LOCK TABLES `user_user_groups` WRITE;
/*!40000 ALTER TABLE `user_user_groups` DISABLE KEYS */;
INSERT INTO `user_user_groups` VALUES (3,'16337071',1),(2,'16337113',2),(9,'16337260',2);
/*!40000 ALTER TABLE `user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(8) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq` (`user_id`,`permission_id`),
  KEY `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_user_permi_user_id_31782f58_fk_user_user` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_user_permissions`
--

LOCK TABLES `user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_bookmark`
--

DROP TABLE IF EXISTS `xadmin_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `query` varchar(1000) NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_bookmark_content_type_id_60941679_fk_django_co` (`content_type_id`),
  KEY `xadmin_bookmark_user_id_42d307fc_fk_user_user_username` (`user_id`),
  CONSTRAINT `xadmin_bookmark_content_type_id_60941679_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_bookmark`
--

LOCK TABLES `xadmin_bookmark` WRITE;
/*!40000 ALTER TABLE `xadmin_bookmark` DISABLE KEYS */;
INSERT INTO `xadmin_bookmark` VALUES (1,'测试','xadmin:teaching_takepartin_changelist','_rel_activity__id__exact=1',0,7,'16337071');
/*!40000 ALTER TABLE `xadmin_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_log`
--

DROP TABLE IF EXISTS `xadmin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` varchar(32) NOT NULL,
  `message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` (`content_type_id`),
  KEY `xadmin_log_user_id_bb16a176_fk_user_user_username` (`user_id`),
  CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_log_user_id_bb16a176_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_log`
--

LOCK TABLES `xadmin_log` WRITE;
/*!40000 ALTER TABLE `xadmin_log` DISABLE KEYS */;
INSERT INTO `xadmin_log` VALUES (55,'2019-02-14 22:11:04.915035','117.136.41.96',NULL,'','delete','批量删除 53 个 日志记录',NULL,'000000'),(56,'2019-02-15 10:38:39.974544','117.136.33.163','16337260','16337260','change','修改 groups',1,'000000'),(57,'2019-02-15 11:55:21.913322','117.136.33.163','1','出生时间->递交入党申请书时间: 6570','create','已添加。',17,'000000'),(58,'2019-02-15 11:56:29.018943','117.136.33.163','1','数据科学与计算机学院','create','已添加。',5,'000000'),(59,'2019-02-15 11:56:42.076922','117.136.33.163','1','计算机本科生第二党支部(数据科学与计算机学院)','create','已添加。',3,'000000'),(60,'2019-02-15 11:56:48.072167','117.136.33.163','2','保密党支部(数据科学与计算机学院)','create','已添加。',3,'000000'),(61,'2019-02-15 11:56:55.329069','117.136.33.163','3','计算机本科生第三党支部(数据科学与计算机学院)','create','已添加。',3,'000000'),(62,'2019-02-15 12:06:02.878741','117.136.33.163',NULL,'','delete','批量删除 1 个 发展流程依赖',NULL,'000000'),(63,'2019-02-15 12:06:10.632648','117.136.33.163','2','birth_date->application_date: 6570','create','已添加。',17,'000000'),(64,'2019-02-15 12:11:15.115769','117.136.33.163',NULL,'','delete','批量删除 1 个 成员信息',NULL,'000000'),(65,'2019-02-15 12:12:50.681875','117.136.33.163',NULL,'','delete','批量删除 1 个 成员信息',NULL,'000000'),(66,'2019-02-15 12:14:31.319236','117.136.33.163',NULL,'','delete','批量删除 1 个 成员信息',NULL,'000000'),(67,'2019-02-15 12:16:56.900465','117.136.33.163','3','application_date->activist_date: 180','create','已添加。',17,'000000'),(68,'2019-02-15 12:17:54.610071','117.136.33.163','4','activist_date->key_develop_person_date: 365','create','已添加。',17,'000000'),(69,'2019-02-15 12:18:33.381123','117.136.33.163','5','league_promotion_date->democratic_appraisal_date: 1','create','已添加。',17,'000000'),(70,'2019-02-15 12:18:53.934026','117.136.33.163','6','democratic_appraisal_date->key_develop_person_date: 1','create','已添加。',17,'000000'),(71,'2019-02-15 12:19:26.859916','117.136.33.163','7','key_develop_person_date->first_branch_conference: 90','create','已添加。',17,'000000'),(72,'2019-02-15 12:19:44.012959','117.136.33.163','8','first_branch_conference->second_branch_conference: 365','create','已添加。',17,'000000'),(73,'2019-02-15 12:20:01.076477','117.136.33.163','9','application_fullmember_date->second_branch_conference: 60','create','已添加。',17,'000000'),(74,'2019-02-15 12:33:01.726695','117.136.33.163','2','支书','change','修改 permissions',10,'000000'),(75,'2019-02-15 12:33:11.891928','117.136.33.163','3','党辅','change','修改 permissions',10,'000000');
/*!40000 ALTER TABLE `xadmin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_usersettings`
--

DROP TABLE IF EXISTS `xadmin_usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_usersettings_user_id_edeabe4a_fk_user_user_username` (`user_id`),
  CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_usersettings`
--

LOCK TABLES `xadmin_usersettings` WRITE;
/*!40000 ALTER TABLE `xadmin_usersettings` DISABLE KEYS */;
INSERT INTO `xadmin_usersettings` VALUES (1,'dashboard:home:pos','','000000'),(2,'dashboard:home:pos','','16337113'),(3,'dashboard:home:pos','','16337071'),(6,'dashboard:home:pos','','16337260'),(7,'site-theme','https://bootswatch.com/3/paper/bootstrap.min.css','16337260');
/*!40000 ALTER TABLE `xadmin_usersettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_userwidget`
--

DROP TABLE IF EXISTS `xadmin_userwidget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_userwidget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) NOT NULL,
  `widget_type` varchar(50) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_userwidget_user_id_c159233a_fk_user_user_username` (`user_id`),
  CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_user_user_username` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_userwidget`
--

LOCK TABLES `xadmin_userwidget` WRITE;
/*!40000 ALTER TABLE `xadmin_userwidget` DISABLE KEYS */;
/*!40000 ALTER TABLE `xadmin_userwidget` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-15 13:03:55