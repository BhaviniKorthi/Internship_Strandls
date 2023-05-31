-- Select variant_hash from variant_hashes where variant_id = 7;

-- SELECT variant_hash from variant_hashes;

-- SELECT *  FROM variants;
SELECT  variant_hash, MD5(variant_info) FROM variants WHERE variant_info = "Variant 5";
