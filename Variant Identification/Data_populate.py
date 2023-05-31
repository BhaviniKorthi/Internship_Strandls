import mysql.connector
import  hashlib
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'auth_plugin': 'mysql_native_password'
}

db_connection = mysql.connector.connect(**config)


# def load_data():
    # count = 100
    # insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
    # db_cursor = db_connection.cursor(dictionary=True)
    # for i in range(1, count + 1):
    #     db_cursor.execute(insert_query, (f'Variant {i}', f'Variant {i}'))
    # db_connection.commit()


def load_data():
    count = 100
    insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
    db_cursor = db_connection.cursor(dictionary=True)
    for i in range(1, count + 1):
        variant_info = f'Variant {i}'
        check_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        db_cursor.execute(check_query, (variant_info,))
        result = db_cursor.fetchone()

        if result:
          
            info_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s) AND variant_info = %s"
            db_cursor.execute(info_query, (variant_info, variant_info))
            result = db_cursor.fetchone()

            if not result:
                db_cursor.execute(insert_query, (variant_info, variant_info))
        else:
            db_cursor.execute(insert_query, (variant_info, variant_info))
    
    db_connection.commit()


load_data()
