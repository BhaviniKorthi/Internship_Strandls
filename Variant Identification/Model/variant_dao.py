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
                fetched_variant_info = result[self.COLUMN_VARIANT_INFO]
                if fetched_variant_info == variant_info:
                    return result[self.COLUMN_VARIANT_ID]
        return None

    def variant_info_by_id(self, variant_id):
        query = f"SELECT {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_ID} = %s"
        result = self.db_connect(query, (variant_id,), ResultType.FETCHALL)
        if result:
            variant_info = result[0][self.COLUMN_VARIANT_INFO]
            return VariantDTO(variant_id, variant_info, "Variant info found")
        else:
            return VariantDTO(variant_id, None, "Variant info not found")

    def variant_id_by_info(self, variant_info):
        query = f"SELECT {self.COLUMN_VARIANT_ID}, {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} = MD5(%s)"
        results = self.db_connect(query, (variant_info, ), ResultType.FETCHALL)
        variant_id = self.collision_handler(results, variant_info)
        if variant_id:
            return VariantDTO(variant_id, variant_info, "Variant ID found")
        return VariantDTO(None, variant_info, "Variant ID not found")

    def insert_variant(self, variant_info):
        query = f"SELECT {self.COLUMN_VARIANT_ID}, {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} = MD5(%s)"
        results = self.db_connect(query, (variant_info, ), ResultType.FETCHALL)
        variant_id = self.collision_handler(results, variant_info)
        if variant_id:
            return VariantDTO(variant_id, variant_info ,"already exists")
        insert_query = f"INSERT INTO {self.TABLE_NAME} ({self.COLUMN_VARIANT_INFO}, {self.COLUMN_VARIANT_HASH}) VALUES (%s, MD5(%s))"
        variant_id = self.db_connect(insert_query, (variant_info, variant_info), ResultType.LASTROWID)
        return VariantDTO(variant_id, variant_info, "added")