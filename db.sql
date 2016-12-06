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
    `name` varchar(100) NOT NULL,
    `extra` longtext,
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
    `tenant_id` varchar(36) NULL,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `last_login` datetime default '0000-00-00 00:00:00',
    `extra` longtext,
    `enabled` bool DEFAULT 1,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

INSERT INTO user (id,domain_id,username,password) values ('C0418B28-CCAE-459E-8882-568F433C46FB','3AF4FA64-9AFE-4481-8BB6-24F246599BF3','admin','$2b$15$Ij1uoXuF3ZAuxpg6WNZ5RuPPqcKMA80Vs7ELjzF0m/WcxQNrl4ezq');

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
    `id` varchar(36) NOT NULL,
    `name` varchar(64) DEFAULT NULL,
    `creation_time` DATETIME DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY `role` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

INSERT INTO role (id,name) values ('766E2877-0E06-440A-8E02-E09988FC21A7','Administrator');
INSERT INTO role (id,name) values ('F4FA990F-8D08-41C4-A927-4B08D86374A0','Support');

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

CREATE TABLE `token` (
    `id` varchar(36) NOT NULL,
    `user_id` varchar(36) NOT NULL,
    `token` varchar(255) NOT NULL DEFAULT '',
    `token_expire` datetime NOT NULL default '0000-00-00 00:00:00',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


SET FOREIGN_KEY_CHECKS = 1;
