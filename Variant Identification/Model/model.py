import json
import hashlib

class VariantQueries:
    @staticmethod
    def create_table():
        return """
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INT PRIMARY KEY AUTO_INCREMENT,
                variant_info JSON,
                variant_hash VARCHAR(32),
                INDEX idx_variant_hash (variant_hash)
            )
        """

    @staticmethod
    def select_variant_by_id():
        return "SELECT variant_info AS info FROM variants WHERE variant_id = %s"

    @staticmethod
    def select_variant_by_hash():
        return "SELECT variant_id FROM variants WHERE variant_hash = %s"

    @staticmethod
    def select_variant_info_by_id():
        return "SELECT variant_info FROM variants WHERE variant_id = %s"

    @staticmethod
    def insert_variant():
        return "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, %s)"


class VariantHandler:
    def __init__(self, db_connection, redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client

    def create_table(self):
        create_table_query = VariantQueries.create_table()
        db_cursor = self.db_connection.cursor()
        db_cursor.execute(create_table_query)
        self.db_connection.commit()
        db_cursor.close()

    def get_variant_by_id(self, variant_id):
        variant_info = self.redis_client.get(f'variant:{variant_id}')
        if variant_info:
            try:
                return variant_info.decode('utf-8')
            except:
                return variant_info

        query = VariantQueries.select_variant_by_id()
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        db_cursor.close()

        if result:
            variant_info = result['info']
            self.redis_client.set(f'variant:{variant_id}', variant_info)
            try:
                return variant_info.decode('utf-8')
            except:
                return variant_info
        else:
            return None

    def get_variant_by_info(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        variant_id = self.redis_client.get(f'variant_hash:{variant_hash}')
        if variant_id:
            return variant_id

        query = VariantQueries.select_variant_by_hash()
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_hash,))
        results = db_cursor.fetchall()
        db_cursor.close()

        if results:
            if len(results) == 1:
                variant_id = results[0]['variant_id']
                self.redis_client.set(f'variant_hash:{variant_hash}', variant_id)
                try:
                    return variant_id.decode('utf-8')
                except:
                    return variant_id
            elif len(results) > 1:
                for result in results:
                    variant_id = result['variant_id']
                    query = VariantQueries.select_variant_info_by_id()
                    db_cursor = self.db_connection.cursor(dictionary=True)
                    db_cursor.execute(query, (variant_id,))
                    fetched_variant_info = db_cursor.fetchone()
                    db_cursor.close()

                    if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                        self.redis_client.set(f'variant_hash:{variant_hash}', variant_id)
                        try:
                            return variant_id.decode('utf-8')
                        except:
                            return variant_id

        return None

    def add_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        query = VariantQueries.select_variant_by_hash()
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_hash,))
        result = db_cursor.fetchall()
        db_cursor.close()

        if result:
            for row in result:
                variant_id = row['variant_id']
                query = VariantQueries.select_variant_info_by_id()
                db_cursor = self.db_connection.cursor(dictionary=True)
                db_cursor.execute(query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                db_cursor.close()

                if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                    return variant_id, "already exists"

        insert_query = VariantQueries.insert_variant()
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(insert_query, (variant_info_str, variant_hash))
        self.db_connection.commit()
        variant_id = db_cursor.lastrowid
        db_cursor.close()
        return variant_id, "added"
