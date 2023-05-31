show databases;
-- DROP database variant_db;
-- CREATE DATABASE variant_db;
USE variant_db;
-- DROP TABLE variants;
-- DROP TABLE variant_hashes;
CREATE TABLE variants (
    variant_id INT PRIMARY KEY AUTO_INCREMENT,
    variant_info VARCHAR(300),
    variant_hash VARCHAR(255),
    INDEX idx_variant_hash (variant_hash)
);

