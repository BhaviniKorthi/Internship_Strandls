from flask import Flask, render_template, request, jsonify

class VariantAPI:
    def __init__(self, variant_handler, redis_client):
        self.variant_handler = variant_handler
        self.redis_client = redis_client

    def get_variant(self, variant_id):
        variant_info = self.variant_handler.get_variant_by_id(variant_id)
        if not variant_info:
            return jsonify({'error': 'Variant ID not found'})
        
        return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message="Variant ID found")



    def find_variant(self, variant_info):
        variant_id = self.variant_handler.get_variant_by_info(variant_info)
        if not variant_id:
            return jsonify({'error': 'Variant info not found'})
        
        return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message="Variant info found")


    def add_variant(self, variant_info):
        variant_id, msg = self.variant_handler.add_variant(variant_info)
        return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message=msg)
