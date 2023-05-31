sql.connector.connect(**config)


def load_data():
    count = 100
    insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
    db_cursor = db_connection.cursor(dictionary=True)
    for i in range(1, count + 1):
        variant_info = f'Variant {i}'
        variant_hash = hashlib.md5(variant_info.encode()).hexdigest()

        # Check if the variant_hash already exists in the database