from flask import render_template, jsonify, request
import json
from View.view import VariantAPI

class MultipleRouteHandler:
    def __init__(self, db_connection, redis_client):
        self.variant_api = VariantAPI(db_connection, redis_client)

    def home_page(self):
        return render_template('index.html')

    def get_variant_info(self):  #get the variant info from the database
        variant_ids = request.args.getlist('variant_id')
        if len(variant_ids)==1 and variant_ids[0]=="":
            return jsonify({'error': 'Empty input is not allowed'})
        try:
            variant_ids = [int(variant_id) for variant_id in variant_ids]  #convert the variant ids to int
        except:
            return jsonify({'error': 'Invalid input format' })  
        return self.variant_api.get_info(variant_ids)


    def get_variant_id(self): #get the variant id from the database
        variant_infos = request.args.getlist('variant_info')
        if len(variant_infos)==1 and variant_infos[0]=="":
            return jsonify({'error': 'Empty input is not allowed'})
        try:
            variant_infos = [json.dumps(json.loads(variant_info))  for variant_info in variant_infos] #convert the variant infos to json    
        except:
            return jsonify({'error': 'Invalid input format'})
        
        return self.variant_api.get_id(variant_infos)

    def add_variant(self): #add the variant to the database
        variant_infos = request.form.getlist('add_entry')
        if len(variant_infos)==1 and variant_infos[0]=="":
            return jsonify({'error': 'Empty input is not allowed'})
        try:
            variant_infos = [json.dumps(json.loads(variant_info)) for variant_info in variant_infos]
        except:
            return jsonify({'error': 'Invalid input format'})
        return self.variant_api.add_variant(variant_infos)

