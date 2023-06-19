from Model.variant_dao import VariantDAO
from Model.variant_dto import VariantDTO
import hashlib
import json


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
            variant_dto = VariantDTO(variant_id, variant_info.decode('utf-8'), "Variant ID found")
            return variant_dto
        variant_dto = self.variant_dao.variant_info_by_id(variant_id)
        if variant_dto.variant_info:
            self.redis_client.set(f'variant:{variant_id}', variant_dto.variant_info)
        return variant_dto

    def get_variant_by_info(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_hash = hashlib.md5(variant_info_str.encode()).hexdigest()

        variant_id = self.redis_client.get(f'variant:{variant_hash}')
        if variant_id:
            variant_dto = VariantDTO(variant_id.decode('utf-8'), variant_info, "Variant info found")
            return variant_dto
        variant_dto = self.variant_dao.variant_id_by_info(variant_info_str)
        if variant_dto.variant_id:
            variant_id = variant_dto.variant_id
            self.redis_client.set(f'variant:{variant_hash}', variant_id)
        return variant_dto

    def add_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info)
        variant_dto = self.variant_dao.insert_variant(variant_info_str)
        return variant_dto