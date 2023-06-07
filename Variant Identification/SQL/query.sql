use variant_db;

SELECT variant_id
FROM variants
WHERE variant_info = JSON_OBJECT(
    'name', 'Variant 1',
    'description', 'Description for Variant 1'
);
SELECT variant_id FROM variants WHERE variant_hash = MD5(JSON_OBJECT(
    'name', 'Variant 1',
    'description', 'Description for Variant 1'
));


select * from variants where variant_hash = "1b23b7287201c5b5792b6ce7b4129784";

select * from variants;
-- select variant_id, variant_hash from variants;