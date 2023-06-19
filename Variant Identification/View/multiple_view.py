from flask import render_template
from Model.multiple_model import MultipleVariantHandler

class VariantAPI:
    def __init__(self, db_connection,  redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client
        self.multiple_variant_handler = MultipleVariantHandler(db_connection, redis_client)

    def get_info(self, variant_id):
        variant_dto = self.multiple_variant_handler.get_variant_by_id(variant_id)
        # print([variant_dto.variant_id for variant_dto in variant_dto])
        print(render_template('multiple_variant.html', variant_results=variant_dto, page=True))
        return render_template('multiple_variant.html', variant_results=variant_dto, page=True)
    

    

    def get_id(self, variant_info, start, end):
        variant_dto = self.multiple_variant_handler.get_variant_by_info(variant_info, start, end)       
        return render_template('multiple_variant.html', variant_results = variant_dto)


    def add_variant(self, variant_info):
        variant_dto = self.multiple_variant_handler.add_variant(variant_info)
        return render_template('multiple_variant.html', variant_results = variant_dto)