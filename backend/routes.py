from flask import Blueprint, request, jsonify
import pandas as pd 
import numpy as np
from model import update_model, predict_rating
df = pd.read_csv('Data/zurich.csv')


all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/', methods=['GET'])
def start_page():
    text = df.to_string()
    return text

@all_routes.route('/model-train', methods=['PUT'])
def train_model():
    x = np.array([10,5,20]).reshape(1,-1)
    y = request.json['rating']
    y = np.array([y])
    update_model(x,y)
    return jsonify()

@all_routes.route('/model-predict', methods=['PUT'])
def model_predict():
    x = np.array([10,5,20]).reshape(1,-1)
    prediction = predict_rating(x)[0]
    res = jsonify({'prediction':prediction})
    return res