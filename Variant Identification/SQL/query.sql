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
SELECT variant_id, variant_info FROM variants WHERE variant_info IN (JSON_OBJECT(
    'name', 'Variant 1',
    'description', 'Description for Variant 1'
));

select * from variants where variant_id = 101;
insert into variants (variant_id, variant_info, variant_hash) values (101, JSON_OBJECT(
    'name', 'Variant 1',
    'description', 'Description for Variant 1'
), MD5(JSON_OBJECT(
    'name', 'Variant 101',
    'description', 'Description for Variant 101'
))) ;

select * from variants;

insert into variants (variant_id, variant_info , variant_hash) values (122, JSON_OBJECT(
    'name', 'Variant 122',
    'description', 'Description for Variant 122'
), "a227b159aee3d85476d63bb30c141d6d");

SELECT variant_id, variant_info FROM variants WHERE variant_hash IN ("a227b159aee3d85476d63bb30c141d6d", "1b23b7287201c5b5792b6ce7b4129784");

TRUNCATE TABLE variants;
