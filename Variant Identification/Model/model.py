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

    def get_variant_by_id(self, variant_ids):
        variant_dtos = []
        variant_ids_to_query = []
        for variant_id in variant_ids:
            variant_info = self.redis_client.get(f'variant:{variant_id}')
            if variant_info:
                variant_dtos.append(
                    VariantDTO(variant_id, variant_info.decode('utf-8'), "Variant ID found")
                )
            else:
                variant_ids_to_query.append(variant_id)

        if variant_ids_to_query:
            variant_infos_from_sql = self.variant_dao.variant_info_by_ids(variant_ids_to_query)
            for variant_dto in variant_infos_from_sql:
                variant_dtos.append(variant_dto)
                
                self.redis_client.set(f'variant:{variant_dto.variant_id}', variant_dto.variant_info)
        return variant_dtos



    def get_variant_by_info(self, variant_infos):
        variant_dtos = []
        variant_infos_to_query = []
        for variant_info in variant_infos:
            variant_hash = hashlib.md5(variant_info.encode()).hexdigest()
            variant_id = self.redis_client.get(f'variant:{variant_hash}')
            if variant_id:
                variant_dtos.append(
                    VariantDTO(variant_id.decode('utf-8'), variant_info, "Variant info found")
                )
            else:
                variant_infos_to_query.append(variant_info)

        if variant_infos_to_query:
            variant_infos_from_sql = self.variant_dao.variant_id_by_infos(variant_infos_to_query)
            for variant_dto in variant_infos_from_sql:
                variant_hash = hashlib.md5(variant_dto.variant_info.encode()).hexdigest()
                self.redis_client.set(f'variant:{variant_hash}', variant_dto.variant_id)
                variant_dtos.append(variant_dto)
      
        return variant_dtos





    def add_variant(self, variant_infos):
        variant_dtos = []
        if variant_infos:
            variant_infos_from_sql = self.variant_dao.insert_variants(variant_infos)
            for variant_dto in variant_infos_from_sql:
                variant_dtos.append(variant_dto)
        return variant_dtos
