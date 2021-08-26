DROP DATABASE IF EXISTS covid19status;
CREATE DATABASE covid19status;

CREATE USER 'ssac_kes'@'localhost' IDENTIFIED BY 'KES!23';
CREATE USER 'ssac_ysh'@'localhost' IDENTIFIED BY 'YSH!23';

GRANT ALL PRIVILEGES ON * . * TO 'ssac_kes'@'localhost';
GRANT ALL PRIVILEGES ON * . * TO 'ssac_ysh'@'localhost';

FLUSH PRIVILEGES;

USE covid19status;

CREATE TABLE IF NOT EXISTS daily_confirmed_cases(
	id INT(11) PRIMARY KEY auto_increment,
	dt DATE NOT NULL,
    n_domestic SMALLINT NOT NULL,
	n_international SMALLINT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS total_confirmed_cases(
	id INT(11) PRIMARY KEY auto_increment,
    city VARCHAR(2) NULL, -- 해외유입은 검역 사용
    n_confirmed_case INT(11) NOT NULL
) ENGINE=INNODB;

