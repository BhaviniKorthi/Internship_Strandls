-- Select variant_hash from variant_hashes where variant_id = 7;

SELECT variant_id AS ID
FROM variant_hashes
WHERE variant_hash = MD5("v3");


SELECT variant_info AS info FROM variants WHERE variant_id = 3;