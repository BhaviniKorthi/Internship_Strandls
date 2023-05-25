show databases;
drop database bhavini_sample;
create database bhavini_sample;
use bhavini_sample;
create table Sample(
	name varchar(20) NOT NULL,
    gender varchar(10) NOT NULL,
    phone numeric(10) NOT NULL UNIQUE,
    roll_number numeric(8) NOT NULL UNIQUE,
    email_id varchar(100),
    PRIMARY KEY (roll_number)
    
);