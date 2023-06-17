from flask import render_template, jsonify, request
import json
from View.view import VariantAPI

class RouteHandler:
    def __init__(self, db_connection, redis_client):
        self.db_connection = db_connection
        self.redis_client = redis_client
        self.variant_api = VariantAPI(db_connection, redis_client)

    def home_page(self):
        return render_template('index.html')

    def get_variant_info(self):
        variant_id = request.args.get('variant_id')
        print(variant_id, "single")
        if not variant_id:
            return jsonify({'error': 'Empty input is not allowed'})
        
        try:
            variant_id = int(variant_id)
            return self.variant_api.get_info(variant_id)
        except ValueError:
            return jsonify({'error': 'Invalid input format'})
        


    def get_variant_id(self):
        variant_info = request.args.get('variant_info')
        if not variant_info:
            return jsonify({'error': 'Empty input is not allowed'})
        
        try:
            variant_info = json.loads(variant_info)
            return self.variant_api.get_id(variant_info)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid input format'})




    def add_variant(self):
        variant_info = request.form.get('add_entry')
        if not variant_info:
            return jsonify({'error': 'Empty input is not allowed'})
        
        try:
            variant_info = json.loads(variant_info)
            return self.variant_api.add_variant(variant_info)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid input format'})
     