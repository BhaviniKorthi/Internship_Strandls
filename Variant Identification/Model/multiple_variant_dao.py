import enum
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
        return result


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

        
    def variant_info_by_ids(self, variant_ids):
        placeholders = ', '.join(['%s'] * len(variant_ids))
        query = f"SELECT {self.COLUMN_VARIANT_ID} as id, {self.COLUMN_VARIANT_INFO} as info FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_ID} IN ({placeholders})"
        result = self.db_connect(query, variant_ids, ResultType.FETCHALL)
        variant_dtos = []
        variant_id_map = {row["id"]: row["info"] for row in result}
        for id in variant_ids:
            if id not in variant_id_map:
                variant_dtos.append(VariantDTO(id, None, "Variant info not found"))
            else:
                variant_dtos.append(VariantDTO(id, variant_id_map[id], "Variant info found"))    
        return variant_dtos



    def variant_id_by_infos(self, variant_infos):
        placeholders = ', '.join(['MD5(%s)'] * len(variant_infos))
        query = f"SELECT {self.COLUMN_VARIANT_ID}, {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} IN ({placeholders})"
        results = self.db_connect(query, variant_infos, ResultType.FETCHALL)
        variant_info_map = {result[self.COLUMN_VARIANT_INFO]: result[self.COLUMN_VARIANT_ID] for result in results}
        variant_dtos =[]
        for variant_info in variant_infos:
            if variant_info not in variant_info_map:
                variant_dtos.append(VariantDTO(None, variant_info, "Variant ID not found"))
            else:
                variant_dtos.append(VariantDTO(variant_info_map[variant_info], variant_info, "Variant ID found"))
        
        return variant_dtos


    def insert_variants(self, variant_infos):
        placeholders = ', '.join(['MD5(%s)'] * len(variant_infos))
        query = f"SELECT {self.COLUMN_VARIANT_ID}, {self.COLUMN_VARIANT_INFO} FROM {self.TABLE_NAME} WHERE {self.COLUMN_VARIANT_HASH} IN ({placeholders})"
        results = self.db_connect(query, variant_infos, ResultType.FETCHALL)
        variant_info_map = {result[self.COLUMN_VARIANT_INFO]: result[self.COLUMN_VARIANT_ID] for result in results}
      
        variant_dto_list = []
        for variant_info in variant_infos:
            if variant_info in variant_info_map:
                variant_dto_list.append(VariantDTO(variant_info_map[variant_info], variant_info, "already exists"))
            else:
                insert_query = f"INSERT INTO {self.TABLE_NAME} ({self.COLUMN_VARIANT_INFO}, {self.COLUMN_VARIANT_HASH}) VALUES (%s, MD5(%s))"
                inserted_variant_id = self.db_connect(insert_query, (variant_info, variant_info), ResultType.LASTROWID)
                variant_dto_list.append(VariantDTO(inserted_variant_id, variant_info, "added"))
        return variant_dto_list

        
