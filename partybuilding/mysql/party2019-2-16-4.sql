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
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
-- /*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (2,1,2),(3,1,4),(5,1,18),(6,1,20),(12,1,28),(1,1,32),(7,1,53),(8,1,54),(9,1,55),(10,1,56),(11,1,58),(4,1,60),(13,2,2),(62,2,3),(14,2,4),(61,2,10),(15,2,16),(16,2,17),(17,2,18),(18,2,19),(19,2,20),(20,2,25),(21,2,26),(22,2,27),(23,2,28),(24,2,29),(25,2,30),(26,2,31),(27,2,32),(28,2,53),(29,2,54),(30,2,55),(31,2,56),(32,2,58),(33,2,60),(34,3,2),(60,3,3),(35,3,4),(36,3,9),(37,3,10),(38,3,11),(39,3,12),(40,3,13),(41,3,14),(42,3,15),(43,3,16),(44,3,20),(45,3,24),(46,3,25),(47,3,26),(48,3,27),(49,3,28),(50,3,29),(51,3,30),(52,3,31),(53,3,32),(54,3,53),(55,3,54),(56,3,55),(57,3,56),(58,3,58),(59,3,60);
-- /*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
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
-- --
-- -- Dumping data for table `auth_permission`
-- --
--
LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add 我的账号',1,'add_user'),(2,'Can change 我的账号',1,'change_user'),(3,'Can delete 我的账号',1,'delete_user'),(4,'Can view 我的账号',1,'view_user'),(5,'Can add application',2,'add_application'),(6,'Can change application',2,'change_application'),(7,'Can delete application',2,'delete_application'),(8,'Can view application',2,'view_application'),(9,'Can add 党支部',3,'add_branch'),(10,'Can change 党支部',3,'change_branch'),(11,'Can delete 党支部',3,'delete_branch'),(12,'Can view 党支部',3,'view_branch'),(13,'Can add 发展流程依赖',4,'add_dependency'),(14,'Can change 发展流程依赖',4,'change_dependency'),(15,'Can delete 发展流程依赖',4,'delete_dependency'),(16,'Can view 发展流程依赖',4,'view_dependency'),(17,'Can add 成员信息',5,'add_member'),(18,'Can change 成员信息',5,'change_member'),(19,'Can delete 成员信息',5,'delete_member'),(20,'Can view 成员信息',5,'view_member'),(21,'Can add 学院',6,'add_school'),(22,'Can change 学院',6,'change_school'),(23,'Can delete 学院',6,'delete_school'),(24,'Can view 学院',6,'view_school'),(25,'Can add 会议/活动',7,'add_activity'),(26,'Can change 会议/活动',7,'change_activity'),(27,'Can delete 会议/活动',7,'delete_activity'),(28,'Can view 会议/活动',7,'view_activity'),(29,'Can add 学时统计',8,'add_takepartin'),(30,'Can change 学时统计',8,'change_takepartin'),(31,'Can delete 学时统计',8,'delete_takepartin'),(32,'Can view 学时统计',8,'view_takepartin'),(33,'Can add log entry',9,'add_logentry'),(34,'Can change log entry',9,'change_logentry'),(35,'Can delete log entry',9,'delete_logentry'),(36,'Can view log entry',9,'view_logentry'),(37,'Can add permission',10,'add_permission'),(38,'Can change permission',10,'change_permission'),(39,'Can delete permission',10,'delete_permission'),(40,'Can view permission',10,'view_permission'),(41,'Can add group',11,'add_group'),(42,'Can change group',11,'change_group'),(43,'Can delete group',11,'delete_group'),(44,'Can view group',11,'view_group'),(45,'Can add content type',12,'add_contenttype'),(46,'Can change content type',12,'change_contenttype'),(47,'Can delete content type',12,'delete_contenttype'),(48,'Can view content type',12,'view_contenttype'),(49,'Can add session',13,'add_session'),(50,'Can change session',13,'change_session'),(51,'Can delete session',13,'delete_session'),(52,'Can view session',13,'view_session'),(53,'Can add Bookmark',14,'add_bookmark'),(54,'Can change Bookmark',14,'change_bookmark'),(55,'Can delete Bookmark',14,'delete_bookmark'),(56,'Can view Bookmark',14,'view_bookmark'),(57,'Can add User Setting',15,'add_usersettings'),(58,'Can change User Setting',15,'change_usersettings'),(59,'Can delete User Setting',15,'delete_usersettings'),(60,'Can view User Setting',15,'view_usersettings'),(61,'Can add User Widget',16,'add_userwidget'),(62,'Can change User Widget',16,'change_userwidget'),(63,'Can delete User Widget',16,'delete_userwidget'),(64,'Can view User Widget',16,'view_userwidget'),(65,'Can add log entry',17,'add_log'),(66,'Can change log entry',17,'change_log'),(67,'Can delete log entry',17,'delete_log'),(68,'Can view log entry',17,'view_log');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `django_admin_log`
-- --
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `django_admin_log`
-- --
--
LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `django_content_type`
-- --
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
-- --
-- -- Dumping data for table `django_content_type`
-- --
--
LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'admin','logentry'),(11,'auth','group'),(10,'auth','permission'),(12,'contenttypes','contenttype'),(2,'info','application'),(3,'info','branch'),(4,'info','dependency'),(5,'info','member'),(6,'info','school'),(13,'sessions','session'),(7,'teaching','activity'),(8,'teaching','takepartin'),(1,'user','user'),(14,'xadmin','bookmark'),(17,'xadmin','log'),(15,'xadmin','usersettings'),(16,'xadmin','userwidget');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `django_migrations`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `django_migrations`
-- --
--
LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-02-17 00:26:37.145862'),(2,'contenttypes','0002_remove_content_type_name','2019-02-17 00:26:37.210312'),(3,'auth','0001_initial','2019-02-17 00:26:37.418070'),(4,'auth','0002_alter_permission_name_max_length','2019-02-17 00:26:37.460318'),(5,'auth','0003_alter_user_email_max_length','2019-02-17 00:26:37.468058'),(6,'auth','0004_alter_user_username_opts','2019-02-17 00:26:37.476461'),(7,'auth','0005_alter_user_last_login_null','2019-02-17 00:26:37.484257'),(8,'auth','0006_require_contenttypes_0002','2019-02-17 00:26:37.488144'),(9,'auth','0007_alter_validators_add_error_messages','2019-02-17 00:26:37.496258'),(10,'auth','0008_alter_user_username_max_length','2019-02-17 00:26:37.504528'),(11,'auth','0009_alter_user_last_name_max_length','2019-02-17 00:26:37.512314'),(12,'user','0001_initial','2019-02-17 00:26:37.735984'),(13,'admin','0001_initial','2019-02-17 00:26:37.845194'),(14,'admin','0002_logentry_remove_auto_add','2019-02-17 00:26:37.894308'),(15,'admin','0003_logentry_add_action_flag_choices','2019-02-17 00:26:37.906246'),(16,'info','0001_initial','2019-02-17 00:26:38.129213'),(17,'sessions','0001_initial','2019-02-17 00:26:38.166788'),(18,'teaching','0001_initial','2019-02-17 00:26:38.416829'),(19,'xadmin','0001_initial','2019-02-17 00:26:38.662837'),(20,'xadmin','0002_log','2019-02-17 00:26:38.768231'),(21,'xadmin','0003_auto_20160715_0100','2019-02-17 00:26:38.829328');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `django_session`
-- --
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
-- --
-- -- Dumping data for table `django_session`
-- --
--
LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('332x24xp119mpuf411mmid0sns2y9z4c','OGY5MGU0MTJjNzhiZTJkMTBjNDQ4OTVlOTA1MDNhMmVjMmIyZTc3MTp7Il9hdXRoX3VzZXJfaWQiOiIxNTMzNjE0MSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODE0M2RlOGY5NjA4YmExNDU0ZjQxNTMyNmIzMWU1MDJmMWEyYjcxOCIsIm5hdl9tZW51IjoiW3tcInRpdGxlXCI6IFwiXHU1MTVhXHU1NDU4XHU1M2QxXHU1YzU1XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU2MjEwXHU1NDU4XHU0ZmUxXHU2MDZmXCIsIFwidXJsXCI6IFwiL2luZm8vbWVtYmVyL1wiLCBcImljb25cIjogXCJmYSBmYS1pbmZvXCIsIFwib3JkZXJcIjogOX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwiZmlyc3RfdXJsXCI6IFwiL2luZm8vc2Nob29sL1wifSwge1widGl0bGVcIjogXCJcdTUxNWFcdTU0NThcdTY1NTlcdTgwYjJcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTRmMWFcdThiYWUvXHU2ZDNiXHU1MmE4XCIsIFwidXJsXCI6IFwiL3RlYWNoaW5nL2FjdGl2aXR5L1wiLCBcImljb25cIjogXCJmYSBmYS11c2Vyc1wiLCBcIm9yZGVyXCI6IDEwfSwge1widGl0bGVcIjogXCJcdTViNjZcdTY1ZjZcdTdlZGZcdThiYTFcIiwgXCJ1cmxcIjogXCIvdGVhY2hpbmcvdGFrZXBhcnRpbi9cIiwgXCJpY29uXCI6IFwiZmEgZmEtYmFyLWNoYXJ0XCIsIFwib3JkZXJcIjogMTF9XSwgXCJmaXJzdF9pY29uXCI6IFwiZmEgZmEtdXNlcnNcIiwgXCJmaXJzdF91cmxcIjogXCIvdGVhY2hpbmcvYWN0aXZpdHkvXCJ9LCB7XCJ0aXRsZVwiOiBcIlx1NzUyOFx1NjIzN1wiLCBcIm1lbnVzXCI6IFt7XCJ0aXRsZVwiOiBcIlx1NjIxMVx1NzY4NFx1OGQyNlx1NTNmN1wiLCBcInVybFwiOiBcIi91c2VyL3VzZXIvXCIsIFwiaWNvblwiOiBcImZhIGZhLXZjYXJkXCIsIFwib3JkZXJcIjogNX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS12Y2FyZFwiLCBcImZpcnN0X3VybFwiOiBcIi91c2VyL3VzZXIvXCJ9XSIsIkxJU1RfUVVFUlkiOltbImluZm8iLCJtZW1iZXIiXSwiIl0sIndpemFyZF9pbmZvbWVtYmVyX2FkbWluX3dpemFyZF9mb3JtX3BsdWdpbiI6eyJzdGVwIjoiXHU1N2ZhXHU2NzJjXHU0ZmUxXHU2MDZmIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9fX0=','2019-03-03 00:30:25.082011'),('lv87oea7v61zhv76wv5cfd9caajjxhk0','ZDEwNGE0MGU1NDUzNGIxZTVlYWQ2NjhjZWI3NDk0NGYzYjQ5NjNjOTp7Il9hdXRoX3VzZXJfaWQiOiIxNjMzNzExMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjBkZWQ3ZjE5OWQ1ODJkNzBmMDZjMTNlNjBiNTA5OTkyOWMxYzU3NCIsIm5hdl9tZW51IjoiW3tcInRpdGxlXCI6IFwiXHU1MTVhXHU1NDU4XHU1M2QxXHU1YzU1XCIsIFwibWVudXNcIjogW3tcInRpdGxlXCI6IFwiXHU1M2QxXHU1YzU1XHU2ZDQxXHU3YTBiXHU0ZjlkXHU4ZDU2XCIsIFwidXJsXCI6IFwiL2luZm8vZGVwZW5kZW5jeS9cIiwgXCJpY29uXCI6IG51bGwsIFwib3JkZXJcIjogOH0sIHtcInRpdGxlXCI6IFwiXHU2MjEwXHU1NDU4XHU0ZmUxXHU2MDZmXCIsIFwidXJsXCI6IFwiL2luZm8vbWVtYmVyL1wiLCBcImljb25cIjogXCJmYSBmYS1pbmZvXCIsIFwib3JkZXJcIjogOX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS11bml2ZXJzaXR5XCIsIFwiZmlyc3RfdXJsXCI6IFwiL2luZm8vc2Nob29sL1wifSwge1widGl0bGVcIjogXCJcdTUxNWFcdTU0NThcdTY1NTlcdTgwYjJcIiwgXCJtZW51c1wiOiBbe1widGl0bGVcIjogXCJcdTRmMWFcdThiYWUvXHU2ZDNiXHU1MmE4XCIsIFwidXJsXCI6IFwiL3RlYWNoaW5nL2FjdGl2aXR5L1wiLCBcImljb25cIjogXCJmYSBmYS11c2Vyc1wiLCBcIm9yZGVyXCI6IDEwfSwge1widGl0bGVcIjogXCJcdTViNjZcdTY1ZjZcdTdlZGZcdThiYTFcIiwgXCJ1cmxcIjogXCIvdGVhY2hpbmcvdGFrZXBhcnRpbi9cIiwgXCJpY29uXCI6IFwiZmEgZmEtYmFyLWNoYXJ0XCIsIFwib3JkZXJcIjogMTF9XSwgXCJmaXJzdF9pY29uXCI6IFwiZmEgZmEtdXNlcnNcIiwgXCJmaXJzdF91cmxcIjogXCIvdGVhY2hpbmcvYWN0aXZpdHkvXCJ9LCB7XCJ0aXRsZVwiOiBcIlx1NzUyOFx1NjIzN1wiLCBcIm1lbnVzXCI6IFt7XCJ0aXRsZVwiOiBcIlx1NjIxMVx1NzY4NFx1OGQyNlx1NTNmN1wiLCBcInVybFwiOiBcIi91c2VyL3VzZXIvXCIsIFwiaWNvblwiOiBcImZhIGZhLXZjYXJkXCIsIFwib3JkZXJcIjogNX1dLCBcImZpcnN0X2ljb25cIjogXCJmYSBmYS12Y2FyZFwiLCBcImZpcnN0X3VybFwiOiBcIi91c2VyL3VzZXIvXCJ9XSIsIkxJU1RfUVVFUlkiOltbImluZm8iLCJtZW1iZXIiXSwiIl0sIndpemFyZF9pbmZvbWVtYmVyX2FkbWluX3dpemFyZF9mb3JtX3BsdWdpbiI6eyJzdGVwIjoiXHU1N2ZhXHU2NzJjXHU0ZmUxXHU2MDZmIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9fX0=','2019-03-03 00:52:56.545200');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `info_application`
-- --
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
-- --
-- -- Dumping data for table `info_application`
-- --
--
LOCK TABLES `info_application` WRITE;
/*!40000 ALTER TABLE `info_application` DISABLE KEYS */;
/*!40000 ALTER TABLE `info_application` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `info_branch`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `info_branch`
-- --
--
LOCK TABLES `info_branch` WRITE;
/*!40000 ALTER TABLE `info_branch` DISABLE KEYS */;
INSERT INTO `info_branch` VALUES (1,'计算机本科生第二党支部',NULL,1),(2,'保密党支部',NULL,1),(3,'计算机本科生第三党支部',NULL,1);
/*!40000 ALTER TABLE `info_branch` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `info_dependency`
-- --
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
-- --
-- -- Dumping data for table `info_dependency`
-- --
--
LOCK TABLES `info_dependency` WRITE;
/*!40000 ALTER TABLE `info_dependency` DISABLE KEYS */;
INSERT INTO `info_dependency` VALUES (2,'birth_date','application_date',6570),(3,'application_date','activist_date',180),(4,'activist_date','key_develop_person_date',365),(5,'league_promotion_date','democratic_appraisal_date',1),(6,'democratic_appraisal_date','key_develop_person_date',1),(7,'key_develop_person_date','first_branch_conference',90),(8,'first_branch_conference','second_branch_conference',365),(9,'application_fullmember_date','second_branch_conference',60);
/*!40000 ALTER TABLE `info_dependency` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `info_member`
-- --
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
  `credit_card_id` varchar(50) DEFAULT NULL,
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
-- --
-- -- Dumping data for table `info_member`
-- --
--
LOCK TABLES `info_member` WRITE;
/*!40000 ALTER TABLE `info_member` DISABLE KEYS */;
INSERT INTO `info_member` VALUES ('15336095','梁沛霖','1997-05-27','男','汉','广州市荔湾区360号2203','+8613435644823','440107199705270012','计算机科学与技术','2010-09-01','2016-10-20','2016-10-23','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-23','劳马东 柯司博',NULL,NULL,'2018-12-22',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('15336101','林建涛','1996-09-06','男','汉','',NULL,'','计算机类',NULL,NULL,'2016-10-21','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336102','林民钊','1997-06-25','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-11-29','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336117','刘展宏','1997-08-28','男','汉',NULL,NULL,NULL,'计算机类',NULL,NULL,'2015-10-10','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-05-12','2018-06-04','劳马东 柯司博',NULL,NULL,'2018-06-04','2018-06-12','胡凤娟','2018-06-27','2018-06-12',NULL,NULL,NULL,1),('15336121','陆剑','1997-04-18','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-11-30','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('15336141','彭博东','1996-12-24','男','汉',NULL,NULL,NULL,'计算机类',NULL,NULL,'2015-09-28','2016-09-24','2018-03-14','2018-03-16','2018-03-17','2018-03-17','2018-05-12','2018-06-04','劳马东 柯司博',NULL,NULL,'2018-06-04','2018-06-12','胡凤娟','2018-06-27','2018-06-12',NULL,NULL,NULL,1),('15336142','彭诗煜','1996-04-10','男','汉','',NULL,'','计算机类',NULL,NULL,'2015-10-10','2017-09-16',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337071','郭如意','1998-01-09','女','汉','浙江省台州市仙居县','+8615626210493','332624199801093749','信息安全',NULL,'2016-10-13','2016-10-14','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337094','黄凯欢','1997-12-19','男','汉',NULL,NULL,NULL,'计算机类',NULL,'2016-10-10','2017-03-02','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('16337098','黄义凯','1997-10-25','男','汉','',NULL,'','计算机类',NULL,'2016-10-20','2016-10-25','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10',NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337099','黄亦安','1997-08-05','男','汉','',NULL,'','计算机类',NULL,'2016-10-10','2017-02-28','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337106','解锐','1998-12-13','男','汉','重庆市云阳县双江镇莲花一街38号','+8615626225228','50023519981213067X','计算机类','2013-03-16','2016-10-10','2017-04-07','2018-03-17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('16337108','金牧','1998-08-18','女','汉','',NULL,'','计算机科学与技术',NULL,'2016-10-25','2016-10-31','2017-09-16','2018-09-12','2018-09-18','2018-09-22','2018-09-22','2018-11-10','2018-12-22','劳马东 柯司博',NULL,NULL,'2018-12-23',NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337109','柯司博','1996-12-24','男','汉',NULL,NULL,NULL,'计算机类',NULL,'2016-09-01','2015-03-01','2015-03-10','2015-03-08','2016-03-14','2016-03-15','2016-03-15','2016-03-16','2016-03-20','徐亦春 范瑞莲',NULL,NULL,'2016-03-21','2016-03-29','莫宇贵','2016-03-31','2016-06-02','2017-03-14','2017-04-23','2017-05-24',1),('16337112','兰楠','1999-10-14','女','汉','',NULL,'','计算机类',NULL,'2017-10-15','2017-10-24','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337113','劳马东','1997-02-14','男','汉','广东省湛江市遂溪县杨柑镇下山仔村41号','+8617875971360','440823199702144991','计算机科学与技术（超算方向）',NULL,'2016-09-01','2015-02-19','2015-03-08','2015-04-01','2015-04-01','2016-03-01','2016-03-01','2016-03-10','2016-03-10','陈成文 郑康明',NULL,NULL,'2016-04-05','2016-04-10','骆国丰','2016-04-20','2016-06-24','2017-03-25','2017-04-23','2017-05-24',1),('16337129','李智源','1997-07-15','男','汉','',NULL,'','计算机科学与技术',NULL,'2016-10-11','2018-03-03','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('16337154','刘海','1997-09-20','男','汉','',NULL,'','计算机类',NULL,'2016-10-19','2017-10-10','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341061','黄勇','1997-11-01','男','汉','',NULL,'','计算机类',NULL,'2017-10-20','2016-01-18','2016-02-28','2017-03-08','2017-03-08','2017-03-14','2017-03-14','2017-05-18','2017-05-18','汪绍银 席永红',NULL,NULL,'2017-05-19','2017-05-25','席永红','2017-06-20','2017-06-30','2018-05-03','2018-07-18','2020-06-27',1),('17341073','蓝靖瑜','1999-01-22','男','汉','广东省东莞市虎门镇丰泰华园山庄9栋5D','+8615626261384','441900199901221517','计算机类','2013-02-15','2017-09-01','2017-12-22','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341074','蓝煜航','1999-09-06','男','畲','福建省上杭县民兴路七巷11号','+8613246863236','350823199909064612','信息安全','2011-05-04','2017-11-20','2018-03-16','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341095','廖德洋','1997-10-27','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341096','廖浩淳','1999-08-27','男','汉族','广东省深圳市龙岗区南湾街道南晶小区二栋1609','+8613510088509','445221199908274176','计算机类','2013-05-04','2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341097','廖永滨','1999-02-05','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341099','廖泽祥','1998-08-26','男','汉族','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341105','刘晨飞','1999-12-01','男','汉','',NULL,'','计算机类',NULL,'2017-10-20','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341114','刘雨萱','1999-07-22','女','汉族','河北省唐山市路北区幸福花园','+8613242870068','130203199907225428','信息安全','2012-12-09','2018-03-21','2018-03-21','2018-09-22',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('17341117','卢曼宁','1999-06-29','女','汉','广西南宁市纬武路区直机关干休所','+8613977188261','450103199906290024','计算机类','2014-12-01','2018-03-27','2018-03-27',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('18340060','黄涵','1999-08-18','男','汉',NULL,NULL,NULL,'计算机类',NULL,'2018-10-19','2018-12-25',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('18340069','黄轩腾','2000-08-15','男','汉','福建省漳州市芗城区国道南上街农业银行304','+8615059633159','35068120000815351X','计算机类','2013-11-01','2018-10-19','2018-10-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('18340075','黄卓燊','1999-10-03','男','汉','广州市番禺区市桥大北路康富花园业兴大厦3座301','+8613286836183','441481199910030393','计算机类','2014-01-19','2018-10-19','2018-10-12',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1),('18340076','黄子聿','2000-02-13','男','汉','',NULL,'','计算机类',NULL,'2018-10-19','2018-10-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `info_member` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `info_school`
-- --
--
DROP TABLE IF EXISTS `info_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `info_school`
-- --
--
LOCK TABLES `info_school` WRITE;
/*!40000 ALTER TABLE `info_school` DISABLE KEYS */;
INSERT INTO `info_school` VALUES (1,'数据科学与计算机学院');
/*!40000 ALTER TABLE `info_school` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `teaching_activity`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `teaching_activity`
-- --
--
LOCK TABLES `teaching_activity` WRITE;
/*!40000 ALTER TABLE `teaching_activity` DISABLE KEYS */;
INSERT INTO `teaching_activity` VALUES (1,'组织生活会','2019-01-03 20:00:00.000000','2019-01-03 20:40:00.000000',1,0);
/*!40000 ALTER TABLE `teaching_activity` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `teaching_activity_branch`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `teaching_activity_branch`
-- --
--
LOCK TABLES `teaching_activity_branch` WRITE;
/*!40000 ALTER TABLE `teaching_activity_branch` DISABLE KEYS */;
INSERT INTO `teaching_activity_branch` VALUES (1,1,1);
/*!40000 ALTER TABLE `teaching_activity_branch` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `teaching_takepartin`
-- --
--
DROP TABLE IF EXISTS `teaching_takepartin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teaching_takepartin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `credit` double DEFAULT NULL,
  `activity_id` int(11) NOT NULL,
  `member_id` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teaching_takepartin_activity_id_member_id_3b4305ab_uniq` (`activity_id`,`member_id`),
  KEY `teaching_takepartin_member_id_79f6fabe_fk_info_member_netid` (`member_id`),
  CONSTRAINT `teaching_takepartin_activity_id_10744c51_fk_teaching_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `teaching_activity` (`id`),
  CONSTRAINT `teaching_takepartin_member_id_79f6fabe_fk_info_member_netid` FOREIGN KEY (`member_id`) REFERENCES `info_member` (`netid`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `teaching_takepartin`
-- --
--
LOCK TABLES `teaching_takepartin` WRITE;
/*!40000 ALTER TABLE `teaching_takepartin` DISABLE KEYS */;
INSERT INTO `teaching_takepartin` VALUES (33,1,1,'16337113'),(34,1,1,'17341061'),(35,1,1,'15336117'),(36,1,1,'15336141'),(37,1,1,'15336095'),(38,1,1,'15336101'),(39,1,1,'15336102'),(40,1,1,'15336121'),(41,1,1,'16337071'),(42,1,1,'16337098'),(43,1,1,'16337108'),(44,1,1,'15336142'),(45,1,1,'16337094'),(46,1,1,'16337099'),(47,1,1,'16337106'),(48,1,1,'16337112'),(49,1,1,'16337129'),(50,1,1,'16337154'),(51,1,1,'17341073'),(52,1,1,'17341074'),(53,1,1,'17341095'),(54,1,1,'17341096'),(55,1,1,'17341097'),(56,1,1,'17341099'),(57,1,1,'17341105'),(58,1,1,'17341114'),(59,1,1,'17341117'),(60,1,1,'18340069'),(61,1,1,'18340075'),(62,1,1,'18340076'),(64,1,1,'16337109');
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


  SET NEW.credit = L_credit;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- --
-- -- Table structure for table `user_user`
-- --
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
-- --
-- -- Dumping data for table `user_user`
-- --
--
LOCK TABLES `user_user` WRITE;
/*!40000 ALTER TABLE `user_user` DISABLE KEYS */;
INSERT INTO `user_user` VALUES (1,'000000','pbkdf2_sha256$120000$4IfAQhOuzuME$1+fY5YL8tDvjgH2q8zBHF64DMCJFrzBXVVro4Rlnp7g=','2019-02-17 00:39:30.308635','965524991@qq.com',1,1,'2019-02-09 22:47:00.000000'),(0,'100001','pbkdf2_sha256$120000$1hPukEohn6se$EKHemTe/X9OOJmF7As/uZ/7vZD+WELAGjrNzL9/f8ME=','2019-02-16 23:16:51.149653','',1,1,'2019-02-15 13:50:00.000000'),(0,'15336095','pbkdf2_sha256$120000$3S1CyC6qcoEE$H/GwOQsVYCmTYDKKl9PJISQQAihMksb2tWX/WitalJk=','2019-02-15 13:40:09.923372','943246342@qq.com',1,1,'2019-02-15 13:40:04.791453'),(0,'15336121','pbkdf2_sha256$120000$b7dZuafg2fK1$QbmsdjUaXRm3pNkFvx+1DsegM2J2LMavcO0+vdGCgpk=','2019-02-15 13:48:08.085671','1248569186@qq.com',1,1,'2019-02-15 13:47:58.209737'),(0,'16337071','pbkdf2_sha256$120000$rihQ3Uo0TtFV$XhGZ0xzt7dgZwXLsx8jt3QNtkbpifOxtVxuh0ICGuPM=','2019-02-17 00:37:48.749281','guory5@mail2.sysu.edu.cn',1,1,'2019-02-16 12:34:51.505340'),(0,'16337094','pbkdf2_sha256$120000$4yF7roeYOm1F$EpiLVuMrz9ManXLlShawvhKUxh1iNZMuzmdGAlZMPvY=','2019-02-15 20:35:01.993487','2217549130@qq.com',1,1,'2019-02-15 20:34:46.868799'),(0,'16337106','pbkdf2_sha256$120000$ICjDrCEy9TMP$K18gHLuSv5DnMk+iFTqDPBOecFXIsebbGuL+pej0mfo=','2019-02-16 12:39:30.420048','422874005@qq.com',1,1,'2019-02-16 12:24:11.097475'),(0,'16337108','pbkdf2_sha256$120000$oIZwKBGXkECP$hbUSAbJpRGxh3tFgFQ5sfJhxVZL/EYNHKlUlVErZvI4=','2019-02-15 16:10:32.155142','3463141351@qq.com',1,1,'2019-02-15 16:09:43.270776'),(0,'16337109','pbkdf2_sha256$120000$1l26xUBZmTTp$4zU/SKDjlP+xCW618Wk9PbV1SGJ4z4f4joiN6c5BDNI=','2019-02-15 19:11:01.326095','1214097402@qq.com',1,1,'2019-02-15 16:32:33.587585'),(0,'16337113','pbkdf2_sha256$120000$CAoxKRgSXQuH$uw6ReylBgE+E4hCorgsmgTyHUrR/Qf/iknezESz083w=','2019-02-17 00:40:21.691559','laomd@mail2.sysu.edu.cn',1,1,'2019-02-09 23:12:00.000000'),(0,'16337171','pbkdf2_sha256$120000$PUs25ftsRlVB$V/mVhfqHBZeuGeRVasVoqD6VMOhs0Ng+IF8ppn2eaFg=','2019-02-15 15:48:17.872059','1141574974@qq.com',1,1,'2019-02-15 15:48:05.023276'),(0,'16337260','pbkdf2_sha256$120000$LYPE6Snw1FkL$lxFa60f+YjmJVEgkzp7lJ4WYf9SM63g+95Rsx4lX020=','2019-02-16 11:22:57.706182','1053331679@qq.com',1,1,'2019-02-15 00:15:00.000000'),(0,'17341061','pbkdf2_sha256$120000$Vp848TsOUxjx$LkHaDbJapPwYJtpbCBzw5P12oi0tQTHJmQp7rqOUdRc=','2019-02-15 18:48:48.111494','1173685903@qq.com',1,1,'2019-02-15 18:48:31.535741'),(0,'17341073','pbkdf2_sha256$120000$C65cgZ6Yk6t7$dk0a9rDJqdj8J9Gcy3R0UX3nIJjbThQUF35cLsWQkZA=','2019-02-15 13:26:44.295235','463275460@qq.com',1,1,'2019-02-15 13:24:14.865594'),(0,'17341074','pbkdf2_sha256$120000$AT1x9x5TWYWe$oEmEQ0WXnvA0neFrVBXZW8YQIJn6bBWqjzBpQacD+CM=','2019-02-15 15:16:13.116728','1103597762@qq.com',1,1,'2019-02-15 15:11:09.184800'),(0,'17341087','pbkdf2_sha256$120000$HlDkgSpiCzpy$AR7F4NeGDMR32qBSZBp9gxzaapmpqkZgB1ZcgVHM2aQ=','2019-02-15 13:55:55.070946','at8397756@163.com',1,1,'2019-02-15 13:30:59.410680'),(0,'17341096','pbkdf2_sha256$120000$h4QDv3rhvEXA$HX57tMXGKXvJEzqLOj/q7wtpie3d39KPt08bJJhl8OM=','2019-02-15 18:13:16.879932','1015118636@qq.com',1,1,'2019-02-15 18:11:33.597040'),(0,'17341097','pbkdf2_sha256$120000$iQ0yt4XjfAgB$fMpzJTcJU7lnyC9+9LunSek4ros2UHzGfKwbClJKjoA=','2019-02-15 13:53:49.223142','1293338675@qq.com',1,1,'2019-02-15 13:53:39.611199'),(0,'17341114','pbkdf2_sha256$120000$u2Y8QuCCfwK9$v2YOFLPho8X6sK2ovVX+YC2x17Xxn8iSPhG2mo7ZC/E=','2019-02-16 19:54:09.257121','3044897992@qq.com',1,1,'2019-02-15 18:14:41.072356'),(0,'17341117','pbkdf2_sha256$120000$M0P5w45n4rQp$r5uujFODF+X4Fjn+53K8QO4r/WJl4XyyuZ9+/B42r1M=','2019-02-15 17:43:31.124781','729228747@qq.com',1,1,'2019-02-15 17:43:22.946148'),(0,'18340060','pbkdf2_sha256$120000$hSHOvFI3qtfp$RBJe6DTYOgKAqSmTXpjaQz1Zc/F1iz8A1unDwQFMEpA=','2019-02-15 21:31:55.287486','1770631002@qq.com',1,1,'2019-02-15 21:31:39.456144'),(0,'18340069','pbkdf2_sha256$120000$3I462IWHzmay$U/oFl8YJUDEepkQWljlZ2uL6chd2k9vKs5BFNr2qsuY=','2019-02-15 13:34:12.705886','314200068@qq.com',1,1,'2019-02-15 13:32:45.226887'),(0,'18340074','pbkdf2_sha256$120000$hpMOVg9IplvZ$ge6U+tMs1gGN0S3hwjzLytpR0Sbdy0Cy6fDRiLitnxI=','2019-02-16 00:08:24.526920','1525876369@qq.com',1,1,'2019-02-16 00:08:11.099614'),(0,'18340075','pbkdf2_sha256$120000$rzvEOwl7fFXd$jEl7DwMkPwWZ/32igEbPts10FiiOp2/rZN0p/rZb2kk=','2019-02-15 13:53:04.282804','974238840@qq.com',1,1,'2019-02-15 13:50:13.486467');
/*!40000 ALTER TABLE `user_user` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `user_user_groups`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `user_user_groups`
-- --
--
LOCK TABLES `user_user_groups` WRITE;
/*!40000 ALTER TABLE `user_user_groups` DISABLE KEYS */;
INSERT INTO `user_user_groups` VALUES (34,'100001',3),(13,'15336095',1),(14,'15336121',1),(32,'16337071',1),(28,'16337094',1),(31,'16337106',1),(21,'16337108',1),(22,'16337109',1),(2,'16337113',2),(20,'16337171',1),(9,'16337260',2),(26,'17341061',1),(10,'17341073',1),(19,'17341074',1),(11,'17341087',1),(24,'17341096',1),(18,'17341097',1),(25,'17341114',1),(23,'17341117',1),(29,'18340060',1),(12,'18340069',1),(30,'18340074',1),(15,'18340075',1);
/*!40000 ALTER TABLE `user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `user_user_user_permissions`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `user_user_user_permissions`
-- --
--
LOCK TABLES `user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `xadmin_bookmark`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `xadmin_bookmark`
-- --
--
LOCK TABLES `xadmin_bookmark` WRITE;
/*!40000 ALTER TABLE `xadmin_bookmark` DISABLE KEYS */;
INSERT INTO `xadmin_bookmark` VALUES (6,'家庭住址','重庆市','重庆市',1,4,'16337106');
/*!40000 ALTER TABLE `xadmin_bookmark` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `xadmin_log`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `xadmin_log`
-- --
--
LOCK TABLES `xadmin_log` WRITE;
/*!40000 ALTER TABLE `xadmin_log` DISABLE KEYS */;
INSERT INTO `xadmin_log` VALUES (107,'2019-02-17 00:39:46.890743','223.104.65.71','3','党辅','change','修改 permissions',11,'000000'),(108,'2019-02-17 00:40:14.101039','223.104.65.71','2','支书','change','修改 permissions',11,'000000'),(109,'2019-02-17 00:52:25.675296','223.104.65.71','3','组织生活会(3)','delete','',7,'16337113');
/*!40000 ALTER TABLE `xadmin_log` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `xadmin_usersettings`
-- --
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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- --
-- -- Dumping data for table `xadmin_usersettings`
-- --
--
LOCK TABLES `xadmin_usersettings` WRITE;
/*!40000 ALTER TABLE `xadmin_usersettings` DISABLE KEYS */;
INSERT INTO `xadmin_usersettings` VALUES (1,'dashboard:home:pos','','000000'),(2,'dashboard:home:pos','','16337113'),(6,'dashboard:home:pos','','16337260'),(7,'site-theme','https://bootswatch.com/3/paper/bootstrap.min.css','16337260'),(8,'dashboard:home:pos','','17341073'),(9,'dashboard:home:pos','','17341087'),(10,'dashboard:home:pos','','18340069'),(11,'dashboard:home:pos','','15336095'),(12,'dashboard:home:pos','','15336121'),(13,'dashboard:home:pos','','18340075'),(15,'dashboard:home:pos','','17341097'),(16,'dashboard:home:pos','','17341074'),(17,'info_member_editform_portal',',,,','17341074'),(18,'dashboard:home:pos','','16337171'),(19,'dashboard:home:pos','','16337108'),(20,'dashboard:home:pos','','16337109'),(21,'site-theme','/static/xadmin/css/themes/bootstrap-xadmin.css','16337109'),(22,'dashboard:home:pos','','17341117'),(23,'dashboard:home:pos','','17341096'),(25,'dashboard:home:pos','','17341061'),(27,'dashboard:home:pos','','16337094'),(28,'dashboard:home:pos','','18340060'),(29,'dashboard:home:pos','','18340074'),(30,'dashboard:home:pos','','16337106'),(31,'dashboard:home:pos','','16337071'),(32,'dashboard:home:pos','','17341114'),(33,'dashboard:home:pos','','100001');
/*!40000 ALTER TABLE `xadmin_usersettings` ENABLE KEYS */;
UNLOCK TABLES;
--
-- --
-- -- Table structure for table `xadmin_userwidget`
-- --
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
-- --
-- -- Dumping data for table `xadmin_userwidget`
-- --
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

-- -- Dump completed on 2019-02-17  0:54:05
