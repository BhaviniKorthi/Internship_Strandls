import json
import hashlib

class VariantHandler:
    def __init__(self, db_connection, redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INT PRIMARY KEY AUTO_INCREMENT,
                variant_info JSON,
                variant_hash VARCHAR(32),
                INDEX idx_variant_hash (variant_hash)
            )
        """
        db_cursor = self.db_connection.cursor()
        db_cursor.execute(create_table_query)
        self.db_connection.commit()
        db_cursor.close()

    def load_data(self):
        query = "SELECT COUNT(*) AS count FROM variants"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query)
        result = db_cursor.fetchone()["count"]
        # db_cursor.close()
        if result == 0:
            count = 100
            insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, %s)"
            check_query = "SELECT variant_id FROM variants WHERE variant_hash = %s"
            db_cursor = self.db_connection.cursor(dictionary=True)
            
            for i in range(1, count + 1):
                variant_data = {
                    'name': f'Variant {i}',
                    'description': f'Description for Variant {i}',
                }
                variant_info = json.dumps(variant_data)
                variant_hash = hashlib.md5(variant_info.encode()).hexdigest()

                db_cursor.execute(check_query, (variant_hash,))
                count = db_cursor.fetchall()

                if len(count) > 0:
                    continue
                else:
                    db_cursor.execute(insert_query, (variant_info, variant_hash))
                    self.db_connection.commit()

        db_cursor.close()

    def get_variant_by_id(self, variant_id):
        variant_info = self.redis_client.get(f'variant:{variant_id}')
        if variant_info:
            return variant_info
        query = "SELECT variant_info AS info FROM variants WHERE variant_id = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()

        if result:
            variant_info = result['info']
            self.redis_client.set(f'variant:{variant_id}', variant_info)
            return variant_info
        else:
            return None

    def get_variant_by_info(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        variant_id = self.redis_client.get(f'variant_hash:{variant_hash}')
        if variant_id:
            return variant_id

        query = "SELECT variant_id FROM variants WHERE variant_hash = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_hash,))
        results = db_cursor.fetchall()

        if results:
            if len(results) == 1:
                variant_id = results[0]['variant_id']
                self.redis_client.set(f'variant_hash:{variant_hash}', variant_id)
                return variant_id
            elif len(results) > 1:
                for result in results:
                    variant_id = result['variant_id']
                    query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                    db_cursor.execute(query, (variant_id,))
                    fetched_variant_info = db_cursor.fetchone()
                    if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                        self.redis_client.set(f'variant_hash:{variant_hash}', variant_id)
                        return variant_id

        return None

    def add_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        check_query = "SELECT variant_id FROM variants WHERE variant_hash = %s"
        insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, %s)"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(check_query, (variant_hash,))
        result = db_cursor.fetchall()

        if result:
            for row in result:
                variant_id = row['variant_id']
                collision_query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                db_cursor.execute(collision_query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                    return variant_id, "already exists"

        db_cursor.execute(insert_query, (variant_info_str, variant_hash))
        self.db_connection.commit()
        variant_id = db_cursor.lastrowid
        return variant_id, "added"
