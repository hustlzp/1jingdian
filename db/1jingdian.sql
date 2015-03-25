-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2015 at 08:09 AM
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
('32772872fc66');

-- --------------------------------------------------------

--
-- Table structure for table `collection`
--

CREATE TABLE IF NOT EXISTS `collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `cover` varchar(200) DEFAULT NULL,
  `sm_cover` varchar(200) DEFAULT NULL,
  `desc` text,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `collection`
--

INSERT INTO `collection` (`id`, `title`, `created_at`, `cover`, `sm_cover`, `desc`, `user_id`) VALUES
(1, '李商隐', '2015-03-07 15:16:32', NULL, NULL, '春蚕到死丝方尽，蜡炬成灰泪始干。', 1),
(2, '禅', '2015-03-07 15:16:32', NULL, NULL, NULL, 1),
(3, '电影台词', '2015-03-07 15:16:32', NULL, NULL, NULL, 1),
(4, '歌词', '2015-03-07 15:16:32', NULL, NULL, NULL, 1),
(5, '自然', '2015-03-07 15:16:32', NULL, NULL, NULL, 1),
(6, '爱情', '2015-03-14 20:46:29', NULL, NULL, '', 1),
(7, '生活', '2015-03-14 20:57:12', NULL, NULL, '', 1),
(8, '呵呵', '2015-03-16 10:21:19', NULL, NULL, '', 1),
(9, 'ss', '2015-03-19 19:13:36', NULL, NULL, '', 1),
(10, 'sss', '2015-03-21 21:25:26', NULL, NULL, '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `collection_piece`
--

CREATE TABLE IF NOT EXISTS `collection_piece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `collection_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  `collection_owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `collection_id` (`collection_id`),
  KEY `piece_id` (`piece_id`),
  KEY `collection_owner_id` (`collection_owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=47 ;

--
-- Dumping data for table `collection_piece`
--

INSERT INTO `collection_piece` (`id`, `created_at`, `collection_id`, `piece_id`, `collection_owner_id`) VALUES
(36, '2015-03-15 12:34:18', 6, 8, 1),
(39, '2015-03-16 09:56:17', 6, 12, 1),
(40, '2015-03-16 09:56:17', 8, 12, 1),
(43, '2015-03-16 09:56:17', 7, 12, 1),
(44, '2015-03-19 19:11:15', 9, 14, 1),
(45, '2015-03-21 20:06:56', 10, 16, 1),
(46, '2015-03-21 20:06:56', 10, 17, 1);

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
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=20 ;

--
-- Dumping data for table `piece`
--

INSERT INTO `piece` (`id`, `content`, `clicks_count`, `votes_count`, `created_at`, `user_id`, `source`, `original`, `author`, `source_link`, `source_link_title`) VALUES
(1, '成功是让自己处于一种舒适的状态下生活。', 130, 0, '2015-03-07 16:00:28', 1, '黑客', 0, '马超', '', NULL),
(2, '我们如大自然一般自然地过一天吧。不要因硬壳果或掉在轨道上的蚊虫的一只翅膀而出了轨。让我们黎明即起，不用或用早餐，平静而又无不安之感；任人去人来，让钟去敲，孩子去哭，——下个决心，好好地过一天。为什么我们要投降，甚至于随波逐流呢？', 180, 0, '2015-03-07 16:23:45', 1, '瓦尔登湖', 0, '梭罗', '', NULL),
(3, '一路经行处，莓苔见屐痕。白云依静渚，芳草闭闲门。过雨看松色，随山到水源。溪花与禅意，相对亦忘言。 ', 103, 0, '2015-03-07 16:31:58', 1, '黑客', NULL, NULL, NULL, NULL),
(4, 'Beautiful things don’t ask for attention.', 54, 0, '2015-03-07 22:56:13', 1, '黑客', NULL, NULL, NULL, NULL),
(5, '优秀的产品从根源上来自核心团队在这个领域独特的理解与想象，他的直觉与品位，武断与偏执。而这些，都与数字KPI全无关系。', 56, 0, '2015-03-09 09:34:04', 1, '黑客', NULL, NULL, NULL, NULL),
(6, '一个大学毕业生总是想“我需要一份工作”，别人也是这么对他说的，好像变成某个组织的成员是一件多么重要的事情。更直接的表达方式应该是“你需要去做一些人们需要的东西”。即使不加入公司，你也能做到。公司不过是一群人在一起工作，共同做出某种人们需要的东西。真正重要的是做出人们需要的东西，而不是加入某个公司。', 20, 0, '2015-03-11 23:09:30', 1, '黑客与画家', NULL, 'Paul Graham', NULL, NULL),
(7, '一个大学毕业生总是想“我需要一份工作”，别人也是这么对他说的，好像变成某个组织的成员是一件多么重要的事情。更直接的表达方式应该是“你需要去做一些人们需要的东西”。即使不加入公司，你也能做到。公司不过是一群人在一起工作，共同做出某种人们需要的东西。真正重要的是做出人们需要的东西，而不是加入某个公司。', 48, 0, '2015-03-12 12:31:07', 1, '黑客与画家', 1, NULL, NULL, NULL),
(8, '我步入丛林，因为我希望生活有意义。我希望活的深刻，吸取生命中所有的精华，把非生命的一切都击溃。以免当我的生命终结，发现自己从来没有活过。', 67, 0, '2015-03-13 23:59:07', 1, '瓦尔登湖', 0, '梭罗', NULL, NULL),
(9, '人类在过着静静的绝望的生活。所谓听天由命，正是肯定的绝望。你从绝望的城市走到绝望的村庄，以水貂和麝鼠的勇敢来安慰自己。在人类的所谓游戏与消遣底下，甚至都隐藏着一种凝固的、不知又不觉的绝望。两者中都没有娱乐可言，因为工作之后才能娱乐。可是不做绝望的事，才是智慧的一种表征。', 58, 0, '2015-03-15 00:09:14', 1, '', 1, '', NULL, NULL),
(10, '人类在过着静静的绝望的生活。所谓听天由命，正是肯定的绝望。你从绝望的城市走到绝望的村庄，以水貂和麝鼠的勇敢来安慰自己。在人类的所谓游戏与消遣底下，甚至都隐藏着一种凝固的、不知又不觉的绝望。两者中都没有娱乐可言，因为工作之后才能娱乐。可是不做绝望的事，才是智慧的一种表征。', 8, 1, '2015-03-14 00:25:48', 1, '', 1, '', NULL, NULL),
(11, '使生如夏花之绚烂，死如秋叶之静美。', 46, 1, '2015-03-15 12:31:57', 1, '', 0, '', NULL, NULL),
(12, '人生中出现的一切，都无法拥有，只能经历。深知这一点的人，就会懂得：无所谓失去，而只是经过而已；亦无所谓失败，而只是经验而已。用一颗浏览的心，去看待人生，一切的得与失、隐与显，都是风景与风情……', 235, 1, '2015-03-16 10:52:03', 1, '要怎样努力，才能成为很厉害的人？', 0, '朱炫', 'http://www.douban.com', NULL),
(13, '天地不仁，以万物为刍狗。', 95, 0, '2015-03-16 20:01:12', 1, '', 0, '', NULL, NULL),
(14, 'WTF', 146, 0, '2015-03-19 19:13:29', 1, '', 0, '', NULL, NULL),
(15, 'WTF', 123, 0, '2015-03-20 19:08:07', 1, '', 0, '', NULL, NULL),
(16, '麻雀看见孔雀负担着它的翎尾，替它担忧。The sparrow is sorry for the peacock at the burden of its tail.', 186, 1, '2015-03-21 00:06:13', 1, '飞鸟集', 0, '泰戈尔', 'http://www.douban.com', NULL),
(17, '世界对着它的爱人，把它浩翰的面具揭下了。它变小了，小如一首歌，小如一回永恒的接吻。The world puts off its mask of vastness to its lover. It becomes small as one song, as one kiss of the eternal. ', 115, 0, '2015-03-21 16:26:34', 1, '', 0, '', '', NULL),
(18, 'WTF', 11, 0, '2015-03-22 12:30:28', 1, '', 0, '', '', NULL),
(19, 'WTF', 15, 0, '2015-03-22 12:30:32', 1, '', 0, '', '', NULL);

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
  `likes_count` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `piece_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `piece_id` (`piece_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=63 ;

--
-- Dumping data for table `piece_comment`
--

INSERT INTO `piece_comment` (`id`, `content`, `created_at`, `likes_count`, `user_id`, `piece_id`) VALUES
(32, 'dsadsa', '2015-03-20 18:02:12', 0, 1, 14),
(33, '的撒旦撒旦', '2015-03-20 18:02:18', 0, 1, 14),
(42, '的撒旦撒旦', '2015-03-20 18:08:55', 0, 1, 14),
(43, '的撒旦撒旦', '2015-03-20 18:08:57', 0, 1, 14),
(49, 'ss', '2015-03-20 18:10:20', 0, 1, 14),
(50, 'hustlzp 1 分钟前\n的撒旦撒旦', '2015-03-20 18:10:48', 0, 1, 14),
(51, 'dsa', '2015-03-20 18:10:54', 0, 1, 14),
(52, '萨达是', '2015-03-20 18:11:46', 0, 1, 14),
(53, '打算打算萨达', '2015-03-20 18:11:53', 0, 1, 14),
(54, '倒萨倒萨倒萨', '2015-03-20 18:12:00', 0, 1, 14),
(55, '实打实大师', '2015-03-20 18:12:04', 0, 1, 14),
(56, 'dasdsadsa', '2015-03-20 18:12:57', 0, 1, 14),
(57, 'dasdasdsad', '2015-03-20 18:13:11', 0, 1, 14),
(58, '是大大撒', '2015-03-20 18:13:16', 0, 1, 14),
(59, '大师的撒的撒', '2015-03-20 18:13:28', 0, 1, 14),
(60, '实打实', '2015-03-20 18:15:11', 0, 1, 14),
(61, '打算打算撒打算', '2015-03-20 18:15:15', 0, 1, 14),
(62, '的萨达萨达萨达是', '2015-03-20 18:15:25', 0, 1, 14);

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
-- Table structure for table `piece_source`
--

CREATE TABLE IF NOT EXISTS `piece_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `piece_source`
--

INSERT INTO `piece_source` (`id`, `name`, `count`, `created_at`) VALUES
(2, '瓦尔登湖', 1, '2015-03-21 13:07:19'),
(3, '科德康角', 0, '2015-03-21 13:09:35'),
(4, '飞鸟集', 1, '2015-03-21 21:33:47'),
(5, '泰戈尔', 1, '2015-03-21 21:33:47'),
(6, '梭罗', 1, '2015-03-22 09:29:34'),
(7, '马超', 1, '2015-03-22 15:47:31');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=45 ;

--
-- Dumping data for table `piece_vote`
--

INSERT INTO `piece_vote` (`id`, `created_at`, `user_id`, `piece_id`) VALUES
(35, '2015-03-15 12:26:08', 1, 10),
(41, '2015-03-15 23:54:25', 1, 11),
(43, '2015-03-17 00:57:32', 1, 12),
(44, '2015-03-21 15:31:12', 1, 16);

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
  `collections_count` int(11) DEFAULT NULL,
  `pieces_count` int(11) DEFAULT NULL,
  `votes_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `avatar`, `password`, `is_admin`, `created_at`, `blog`, `douban`, `motto`, `weibo`, `zhihu`, `collections_count`, `pieces_count`, `votes_count`) VALUES
(1, 'hustlzp', 'hustlzp@qq.com', 'c85683cc-8b36-4174-a7c2-590cc46f38dd.png', 'pbkdf2:sha1:1000$iaFZlq90$ed33ea3203bc0211e8b88f84657b7e11c4c2dfa3', 1, '2015-03-07 15:16:32', 'http://hustlzp.com', 'http://www.douban.com/people/hustlzp', '以免当我生命终结时，发现自己，从来没有活过。', 'http://weibo.com/u/2263322031', 'http://www.zhihu.com/people/hustlzp', 10, 19, 4);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `collection`
--
ALTER TABLE `collection`
  ADD CONSTRAINT `collection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `collection_piece`
--
ALTER TABLE `collection_piece`
  ADD CONSTRAINT `collection_piece_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`),
  ADD CONSTRAINT `collection_piece_ibfk_2` FOREIGN KEY (`piece_id`) REFERENCES `piece` (`id`),
  ADD CONSTRAINT `collection_piece_ibfk_3` FOREIGN KEY (`collection_owner_id`) REFERENCES `user` (`id`);

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
