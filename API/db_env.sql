-- create a database envirement

CREATE DATABASE IF NOT EXISTS booker;

CREATE USER IF NOT EXISTS `admin`@`localhost` IDENTIFIED BY 'admin';

GRANT ALL PRIVILEGES ON booker.* TO `admin`@`localhost`;
