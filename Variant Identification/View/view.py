from flask import render_template
from Model.model import VariantHandler

class VariantAPI:
    def __init__(self, db_connection,  redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client
        self.variant_handler = VariantHandler(db_connection, redis_client)

    def get_info(self, variant_id):
        variant_dto = self.variant_handler.get_variant_by_id(variant_id) 
        return render_template('variant.html', variant_id = variant_dto.variant_id, variant_info = variant_dto.variant_info, Message = variant_dto.Message)
    

    def get_id(self, variant_info):
        variant_dto = self.variant_handler.get_variant_by_info(variant_info)        
        return render_template('variant.html', variant_id = variant_dto.variant_id, variant_info = variant_dto.variant_info, Message = variant_dto.Message)
    

    def add_variant(self, variant_info):
        variant_dto= self.variant_handler.add_variant(variant_info)
        return render_template('variant.html', variant_id = variant_dto.variant_id, variant_info = variant_dto.variant_info, Message = variant_dto.Message)