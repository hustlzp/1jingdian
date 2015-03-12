-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 12, 2015 at 01:48 AM
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

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('38e41625bbba');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE IF NOT EXISTS `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `intro` text,
  `cover` varchar(200) DEFAULT NULL,
  `amazon_url` varchar(300) DEFAULT NULL,
  `douban_url` varchar(200) DEFAULT NULL,
  `pub_date` date DEFAULT NULL,
  `press` varchar(100) DEFAULT NULL,
  `pages` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `isbn` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`id`, `title`, `author`, `intro`, `cover`, `amazon_url`, `douban_url`, `pub_date`, `press`, `pages`, `price`, `isbn`) VALUES
(1, '黑客与画家', 'Paul Graham', NULL, NULL, NULL, 'http://book.douban.com/subject/6021440/', NULL, NULL, NULL, NULL, NULL);

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
  `book_id` int(11) DEFAULT NULL,
  `page` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `piece`
--

INSERT INTO `piece` (`id`, `content`, `clicks_count`, `votes_count`, `created_at`, `user_id`, `book_id`, `page`) VALUES
(1, '成功是让自己处于一种舒适的状态下生活。', 121, 1, '2015-03-07 16:00:28', 1, 1, NULL),
(2, '我们如大自然一般自然地过一天吧。不要因硬壳果或掉在轨道上的蚊虫的一只翅膀而出了轨。让我们黎明即起，不用或用早餐，平静而又无不安之感；任人去人来，让钟去敲，孩子去哭，——下个决心，好好地过一天。为什么我们要投降，甚至于随波逐流呢？', 163, 1, '2015-03-07 16:23:45', 1, 1, NULL),
(3, '一路经行处，莓苔见屐痕。白云依静渚，芳草闭闲门。过雨看松色，随山到水源。溪花与禅意，相对亦忘言。 ', 84, 0, '2015-03-07 16:31:58', 1, 1, NULL),
(4, 'Beautiful things don’t ask for attention.', 47, 0, '2015-03-07 22:56:13', 1, 1, NULL),
(5, '优秀的产品从根源上来自核心团队在这个领域独特的理解与想象，他的直觉与品位，武断与偏执。而这些，都与数字KPI全无关系。', 47, 1, '2015-03-09 09:34:04', 1, 1, NULL),
(6, '一个大学毕业生总是想“我需要一份工作”，别人也是这么对他说的，好像变成某个组织的成员是一件多么重要的事情。更直接的表达方式应该是“你需要去做一些人们需要的东西”。即使不加入公司，你也能做到。公司不过是一群人在一起工作，共同做出某种人们需要的东西。真正重要的是做出人们需要的东西，而不是加入某个公司。', 4, 0, '2015-03-11 23:09:30', 1, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `piece_comment`
--

CREATE TABLE IF NOT EXISTS `piece_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `created_at` datetime DEFAULT NULL,
  `likes_count` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_id` (`piece_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `piece_comment`
--

INSERT INTO `piece_comment` (`id`, `content`, `created_at`, `likes_count`, `user_id`, `piece_id`) VALUES
(3, '但愿人长久，千里共婵娟。', '2015-03-08 19:45:09', 0, 1, 1),
(8, '非常赞！', '2015-03-09 10:25:17', 0, 1, 5),
(9, 'ss', '2015-03-09 19:56:57', 0, 1, 5),
(10, 'sss', '2015-03-09 19:56:59', 0, 1, 5),
(11, 'sssss', '2015-03-09 19:57:01', 0, 1, 5),
(12, '倒萨', '2015-03-10 20:51:07', 0, 1, 5),
(13, '萨达倒萨', '2015-03-10 20:53:21', 0, 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `piece_comment_like`
--

CREATE TABLE IF NOT EXISTS `piece_comment_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_comment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_comment_id` (`piece_comment_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=26 ;

--
-- Dumping data for table `piece_vote`
--

INSERT INTO `piece_vote` (`id`, `created_at`, `user_id`, `piece_id`) VALUES
(16, '2015-03-08 12:57:27', 1, 2),
(18, '2015-03-08 13:01:46', 1, 1),
(25, '2015-03-11 11:10:52', 1, 5);

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
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `avatar`, `password`, `is_admin`, `created_at`, `blog`, `douban`, `motto`, `weibo`, `zhihu`) VALUES
(1, 'hustlzp', 'hustlzp@qq.com', 'c85683cc-8b36-4174-a7c2-590cc46f38dd.png', 'pbkdf2:sha1:1000$iaFZlq90$ed33ea3203bc0211e8b88f84657b7e11c4c2dfa3', 0, '2015-03-07 15:16:32', 'http://hustlzp.com', 'http://www.douban.com/people/hustlzp', '以免当我生命终结时，发现自己，从来没有活过。', 'http://weibo.com/u/2263322031', 'http://www.zhihu.com/people/hustlzp');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `piece`
--
ALTER TABLE `piece`
  ADD CONSTRAINT `piece_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `piece_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);

--
-- Constraints for table `piece_comment`
--
ALTER TABLE `piece_comment`
  ADD CONSTRAINT `piece_comment_ibfk_1` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `piece_comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_comment_like`
--
ALTER TABLE `piece_comment_like`
  ADD CONSTRAINT `piece_comment_like_ibfk_1` FOREIGN KEY (`piece_comment_id`) REFERENCES `piece_comment` (`id`),
  ADD CONSTRAINT `piece_comment_like_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `piece_vote`
--
ALTER TABLE `piece_vote`
  ADD CONSTRAINT `piece_vote_ibfk_1` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `piece_vote_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
