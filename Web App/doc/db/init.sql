# 创建数据库，并创建权限用户
CREATE DATABASE `ssm` CHARACTER SET utf8;
CREATE USER 'ssm'@'%' IDENTIFIED BY 'ssm';
GRANT ALL PRIVILEGES ON ssm.* TO 'ssm'@'%';
FLUSH PRIVILEGES;



CREATE TABLE `sys_user` (
  `sys_user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sys_user_login_name` varchar(50) NOT NULL,
  `sys_user_login_password` varchar(50) NOT NULL,
  `sys_user_is_delete` varchar(1) NOT NULL,
  `sys_user_register_datetime` datetime NOT NULL,
  `sys_user_email` varchar(50) DEFAULT NULL,
  `sys_user_mobile` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`sys_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;


insert  into `sys_user`(`sys_user_id`,`sys_user_login_name`,`sys_user_login_password`,`sys_user_is_delete`,`sys_user_register_datetime`,`sys_user_email`,`sys_user_mobile`) values (1,'YouMeek1','e10adc3949ba59abbe56e057f20f883e','N','2016-02-24 00:12:23','363379441@qq.com','13800000001');
insert  into `sys_user`(`sys_user_id`,`sys_user_login_name`,`sys_user_login_password`,`sys_user_is_delete`,`sys_user_register_datetime`,`sys_user_email`,`sys_user_mobile`) values (2,'YouMeek2','e10adc3949ba59abbe56e057f20f883e','N','2016-02-24 00:12:23','363379442@qq.com','13800000002');
insert  into `sys_user`(`sys_user_id`,`sys_user_login_name`,`sys_user_login_password`,`sys_user_is_delete`,`sys_user_register_datetime`,`sys_user_email`,`sys_user_mobile`) values (3,'YouMeek3','e10adc3949ba59abbe56e057f20f883e','N','2016-02-24 00:12:23','363379443@qq.com','13800000003');
insert  into `sys_user`(`sys_user_id`,`sys_user_login_name`,`sys_user_login_password`,`sys_user_is_delete`,`sys_user_register_datetime`,`sys_user_email`,`sys_user_mobile`) values (4,'YouMeek4','e10adc3949ba59abbe56e057f20f883e','N','2016-02-24 00:12:23','363379444@qq.com','13800000004');
insert  into `sys_user`(`sys_user_id`,`sys_user_login_name`,`sys_user_login_password`,`sys_user_is_delete`,`sys_user_register_datetime`,`sys_user_email`,`sys_user_mobile`) values (5,'YouMeek5','e10adc3949ba59abbe56e057f20f883e','N','2016-02-24 00:12:23','363379445@qq.com','13800000005');
