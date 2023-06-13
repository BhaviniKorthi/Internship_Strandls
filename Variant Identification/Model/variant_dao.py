import json
import hashlib
from Model.variant_dto import VariantDTO

class VariantDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

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

    def select_variant_by_id(self, variant_id):
        query = "SELECT variant_info AS info FROM variants WHERE variant_id = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        db_cursor.close()

        if result:
            variant_info = result['info']
            return VariantDTO(variant_id, variant_info)
        else:
            return None

    def select_variant_by_info(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        query = "SELECT variant_id FROM variants WHERE variant_hash = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_hash,))
        results = db_cursor.fetchall()
        db_cursor.close()

        if results:
            if len(results) == 1:
                variant_id = results[0]['variant_id']
                return VariantDTO(variant_id, variant_info)
            elif len(results) > 1:
                for result in results:
                    variant_id = result['variant_id']
                    query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                    db_cursor = self.db_connection.cursor(dictionary=True)
                    db_cursor.execute(query, (variant_id,))
                    fetched_variant_info = db_cursor.fetchone()
                    db_cursor.close()

                    if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                        return VariantDTO(variant_id, variant_info)

        return None

    def insert_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        query = "SELECT variant_id FROM variants WHERE variant_hash = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_hash,))
        result = db_cursor.fetchall()
        db_cursor.close()

        if result:
            for row in result:
                variant_id = row['variant_id']
                query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                db_cursor = self.db_connection.cursor(dictionary=True)
                db_cursor.execute(query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                db_cursor.close()

                if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                    return VariantDTO(variant_id, "already exists")

        insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, %s)"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(insert_query, (variant_info_str, variant_hash))
        self.db_connection.commit()
        variant_id = db_cursor.lastrowid
        db_cursor.close()
        return VariantDTO(variant_id, "added")
