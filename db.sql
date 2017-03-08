SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `domain`;

CREATE TABLE `domain` (
    `id` varchar(36) NOT NULL,
    `name` varchar(64) NOT NULL,
    `enabled` bool DEFAULT 1,
    `extra` longtext,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `domain_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO domain (id, name) values ('3AF4FA64-9AFE-4481-8BB6-24F246599BF3','default');

DROP TABLE IF EXISTS `tenant`;

CREATE TABLE `tenant` (
    `id` varchar(36) NOT NULL,
    `parent_id` varchar(36) NULL,
    `domain_id` varchar(36) NOT NULL,
    `external_id` varchar(36) NULL,
    `tenant_type` enum('individual','organization') NOT NULL DEFAULT 'individual',
    `name` varchar(100) NOT NULL,
    `title` varchar(10) DEFAULT NULL,
    `email` varchar(255) DEFAULT NULL,
    `phone_mobile` varchar(25) DEFAULT NULL,
    `phone_office` varchar(25) DEFAULT NULL,
    `phone_home` varchar(25) DEFAULT NULL,
    `phone_fax` varchar(25) DEFAULT NULL,
    `idno` varchar(30) DEFAULT NULL,
    `reg` varchar(50) DEFAULT NULL,
    `taxno` varchar(50) DEFAULT NULL,
    `idtype` varchar(20) DEFAULT NULL,
    `employer` varchar(60) DEFAULT NULL,
    `designation` varchar(60) DEFAULT NULL,
    `address_line1` varchar(60) DEFAULT NULL,
    `address_line2` varchar(60) DEFAULT NULL,
    `address_line3` varchar(60) DEFAULT NULL,
    `address_city` varchar(60) DEFAULT NULL,
    `address_code` varchar(60) DEFAULT NULL,
    `address_state` varchar(60) DEFAULT NULL,
    `address_country` varchar(60) DEFAULT NULL,
    `post_line1` varchar(60) DEFAULT NULL,
    `post_line2` varchar(60) DEFAULT NULL,
    `post_line3` varchar(60) DEFAULT NULL,
    `post_city` varchar(60) DEFAULT NULL,
    `post_code` varchar(60) DEFAULT NULL,
    `post_state` varchar(60) DEFAULT NULL,
    `post_country` varchar(60) DEFAULT NULL,
    `enabled` bool DEFAULT 1,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `tenant_unique` (`domain_id`,`external_id`,`name`),
    FOREIGN KEY (`parent_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
    `id` varchar(36) NOT NULL,
    `domain_id` varchar(36) NOT NULL,
    `external_id` varchar(36) NULL,
    `tenant_id` varchar(36) NULL,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `name` varchar(100) NOT NULL,
    `title` varchar(10) NULL,
    `phone_mobile` varchar(25) DEFAULT NULL, 
    `phone_office` varchar(25) DEFAULT NULL, 
    `employer` varchar(60) DEFAULT NULL,
    `designation` varchar(60) DEFAULT NULL,
    `last_login` datetime default '0000-00-00 00:00:00',
    `enabled` bool DEFAULT 1,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`),
    FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

INSERT INTO user (id,domain_id,username,password) values ('C0418B28-CCAE-459E-8882-568F433C46FB','3AF4FA64-9AFE-4481-8BB6-24F246599BF3','root','$2b$15$Ij1uoXuF3ZAuxpg6WNZ5RuPPqcKMA80Vs7ELjzF0m/WcxQNrl4ezq');

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
    `id` varchar(36) NOT NULL,
    `name` varchar(64) NOT NULL,
    `description` varchar(128) DEFAULT NULL,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `role` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

INSERT INTO role (id,name) values ('766E2877-0E06-440A-8E02-E09988FC21A7','Root');
INSERT INTO role (id,name) values ('8dd372aa-edc4-11e6-86e1-14109fe59f3f','Operations');
INSERT INTO role (id,name) values ('9cd65b14-edc4-11e6-86e1-14109fe59f3f','Administrator');
INSERT INTO role (id,name) values ('a525e582-edc4-11e6-86e1-14109fe59f3f','AccountManager');
INSERT INTO role (id,name) values ('F4FA990F-8D08-41C4-A927-4B08D86374A0','Support');
INSERT INTO role (id,name) values ('b7706e6a-edc4-11e6-86e1-14109fe59f3f','Billing');
INSERT INTO role (id,name) values ('bced7216-edc4-11e6-86e1-14109fe59f3f','Customer');

DROP TABLE IF EXISTS `user_role`;

CREATE TABLE `user_role` (
    `id` varchar(36) NOT NULL,
    `role_id` varchar(36) NOT NULL,
    `domain_id` varchar(36) NOT NULL,
    `tenant_id` varchar(36) NULL,
    `user_id` varchar(36) NULL,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_role_tenant` (`role_id`,`domain_id`,`user_id`,`tenant_id`),
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

INSERT INTO user_role (id,role_id,domain_id,user_id) values ('5E72FF71-B34E-42CC-964F-1338E9417438','766E2877-0E06-440A-8E02-E09988FC21A7','3AF4FA64-9AFE-4481-8BB6-24F246599BF3','C0418B28-CCAE-459E-8882-568F433C46FB');

DROP TABLE IF EXISTS `token`;

CREATE TABLE `token` (
    `id` varchar(36) NOT NULL,
    `user_id` varchar(36) NOT NULL,
    `token` varchar(255) NOT NULL DEFAULT '',
    `token_expire` datetime NOT NULL default '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


SET FOREIGN_KEY_CHECKS = 1;
