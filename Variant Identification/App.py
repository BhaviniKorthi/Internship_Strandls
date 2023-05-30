from flask import Flask, render_template, request, jsonify
import mysql.connector
import pymysql

app = Flask(__name__)


config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'cursorclass': pymysql.cursors.DictCursor
}

db_connection = pymysql.connect(**config)

# Home page
@app.route('/')
def home_page():
    return render_template('index.html')

# Variant page
@app.route('/variant', methods=['GET'])
def get_variant():
    if 'variant_id' in request.args:
        variant_id = request.args.get('variant_id')
        try:
            variant_id = int(variant_id)
        except ValueError:
            return jsonify({'error': 'Invalid variant ID'})

        query = "SELECT CAST(AES_DECRYPT(variant_hash, 'encryption_key') AS CHAR) AS info FROM variant_hashes WHERE variant_id = %s"
        db_cursor = db_connection.cursor()
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        if result:
            variant_info = result['info']
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info)
        else:
            return jsonify({'error': 'Variant ID not found'})
    elif 'variant_info' in request.args:
        variant_info = request.args.get('variant_info')

        query = "SELECT variant_id FROM variants WHERE variant_info = %s"
        db_cursor = db_connection.cursor()
        db_cursor.execute(query, (variant_info,))
        result = db_cursor.fetchone()
        if result:
            variant_id = result['variant_id']
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info)
        else:
            return jsonify({'error': 'Variant info not found'})
    else:
        return jsonify({'error': 'No input provided'})

if __name__ == '__main__':
    app.run(debug=True)
