from flask import Blueprint, request, jsonify
import pandas as pd 
import numpy as np
from model import update_model, predict_rating
import csv

csv_file_path = 'Data/zurich.csv'
df = pd.read_csv(csv_file_path)
#X_list = []
#Y_list = []

all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/', methods=['GET'])
def start_page():
    text = df.to_string()
    return text

@all_routes.route('/model-train', methods=['PUT'])
def train_model():

    #**************** Solution 2 *****************
    #target variable
    #y =  [request.json['rating']]
    #Y_list.append(y)
    #Y = np.array(Y_list)

    #feature values
    #id = 73282 #request.json['id']
    #row = df.loc[df['id'] == id]
    #row = row[['latitude', 'longitude', 'price']] 
    #row = [row['latitude'], row['longitude'], row['price']]
    #row = np.array(row)
    #X_list.append(row[0])
    #X_array = np.array(X_list)

    #train model
    #update_model(X_array,Y)


    #**************** Solution 1 *****************
    #target variable
    y =  np.array([request.json['rating']])

    #feature values
    id = 73282 #request.json['id']
    row = df.loc[df['id'] == id]
    row = row[['latitude', 'longitude', 'price']] 
    x = row.to_numpy()

    #train model
    update_model(x,y)
    
    #write rating to csv file
    row_id = df.index[df['id'] == id][0]
    df.at[row_id, 'rating'] = request.json['rating']
    df.to_csv(csv_file_path)

    return jsonify()

@all_routes.route('/model-predict', methods=['PUT'])
def model_predict():
   
    #loop all apartments and add predicted rating 
    for index, row in df.iterrows():
        row = row[['latitude', 'longitude', 'price']]
        x = row.to_numpy().reshape(1,-1)
        df.at[index, 'rating'] = predict_rating(x)[0]
    df.to_csv(csv_file_path)

    csv_encoding = 'utf-8'
    data = []
    with open(csv_file_path, 'r', encoding=csv_encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            data.append(row)
    
    return jsonify(data)
