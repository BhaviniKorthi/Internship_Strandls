from flask import Flask, render_template, request, jsonify
import mysql.connector
import json
import hashlib

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'auth_plugin': 'mysql_native_password'
}

db_connection = mysql.connector.connect(**config)


class VariantHandler:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_variant_by_id(self, variant_id):
        query = "SELECT variant_info AS info FROM variants WHERE variant_id = %s"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        if result:
            variant_info = result['info']
            return variant_info
        else:
            return None

    def get_variant_by_info(self, variant_info):
        query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_info,))
        results = db_cursor.fetchall()

        if results:
            if len(results) == 1:
                variant_id = results[0]['variant_id']
                return variant_id
            elif len(results) > 1:
                for result in results:
                    variant_id = result['variant_id']
                    query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                    db_cursor.execute(query, (variant_id,))
                    fetched_variant_info = db_cursor.fetchone()
                    if fetched_variant_info and fetched_variant_info['variant_info'] == variant_info:
                        return variant_id

        return None

    def add_variant(self, variant_info):
        variant_info_str = json.dumps(variant_info)  # Convert variant_info to JSON string

        check_query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute(check_query, (variant_info_str,))
        result = db_cursor.fetchall()

        if result:
            for row in result:
                variant_id = row['variant_id']
                collision_query = "SELECT variant_info FROM variants WHERE variant_id = %s"
                db_cursor.execute(collision_query, (variant_id,))
                fetched_variant_info = db_cursor.fetchone()
                if fetched_variant_info and json.loads(fetched_variant_info['variant_info']) == variant_info:
                    return variant_id, "already exists"

        db_cursor.execute(insert_query, (variant_info_str, variant_info_str))
        self.db_connection.commit()
        variant_id = db_cursor.lastrowid
        return variant_id, "added"


class VariantAPI:
    def __init__(self, variant_handler):
        self.variant_handler = variant_handler

    def get_variant(self, variant_id):
        variant_info = self.variant_handler.get_variant_by_id(variant_id)
        if variant_info:
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


variant_handler = VariantHandler(db_connection)
variant_api = VariantAPI(variant_handler)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/variant', methods=['GET'])
def get_variant():
    if 'variant_id' in request.args:
        variant_id = request.args.get('variant_id')
        try:
            variant_id = int(variant_id)
        except ValueError:
            return jsonify({'error': 'Invalid variant ID'})

        return variant_api.get_variant(variant_id)

    elif 'variant_info' in request.args:
        variant_info = request.args.get('variant_info')
        return variant_api.find_variant(variant_info)

    else:
        return jsonify({'error': 'No variant_info provided'})


@app.route('/variant/add', methods=['POST'])
def add_entry():
    if request.content_type == 'application/json':
        variant_info = request.get_json()
    else:
        variant_info = request.form.get('add_entry')

        try:
            variant_info = json.loads(variant_info)
        except json.JSONDecodeError:
            return render_template('variant.html', Message="Error: Input is not valid JSON")

    if variant_info is not None:
        return variant_api.add_variant(variant_info)
    else:
        return render_template('variant.html', Message="Error: Input cannot be empty")


if __name__ == '__main__':
    app.run(debug=True)
