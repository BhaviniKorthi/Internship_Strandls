from flask import Flask, render_template, jsonify

class VariantAPI:
    def __init__(self, variant_handler, redis_client):
        self.variant_handler = variant_handler
        self.redis_client = redis_client

    def get_variant(self, variant_id):
        variant_dto = self.variant_handler.get_variant_by_id(variant_id)
        if variant_dto is None:
            return jsonify({'error': 'Variant ID not found'})
        
        return render_template('variant.html', variant_id=variant_dto.variant_id, variant_info=variant_dto.variant_info,
                                   Message=variant_dto.Message)



    def find_variant(self, variant_info):
        variant_dto = self.variant_handler.get_variant_by_info(variant_info)
        # if variant_dto is None:
        #     return jsonify({'error': 'Variant info not found'})
        
        return render_template('variant.html', variant_id=variant_dto.variant_id, variant_info=variant_dto.variant_info,
                                   Message=variant_dto.Message)


    def add_variant(self, variant_info):
        variant_dto= self.variant_handler.add_variant(variant_info)
        return render_template('variant.html', variant_id=variant_dto.variant_id, variant_info=variant_dto.variant_info,
                                   Message=variant_dto.Message)