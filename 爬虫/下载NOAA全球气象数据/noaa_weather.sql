DROP TABLE IF EXISTS `data`;
CREATE TABLE `data` (
  `station` char(11) NOT NULL comment '站点ID',
  `date` date NOT NULL comment '日期',
  `latitude` float DEFAULT NULL comment '纬度',
  `longitude` float DEFAULT NULL comment '经度',
  `elevation` float DEFAULT NULL comment '海拔',
  `name` varchar(50) DEFAULT NULL comment '城市英文名',
  `temp` float DEFAULT NULL comment '平均温度',
  `temp_attributes` int DEFAULT NULL comment '计算平均温度的观测次数',
  `dewp` float DEFAULT NULL comment '平均露点',
  `dewp_attributes` int DEFAULT NULL comment '计算平均露点的观测次数',
  `slp` float DEFAULT NULL comment '海平面压力',
  `slp_attributes` int DEFAULT NULL comment '计算海平面压力的观测次数',
  `stp` float DEFAULT NULL comment '当天平均站压',
  `stp_attributes` int DEFAULT NULL comment '平均站压的观测次数',
  `visib` float DEFAULT NULL comment '能见度',
  `visib_attributes` int DEFAULT NULL comment '能见度观测次数',
  `wdsp` float DEFAULT NULL comment '平均风速',
  `wdsp_attributes` int DEFAULT NULL comment '计算平均风速的观测次数',
  `mxspd` float DEFAULT NULL comment '最大持续风速',
  `gust` float DEFAULT NULL comment '最大阵风',
  `max` float DEFAULT NULL comment '最高气温',
  `max_attributes` varchar(10) DEFAULT NULL comment '空白表示最高明确温度而非小时数据',
  `min` float DEFAULT NULL comment '最低气温',
  `min_attributes` varchar(10) DEFAULT NULL comment '空白表示最低明确温度而非小时数据',
  `prcp` float DEFAULT 0 comment '降雨量',
  `prcp_attributes` char(1) DEFAULT NULL comment '取值ABCDEFGH分别代表A 1-6小时 B 2-6小时 C 3-6小时 D 4-6小时 E 1-12小时 F 2-12小时 G 1-24小时即全天 HI不完整降雨记录 一般值为G',
  `sndp` float DEFAULT NULL comment '降雪量',
  `frshtt` char(6) DEFAULT '000000' comment '发生气象事件的概率默认0代表未发生1代表发生,六位分别代表Fog雾Rain雨Snow雪Hail冰雹Thunder雷电Tornado龙卷风',
  PRIMARY KEY (station, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `info`;
CREATE TABLE `info` (
  `station_id` char(11) NOT NULL comment '站点ID',
  `name` varchar(50) NULL comment '城市英文名',
  `latitude` float DEFAULT NULL comment '纬度',
  `longitude` float DEFAULT NULL comment '经度',
  `country` varchar(20) DEFAULT NULL comment '国家',
  `province` varchar(20) DEFAULT NULL comment '省',
  `city` varchar(20) DEFAULT NULL comment '城市',
  `district` varchar(20) DEFAULT NULL comment '县',
  PRIMARY KEY (station_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;