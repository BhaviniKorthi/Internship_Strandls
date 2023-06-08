import json

class VariantHandler:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_variant_by_id(self, variant_id):
        query = "SELECT variant_info AS info FROM variants WHERE variant_id = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        if result:
            variant_info = result['info']
            return variant_info
        else:
            return None

    def get_variant_by_info(self, variant_info):  #need to be fixed
        variant_info_str = json.dumps(variant_info) 
        query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_info_str,))
        results = db_cursor.fetchall()

        if results:
            if len(results) == 1:
                variant_id = results[0]['variant_id']
                return variant_id
            elif len(results) > 1:
                for result in results:
                    variant_id = result['variant_id']
                    query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                    db_cursor.execute(query, (variant_id,))
                    fetched_variant_info = db_cursor.fetchone()
                    if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                        return variant_id

        return None

    def add_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info) 

        check_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(check_query, (variant_info_str,))
        result = db_cursor.fetchall()

        if result:
            for row in result:
                variant_id = row['variant_id']
                collision_query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                db_cursor.execute(collision_query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                    return variant_id, "already exists"

        db_cursor.execute(insert_query, (variant_info_str, variant_info_str))
        self.db_connection.commit()
        variant_id = db_cursor.lastrowid
        return variant_id, "added"