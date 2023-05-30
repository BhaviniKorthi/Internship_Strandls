show databases;
DROP database variant_db;
CREATE DATABASE variant_db;
USE variant_db;
-- DROP TABLE variants;
-- DROP TABLE variant_hashes;
CREATE TABLE variants (
	variant_id INT PRIMARY KEY AUTO_INCREMENT,
    variant_info VARCHAR(20)
);

CREATE TABLE variant_hashes (
    variant_hash VARBINARY(255),
    variant_id INT,
    PRIMARY KEY (variant_id)
    
);

