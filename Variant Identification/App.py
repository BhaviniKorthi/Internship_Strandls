from flask import Flask, render_template
from Model.model import VariantHandler
from Model.multiple_model import MultipleVariantHandler

from View.view import VariantAPI
from Controller.multiple_controller import MultipleRouteHandler
from Controller.controller import RouteHandler
from Data_populate import Populate
import mysql.connector
import redis

app = Flask(__name__)
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Srikar@420',
    'database': 'variant_db',
    'auth_plugin': 'mysql_native_password'
}

db_connection = mysql.connector.connect(**config)
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_client = redis.Redis(connection_pool=redis_pool)

data = Populate(db_connection)
data.load_data()

multiple_route_handler = MultipleRouteHandler(db_connection, redis_client)
route_handler = RouteHandler(db_connection, redis_client)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/single_variant')
def single_variant():
    return render_template('index.html')

@app.route('/multiple_variants')
def multiple_variants():
    return render_template('multiple_index.html')

@app.route('/multiple_variants/id', methods=['GET'])
def get_variant_info_multiple():
    return multiple_route_handler.get_variant_info()

@app.route('/multiple_variants/info', methods=['GET'])
def get_variant_id_multiple():
    return multiple_route_handler.get_variant_id()

@app.route('/multiple_variants/info', methods=['POST'])
def add_variant_multiple():
    return multiple_route_handler.add_variant()

@app.route('/single_variant/id', methods=['GET'])
def get_variant_info_single():
    return route_handler.get_variant_info()

@app.route('/single_variant/info', methods=['GET'])
def get_variant_id_single():
    return route_handler.get_variant_id()

@app.route('/single_variant/info', methods=['POST'])
def add_variant_single():
    return route_handler.add_variant()

if __name__ == '__main__':
    app.run(debug=True)
