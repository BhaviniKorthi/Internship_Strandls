from flask import render_template
from Model.model import VariantHandler
from Model.multiple_model import MultipleVariantHandler

class VariantAPI:
    def __init__(self, db_connection,  redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client
        self.variant_handler = VariantHandler(db_connection, redis_client)
        self.multiple_variant_handler = MultipleVariantHandler(db_connection, redis_client)

    def get_info(self, variant_id):
        if type(variant_id) == list:
            variant_dto = self.multiple_variant_handler.get_variant_by_id(variant_id)
        else:
            variant_dto = self.variant_handler.get_variant_by_id(variant_id)        
        return render_template('variant.html', variant_results = variant_dto)
    

    def get_id(self, variant_info):
        if type(variant_info) == list:
            variant_dto = self.multiple_variant_handler.get_variant_by_info(variant_info)
        else:
            variant_dto = self.variant_handler.get_variant_by_info(variant_info)        
        return render_template('variant.html', variant_results = variant_dto)


    def add_variant(self, variant_info):
        if type(variant_info) == list:
            variant_dto = self.multiple_variant_handler.add_variant(variant_info)
        else:
            variant_dto= self.variant_handler.add_variant(variant_info)
        return render_template('variant.html', variant_results = variant_dto)