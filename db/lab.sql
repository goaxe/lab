-- phpMyAdmin SQL Dump
-- version 4.0.9
-- http://www.phpmyadmin.net
--
-- 主机: 127.0.0.1
-- 生成日期: 2014-09-20 16:14:32
-- 服务器版本: 5.6.14
-- PHP 版本: 5.5.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `lab`
--

-- --------------------------------------------------------

--
-- 表的结构 `alembic_version`
--

CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `renew_at` datetime DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `contact`, `avatar`, `renew_at`, `create_at`) VALUES
(1, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(2, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(3, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(4, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(5, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(6, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 18:49:31', '2014-09-19 18:49:31'),
(7, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:02', '2014-09-19 19:14:02'),
(8, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:25', '2014-09-19 19:14:25'),
(9, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:25', '2014-09-19 19:14:25'),
(10, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:25', '2014-09-19 19:14:25'),
(11, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:25', '2014-09-19 19:14:25'),
(12, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:14:25', '2014-09-19 19:14:25'),
(13, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:17:26', '2014-09-19 19:17:26'),
(14, '蛤蛤', '123@qq.com', NULL, NULL, '2014-09-19 19:17:26', '2014-09-19 19:17:26');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
