from flask import Flask
from Model.model import VariantHandler
from View.view import VariantAPI
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

variant_handler = VariantHandler(db_connection, redis_client)
variant_handler.create_table()
data = Populate(db_connection)
data.load_data()
variant_api = VariantAPI(variant_handler, redis_client)
route_handler = RouteHandler(variant_api)

@app.route('/')
def home_page():
    return route_handler.home_page()

@app.route('/variant/id', methods=['GET'])
def get_variant_info():
    return route_handler.get_variant_info()

@app.route('/variant/info', methods=['GET'])
def get_variant_id():
    return route_handler.get_variant_id()

@app.route('/variant/add', methods=['POST'])
def add_variant():
    return route_handler.add_variant()

if __name__ == '__main__':
    app.run(debug=True)