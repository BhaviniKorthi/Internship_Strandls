INSERT INTO variants (variant_info)
VALUES
    ("v1"),
    ("v2"),
    ("v3"),
    ("v4");

INSERT INTO variant_hashes (variant_id, variant_hash)
VALUES
    (1,MD5("v1")),
    (2,MD5('v2')),
    (3,MD5('v3')),
    (4,MD5('v4'))
