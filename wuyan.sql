/*
Navicat MySQL Data Transfer

Source Server         : awesome
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : wuyan

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-02-13 15:34:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blogs
-- ----------------------------
DROP TABLE IF EXISTS `blogs`;
CREATE TABLE `blogs` (
  `id` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_image` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `summary` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of blogs
-- ----------------------------

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` varchar(255) NOT NULL,
  `blog_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_image` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `passwd` varchar(255) DEFAULT NULL,
  `admin` tinyint(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (null, 'wuyan', '847728225@qq.com', '123456', '1', null, null);
INSERT INTO `users` VALUES (null, 'richard', '1158944720@qq.com', '784319', '0', null, '');
INSERT INTO `users` VALUES (null, 'Auggie', '2290260547@qq.com', '634519', '0', null, null);
INSERT INTO `users` VALUES ('001518493901034649a16fb827047bb8e0dcfd861a44fba000', 'caowenqiao', '555555@qq.com', 'd15d1b035362e8bd4dd975f229f0483b1dfe6bda', '0', 'http://www.gravatar.com/avatar/87eacea84fa0decdd7881cb0a02eed2e?d=mm&s=120', '1518493901.03482');
INSERT INTO `users` VALUES ('001518494114079aae745fbf7d143628368318c5164210a000', 'xiaoqiao', '2290260546@qq.com', '4cdf3f1921db04258724704141c8cd58fa9cd44e', '0', 'http://www.gravatar.com/avatar/36c119fa94324a282aefd0da03f2c6db?d=mm&s=120', '1518494114.07982');
INSERT INTO `users` VALUES ('0015184943958988c814fb7757a45328c5e3ca8283d0cb8000', 'daqiao', '9965733150@qq.com', '0d90a08b57d255c4e2e343271a0a3feb608b0678', '0', 'http://www.gravatar.com/avatar/1239414a4c6d20bc197f9d9026e94b51?d=mm&s=120', '1518494395.89882');
INSERT INTO `users` VALUES ('001518494554741dc5e8f1857ef47abac317b4e8f1bd6d9000', 'Brian', '849928558@qq.com', 'a2ebe573d1c0796ea43d7e7704a92ac9951beeff', '0', 'http://www.gravatar.com/avatar/32086e2d9c728e37c0961c8183d8c69d?d=mm&s=120', '1518494554.74182');
