import os
from flask import Flask

from . import pages
from BinaryTree import BinaryTree
from TemperatureDB import TemperatureDB
from HumidityDB import HumidityDB
from AirQualityDB import AirQualityDB

def create_app():
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=templates_path)
    
    # Initialize binary trees
    app.temp_tree = BinaryTree()
    app.humidity_tree = BinaryTree()
    app.air_quality_tree = BinaryTree()
    
    # Load existing data into trees
    temp_db = TemperatureDB()
    app.temp_tree.load_from_list(temp_db.get_all_temperatures())
    temp_db.close()
    
    humidity_db = HumidityDB()
    app.humidity_tree.load_from_list(humidity_db.get_all_humidities())
    humidity_db.close()
    
    air_db = AirQualityDB()
    app.air_quality_tree.load_from_list(air_db.get_all_iaq())
    air_db.close()
    
    app.register_blueprint(pages.bp)
    return app