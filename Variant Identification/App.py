from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'auth_plugin': 'mysql_native_password'
}

db_connection = mysql.connector.connect(**config)

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

        query = "SELECT variant_info AS info FROM variants WHERE variant_id = %s"
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_id,))
        result = db_cursor.fetchone()
        print(result)
        if result:
            variant_info = result['info']
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info, Message="Variant ID found")
        else:
            return jsonify({'error': 'Variant ID not found'})
    elif 'variant_info' in request.args:
        variant_info = request.args.get('variant_info')

        query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_info,))
        result = db_cursor.fetchone()
        if result:
            variant_id = result['variant_id']
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info, Message="Variant info found")
        else:
            return jsonify({'error': 'GET: Variant info not found'})
   
    elif 'add_entry' in request.args:
        variant_info = request.args['add_entry']
        query = "SELECT variant_id FROM variants WHERE variant_hash = MD5(%s)"
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(query, (variant_info,))
        result = db_cursor.fetchone()
        if result:
            variant_id = result['variant_id']
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info, Message="Variant info already exists")
        else:
            insert_query = "INSERT INTO variants (variant_info, variant_hash) VALUES (%s, MD5(%s))"
            db_cursor.execute(insert_query, (variant_info, variant_info))
            db_connection.commit()
            variant_id = db_cursor.lastrowid
            return render_template('variant.html', variant_id=variant_id, variant_info=variant_info, Message="Variant info added successfully")
    else:
        return jsonify({'error': 'Add: No variant_info provided'})


if __name__ == '__main__':
    app.run(debug=True)
