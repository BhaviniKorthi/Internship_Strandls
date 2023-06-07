show databases;
-- DROP database variant_db;
-- CREATE DATABASE variant_db;
USE variant_db;
-- DROP TABLE variants;

CREATE TABLE variants (
    variant_id INT PRIMARY KEY AUTO_INCREMENT,
    variant_info JSON,
    variant_hash VARCHAR(255),
    INDEX idx_variant_hash (variant_hash)
);

