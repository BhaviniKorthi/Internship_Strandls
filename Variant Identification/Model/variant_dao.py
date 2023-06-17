import enum
import json
from Model.variant_dto import VariantDTO

class ResultType(enum.Enum):
    FETCHALL = "fetchall"
    LASTROWID = "lastrowid"

class VariantDAO:
    TABLE_NAME = "variants"
    COLUMN_VARIANT_ID = "variant_id"
    COLUMN_VARIANT_INFO = "variant_info"
    COLUMN_VARIANT_HASH = "variant_hash"

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def db_connect(self, query, data, result_type):
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, data)
        if result_type == ResultType.FETCHALL:
            result = db_cursor.fetchall()
        elif result_type == ResultType.LASTROWID:
            result = db_cursor.lastrowid
        db_cursor.close()
        return result
    
    def collision_handler(self, results, variant_info):
        if results:
            for result in results:
                variant_id = result[self.COLUMN_VARIANT_ID]
                query = f"SELECT {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_ID} = %s"
                db_cursor = self.db_connection.cursor(dictionary=True)
                db_cursor.execute(query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                db_cursor.close()
                if fetched_variant_info and fetched_variant_info[self.COLUMN_VARIANT_INFO] == variant_info:
                    return variant_id
        return None

    def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                {self.COLUMN_VARIANT_ID} INT PRIMARY KEY AUTO_INCREMENT,
                {self.COLUMN_VARIANT_INFO} JSON,
                {self.COLUMN_VARIANT_HASH} VARCHAR(32),
                INDEX idx_variant_hash ({self.COLUMN_VARIANT_HASH})
            )
        """
        db_cursor = self.db_connection.cursor()
        db_cursor.execute(create_table_query)
        self.db_connection.commit()
        db_cursor.close()

    def variant_info_by_id(self, variant_id):
        query = f"SELECT {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_ID} = %s"
        result = self.db_connect(query, (variant_id,), ResultType.FETCHALL)
        if result:
            variant_info = result[0][self.COLUMN_VARIANT_INFO]
            return VariantDTO(variant_id, variant_info, "Variant info found")
        else:
            return None

    def variant_id_by_info(self, variant_info):
        query = f"SELECT {self.COLUMN_VARIANT_ID} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} = MD5(%s)"
        results = self.db_connect(query, (variant_info, ), ResultType.FETCHALL)
        variant_id = self.collision_handler(results, variant_info)
        if variant_id:
            return VariantDTO(variant_id, variant_info, "Variant ID found")
        return None

    def insert_variant(self, variant_info):
        query = f"SELECT {self.COLUMN_VARIANT_ID} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} = MD5(%s)"
        results = self.db_connect(query, (variant_info, ), ResultType.FETCHALL)
        variant_id = self.collision_handler(results, variant_info)
        if variant_id:
            return VariantDTO(variant_id, variant_info ,"already exists")
        insert_query = f"INSERT INTO {self.TABLE_NAME} ({self.COLUMN_VARIANT_INFO}, {self.COLUMN_VARIANT_HASH}) VALUES (%s, MD5(%s))"
        variant_id = self.db_connect(insert_query, (variant_info, variant_info), ResultType.LASTROWID)
        return VariantDTO(variant_id, variant_info, "added")