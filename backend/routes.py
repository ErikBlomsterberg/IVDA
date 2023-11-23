from flask import Blueprint, request, jsonify
import pandas as pd 
import numpy as np
from model import update_model, predict_rating
import csv

csv_file_path = 'Data/zurich.csv'
df = pd.read_csv(csv_file_path)


all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/', methods=['GET'])
def start_page():
    text = df.to_string()
    return text

@all_routes.route('/model-train', methods=['PUT'])
def train_model():
    x = np.array([10,5,20]).reshape(1,-1)
    id = request.json['id']
    #create model input from csv file 
    #write rating in csv file 
    y = request.json['rating']
    y = np.array([y])
    update_model(x,y)
    return jsonify()

@all_routes.route('/model-predict', methods=['PUT'])
def model_predict():
    x = np.array([10,5,20]).reshape(1,-1)
    #loop all apartments and add predicted rating 
    prediction = predict_rating(x)[0]

    csv_encoding = 'utf-8'
    data = []
    with open(csv_file_path, 'r', encoding=csv_encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            data.append(row)
    
    return jsonify(data)
