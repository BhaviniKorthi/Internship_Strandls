from flask import Flask, render_template, request, jsonify

class VariantAPI:
    def __init__(self, variant_handler, redis_client):
        self.variant_handler = variant_handler
        self.redis_client = redis_client

    def get_variant(self, variant_id):
        # # Check if the variant exists in the cache
        # variant_info = self.redis_client.get(f'variant:{variant_id}')
        # if variant_info:
        #     return render_template('variant.html', variant_id=variant_id, variant_info=variant_info.decode(),
        #                            Message="Variant ID found")

        # If not in cache, retrieve the variant from the database
        variant_info = self.variant_handler.get_variant_by_id(variant_id)
        if variant_info:
            # Cache the variant for future requests
            # self.redis_client.set(f'variant:{variant_id}', variant_info)
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message="Variant ID found")
        else:
            return jsonify({'error': 'Variant ID not found'})

    def find_variant(self, variant_info):
        variant_id = self.variant_handler.get_variant_by_info(variant_info)
        if variant_id:
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message="Variant info found")
        else:
            return jsonify({'error': 'Variant info not found'})

    def add_variant(self, variant_info):
        if variant_info:
            variant_id, msg = self.variant_handler.add_variant(variant_info)
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info,
                                   Message=msg)
        else:
            return render_template('variant.html', Message="Error: Input cannot be empty")
