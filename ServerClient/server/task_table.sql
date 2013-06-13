--
-- Table structure for table `item_url_task`
--

CREATE TABLE IF NOT EXISTS `item_url_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iid` int(11) NOT NULL COMMENT '任务源表的记录id',
  `eid` int(11) NOT NULL COMMENT '企业id',
  `enterprise_name` varchar(300) NOT NULL DEFAULT '',
  `url` varchar(500) NOT NULL DEFAULT '' COMMENT 'url',
  `status` int(11) NOT NULL DEFAULT '-1' COMMENT '-1未领取，0领取，1完成',
  `ip` varchar(30) NOT NULL DEFAULT '' COMMENT '领取任务机器ip',
  `apply_time` varchar(30) NOT NULL DEFAULT '' COMMENT '领取时间',
  `ok_time` varchar(30) NOT NULL DEFAULT '' COMMENT '完成时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

