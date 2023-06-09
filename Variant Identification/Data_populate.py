import mysql.connector
import hashlib
import json


class Populate:

    def __init__(self, db_connection):
        self.db_connection = db_connection


    def load_data(self):
        query = "SELECT COUNT(*) AS count FROM variants"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query)
        check = db_cursor.fetchone()
        print(check)
        if check['count'] == 0:
            count = 100
            insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
            check_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
            db_cursor = self.db_connection.cursor(dictionary=True)
            for i in range(1, count + 1):
                variant_data = {
                    'name': f'Variant {i}',
                    'description': f'Description for Variant {i}',
                }
                variant_info = json.dumps(variant_data)

                db_cursor.execute(check_query, (variant_info,))
                count = db_cursor.fetchall()

                result = db_cursor.fetchone()
                # print(result)

                if len(count)>0:
                    continue
                else:
                    db_cursor.execute(insert_query, (variant_info, variant_info))
                    self.db_connection.commit()

        db_cursor.close()


# load_data()
