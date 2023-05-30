-- Select variant_hash from variant_hashes where variant_id = 7;

SELECT CAST(AES_DECRYPT(variant_hash, 'encryption_key') AS CHAR) AS decrypted_value
FROM variant_hashes
WHERE variant_id = 2;
