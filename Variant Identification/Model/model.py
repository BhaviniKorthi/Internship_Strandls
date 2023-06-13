from Model.variant_dao import VariantDAO

class VariantHandler:
    def __init__(self, db_connection, redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client
        self.variant_dao = VariantDAO(db_connection)

    def create_table(self):
        self.variant_dao.create_table()

    def get_variant_by_id(self, variant_id):
        variant_info = self.redis_client.get(f'variant:{variant_id}')
        if variant_info:
            try:
                return variant_info.decode('utf-8')
            except:
                return variant_info

        variant_dto = self.variant_dao.select_variant_by_id(variant_id)

        if variant_dto:
            variant_info = variant_dto.variant_info
            self.redis_client.set(f'variant:{variant_id}', variant_info)
            try:
                return variant_info.decode('utf-8')
            except:
                return variant_info
        else:
            return None

    def get_variant_by_info(self, variant_info):
        variant_dto = self.variant_dao.select_variant_by_info(variant_info)

        if variant_dto:
            variant_id = variant_dto.variant_id
            return variant_id

        return None

    def add_variant(self, variant_info):
        variant_dto = self.variant_dao.insert_variant(variant_info)

        if variant_dto.variant_info == "already exists":
            return variant_dto.variant_id, "already exists"

        return variant_dto.variant_id, "added"
