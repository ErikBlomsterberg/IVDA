from flask import Blueprint
import pandas as pd 

df = pd.read_csv('Data/zurich.csv')


all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/', methods=['GET'])
def start_page():
    text = df.to_string()
    return text


