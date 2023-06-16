from flask import Flask, render_template, jsonify

class VariantAPI:
    def __init__(self, variant_handler, redis_client):
        self.variant_handler = variant_handler
        self.redis_client = redis_client

    def get_info(self, variant_id):
        variant_dto = self.variant_handler.get_variant_by_id(variant_id)        
        return render_template('variant.html', variant_results = variant_dto)
    

    def get_id(self, variant_info):
        variant_dto = self.variant_handler.get_variant_by_info(variant_info)        
        return render_template('variant.html', variant_results = variant_dto)


    def add_variant(self, variant_info):
        variant_dto= self.variant_handler.add_variant(variant_info)
        return render_template('variant.html', variant_results = variant_dto)