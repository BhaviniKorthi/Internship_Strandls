-- Select variant_hash from variant_hashes where variant_id = 7;

-- SELECT variant_hash from variant_hashes;

-- SELECT *  FROM variants;
SELECT  variant_id, variant_info  FROM variants WHERE variant_hash = MD5("Variant 5");
-- INSERT INTO variants (variant_info, variant_hash) VALUES ("Variant 1000", MD5("Variant 5"));