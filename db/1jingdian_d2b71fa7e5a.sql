-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2015 at 12:35 PM
-- Server version: 5.6.15
-- PHP Version: 5.5.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1jingdian`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `click_log`
--

CREATE TABLE IF NOT EXISTS `click_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `collection`
--

CREATE TABLE IF NOT EXISTS `collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `cover` varchar(200) DEFAULT NULL,
  `desc` text,
  `kind_id` int(11) DEFAULT NULL,
  `locked` tinyint(1) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kind_id` (`kind_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=26 ;

-- --------------------------------------------------------

--
-- Table structure for table `collection_edit_log`
--

CREATE TABLE IF NOT EXISTS `collection_edit_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `kind` int(11) NOT NULL,
  `before` varchar(200) DEFAULT NULL,
  `before_id` int(11) DEFAULT NULL,
  `after` varchar(200) DEFAULT NULL,
  `after_id` int(11) DEFAULT NULL,
  `compare` varchar(500) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `collection_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `collection_id` (`collection_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

-- --------------------------------------------------------

--
-- Table structure for table `collection_edit_log_report`
--

CREATE TABLE IF NOT EXISTS `collection_edit_log_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `collection_edit_log_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `collection_edit_log_id` (`collection_edit_log_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `collection_kind`
--

CREATE TABLE IF NOT EXISTS `collection_kind` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `collection_piece`
--

CREATE TABLE IF NOT EXISTS `collection_piece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `collection_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `collection_id` (`collection_id`),
  KEY `piece_id` (`piece_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=100 ;

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE IF NOT EXISTS `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `created_at` datetime DEFAULT NULL,
  `processed` tinyint(1) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `invitation_code`
--

CREATE TABLE IF NOT EXISTS `invitation_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `used` tinyint(1) DEFAULT NULL,
  `sended_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

-- --------------------------------------------------------

--
-- Table structure for table `mail_log`
--

CREATE TABLE IF NOT EXISTS `mail_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE IF NOT EXISTS `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kind` int(11) NOT NULL,
  `target` varchar(100) DEFAULT NULL,
  `content` text,
  `link` varchar(200) DEFAULT NULL,
  `checked` tinyint(1) NOT NULL,
  `checked_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `sender_id` (`sender_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece`
--

CREATE TABLE IF NOT EXISTS `piece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `clicks_count` int(11) DEFAULT NULL,
  `votes_count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `original` tinyint(1) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `source_link` varchar(200) DEFAULT NULL,
  `source_link_title` varchar(200) DEFAULT NULL,
  `qrcode` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=31 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_author`
--

CREATE TABLE IF NOT EXISTS `piece_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_comment`
--

CREATE TABLE IF NOT EXISTS `piece_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  `votes_count` int(11) DEFAULT NULL,
  `root_comment_id` int(11) DEFAULT NULL,
  `target_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_id` (`piece_id`),
  KEY `user_id` (`user_id`),
  KEY `root_comment_id` (`root_comment_id`),
  KEY `target_user_id` (`target_user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=116 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_comment_vote`
--

CREATE TABLE IF NOT EXISTS `piece_comment_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_comment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_comment_id` (`piece_comment_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=36 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_edit_log`
--

CREATE TABLE IF NOT EXISTS `piece_edit_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  `kind` int(11) NOT NULL,
  `after` varchar(200) DEFAULT NULL,
  `after_id` int(11) DEFAULT NULL,
  `before` varchar(200) DEFAULT NULL,
  `before_id` int(11) DEFAULT NULL,
  `compare` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_id` (`piece_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=52 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_edit_log_report`
--

CREATE TABLE IF NOT EXISTS `piece_edit_log_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_edit_log_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `piece_edit_log_id` (`piece_edit_log_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_source`
--

CREATE TABLE IF NOT EXISTS `piece_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

-- --------------------------------------------------------

--
-- Table structure for table `piece_vote`
--

CREATE TABLE IF NOT EXISTS `piece_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_id` (`piece_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=47 ;

-- --------------------------------------------------------

--
-- Table structure for table `search_log`
--

CREATE TABLE IF NOT EXISTS `search_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `blog` varchar(100) DEFAULT NULL,
  `douban` varchar(100) DEFAULT NULL,
  `motto` varchar(100) DEFAULT NULL,
  `weibo` varchar(100) DEFAULT NULL,
  `zhihu` varchar(100) DEFAULT NULL,
  `pieces_count` int(11) DEFAULT NULL,
  `votes_count` int(11) DEFAULT NULL,
  `liked_collections_count` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `user_like_collection`
--

CREATE TABLE IF NOT EXISTS `user_like_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `collection_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `collection_id` (`collection_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=26 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `click_log`
--
ALTER TABLE `click_log`
  ADD CONSTRAINT `click_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `collection`
--
ALTER TABLE `collection`
  ADD CONSTRAINT `collection_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `collection_ibfk_1` FOREIGN KEY (`kind_id`) REFERENCES `collection_kind` (`id`);

--
-- Constraints for table `collection_edit_log`
--
ALTER TABLE `collection_edit_log`
  ADD CONSTRAINT `collection_edit_log_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`),
  ADD CONSTRAINT `collection_edit_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `collection_edit_log_report`
--
ALTER TABLE `collection_edit_log_report`
  ADD CONSTRAINT `collection_edit_log_report_ibfk_1` FOREIGN KEY (`collection_edit_log_id`) REFERENCES `collection_edit_log` (`id`),
  ADD CONSTRAINT `collection_edit_log_report_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `collection_piece`
--
ALTER TABLE `collection_piece`
  ADD CONSTRAINT `collection_piece_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`),
  ADD CONSTRAINT `collection_piece_ibfk_2` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`);

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `invitation_code`
--
ALTER TABLE `invitation_code`
  ADD CONSTRAINT `invitation_code_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `notification_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece`
--
ALTER TABLE `piece`
  ADD CONSTRAINT `piece_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_comment`
--
ALTER TABLE `piece_comment`
  ADD CONSTRAINT `piece_comment_ibfk_1` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `piece_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `piece_comment_ibfk_3` FOREIGN KEY (`root_comment_id`) REFERENCES `piece_comment` (`id`),
  ADD CONSTRAINT `piece_comment_ibfk_4` FOREIGN KEY (`target_user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_comment_vote`
--
ALTER TABLE `piece_comment_vote`
  ADD CONSTRAINT `piece_comment_vote_ibfk_1` FOREIGN KEY (`piece_comment_id`) REFERENCES `piece_comment` (`id`),
  ADD CONSTRAINT `piece_comment_vote_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_edit_log`
--
ALTER TABLE `piece_edit_log`
  ADD CONSTRAINT `piece_edit_log_ibfk_2` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `piece_edit_log_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_edit_log_report`
--
ALTER TABLE `piece_edit_log_report`
  ADD CONSTRAINT `piece_edit_log_report_ibfk_3` FOREIGN KEY (`piece_edit_log_id`) REFERENCES `piece_edit_log` (`id`),
  ADD CONSTRAINT `piece_edit_log_report_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_vote`
--
ALTER TABLE `piece_vote`
  ADD CONSTRAINT `piece_vote_ibfk_1` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `piece_vote_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `search_log`
--
ALTER TABLE `search_log`
  ADD CONSTRAINT `search_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `user_like_collection`
--
ALTER TABLE `user_like_collection`
  ADD CONSTRAINT `user_like_collection_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`),
  ADD CONSTRAINT `user_like_collection_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
