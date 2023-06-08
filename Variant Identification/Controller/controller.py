from flask import render_template, jsonify, request
import json

class RouteHandler:
    def __init__(self, variant_api):
        self.variant_api = variant_api

    def home_page(self):
        return render_template('index.html')

    def get_variant_info(self):
        if 'variant_id' in request.form:
            variant_id = request.form.get('variant_id')
            try:
                variant_id = int(variant_id)
            except ValueError:
                return jsonify({'error': 'Invalid variant ID'})

            return self.variant_api.get_variant(variant_id)
        else:
            return jsonify({'error': 'No variant_info provided'})

    def get_variant_id(self):
        if request.content_type == 'application/json':
            variant_info = request.get_json()
        else:
            variant_info = request.form.get('variant_info')

            try:
                variant_info = json.loads(variant_info)
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid variant info'})

        if variant_info is not None:
            return self.variant_api.find_variant(variant_info)
        else:
            return render_template('variant.html', Message="Error: Input cannot be empty")

    def add_variant(self):
        if request.content_type == 'application/json':
            variant_info = request.get_json()
        else:
            variant_info = request.form.get('add_entry')

            try:
                variant_info = json.loads(variant_info)
            except json.JSONDecodeError:
                return render_template('variant.html', Message="Error: Input is not valid JSON")

        if variant_info is not None:
            return self.variant_api.add_variant(variant_info)
        else:
            return render_template('variant.html', Message="Error: Input cannot be empty")
