class Table:

    TABLE_NAME = "variants"
    COLUMN_VARIANT_ID = "variant_id"
    COLUMN_VARIANT_INFO = "variant_info"
    COLUMN_VARIANT_HASH = "variant_hash"

    def __init__(self, db_connection):
        self.db_connection = db_connection

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