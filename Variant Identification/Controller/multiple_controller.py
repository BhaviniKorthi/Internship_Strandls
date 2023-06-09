from flask import render_template, jsonify, request
import json
from View.multiple_view import VariantAPI

class MultipleRouteHandler:
    def __init__(self, db_connection, redis_client):
        self.variant_api = VariantAPI(db_connection, redis_client)

    def home_page(self):
        return render_template('index.html')

    def get_variant_info(self):
        variant_ids = request.args.getlist('variant_id')
        page = request.args.get('page', default=1, type=int)  
        items_per_page = request.args.get('items_per_page', default=10, type=int)  
        start = request.args.get('start', type=int)  
        end = request.args.get('end', type=int)  

        if start and end:
            start = int(start)
            end = int(end)
            variant_ids = list(range(start, end + 1))  # Create a list of variant IDs from start to end
        elif variant_ids:
            try:
                variant_ids = [int(variant_id) for variant_id in variant_ids]  # Convert the variant IDs to int
            except ValueError:
                return jsonify({'error': 'Invalid input format'})
            
        else:
            return jsonify({'error': 'Variant IDs not provided'})
        if page < 1 or items_per_page < 1:
            return jsonify({'error': 'Invalid page number'})

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        if start_index < 0 or end_index < 0:
            return jsonify({'error': 'Invalid pagination parameters'})

        paginated_variant_ids = variant_ids[start_index:end_index]
        return self.variant_api.get_info(paginated_variant_ids)



    def get_variant_id(self): #get the variant id 
        variant_infos = request.args.getlist('variant_info')
        page = request.args.get('page', default=1, type=int)
        items_per_page = request.args.get('items_per_page', default=10, type=int)
                
        if len(variant_infos)==1 and variant_infos[0]=="":
            return jsonify({'error': 'Empty input is not allowed'})
        try:
            variant_infos = [json.dumps(json.loads(variant_info))  for variant_info in variant_infos] #convert the variant infos to json    
        except:
            return jsonify({'error': 'Invalid input format'})
        
        if page < 1 or items_per_page < 1:
            return jsonify({'error': 'Invalid page number'})
        
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        if start_index < 0 or end_index < 0:
            return jsonify({'error': 'Invalid pagination parameters'})
        
        paginated_variant_infos = variant_infos[start_index:end_index]
        return self.variant_api.get_id(paginated_variant_infos)
        



    def add_variant(self): #add the variant to the database
        variant_infos = request.form.getlist('add_entry')
        if len(variant_infos)==1 and variant_infos[0]=="":
            return jsonify({'error': 'Empty input is not allowed'})
        try:
            variant_infos = [json.dumps(json.loads(variant_info)) for variant_info in variant_infos]
        except:
            return jsonify({'error': 'Invalid input format'})
        return self.variant_api.add_variant(variant_infos)

