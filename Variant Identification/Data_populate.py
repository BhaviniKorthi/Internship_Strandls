import mysql.connector
import hashlib
import json

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'auth_plugin': 'mysql_native_password'
}

db_connection = mysql.connector.connect(**config)


def load_data():
    count = 100
    insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
    check_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
    db_cursor = db_connection.cursor(dictionary=True)
    for i in range(1, count + 1):
        variant_data = {
            'name': f'Variant {i}',
            'description': f'Description for Variant {i}',
        }
        variant_info = json.dumps(variant_data)

        db_cursor.execute(check_query, (variant_info,))
        count = db_cursor.fetchall()# Consume and discard unread result sets

        result = db_cursor.fetchone()
        # print(result)

        if len(count)>0:
            continue
        else:
            db_cursor.execute(insert_query, (variant_info, variant_info))
            db_connection.commit()

    db_cursor.close()


load_data()
