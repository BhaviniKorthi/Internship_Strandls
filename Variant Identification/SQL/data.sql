INSERT INTO variants (variant_info)
VALUES
    ("v1"),
    ("v2"),
    ("v3"),
    ("v4");
-- DELETE FROM variant_hashes;
-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE variant_hashes SET variant_hash = AES_ENCRYPT(variant_id, 'encryption_key')
-- SET SQL_SAFE_UPDATES = 1;

INSERT INTO variant_hashes (variant_id, variant_hash)
VALUES
    (1,AES_ENCRYPT("v1", 'encryption_key')),
    (2,AES_ENCRYPT('v2', 'encryption_key')),
    (3,AES_ENCRYPT('v3', 'encryption_key')),
    (4,AES_ENCRYPT('v4', 'encryption_key'))
