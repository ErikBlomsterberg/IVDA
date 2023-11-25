import os

from flask import Blueprint, request, jsonify
import pandas as pd 
import numpy as np
from model import update_model, predict_rating
import csv

training_path = 'Data/data.csv'
df = pd.read_csv(training_path, index_col='id')

modified_ratings = {}



all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/apartments', methods=['GET'])
def start_page():
    csv_encoding = 'utf-8'
    data = []
    csv_file_path = 'Data/preprocessed.csv'
    # TODO : decide a better strategy
    with open(csv_file_path, 'r', encoding=csv_encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for i, row in enumerate(csv_reader):
            data.append(row)
            if(i == 9):
                break
    return jsonify(data)

@all_routes.route('/model-train', methods=['PUT'])
def train_model():
    global modified_ratings

    #**************** Solution 1 *****************
    #target variable
    print(request.json)
    modified_ratings.update({int(request.json['id']): int(request.json['rating'])})

    # modified_ratings.update(request.json)
    # y =  np.array([request.json['rating']])
    # json_data = request.get_json()
    # ids = json_data['id']
    # rating = request.json['rating']
    # print(y)
    # print(request.json['rating'])
    # print(request.json['id'])

    #feature values
    # id = request.json['id']
    # row = df.loc[df['id'] == int(ids)]
    # print('type', type(ids))
    # print('type', type(df['id']))
    # row = row[['latitude', 'longitude', 'price']] 
    # x = row.to_numpy()

    #train model
    # update_model(x,y)
    
    #write rating to csv file
    # row_id = df.index[df['id'] == int(ids)][0]
    # df.at[row_id, 'rating'] = request.json['rating']
    # df.to_csv(csv_file_path)
    

    '''
    #**************** Solution 2 *****************
    #target variable
    y =  [request.json['rating']]
    Y_list.append(y)
    Y = np.array(Y_list)

    #feature values
    id = 73282 #request.json['id']
    row = df.loc[df['id'] == id]
    row = row[['latitude', 'longitude', 'price']] 
    row = np.array(row)
    X_list.append(row[0])
    X_array = np.array(X_list)

    #train model
    update_model(X_array,Y)
    '''

    return jsonify("Rating saved for id", request.json['id'])

# When clicking submit
@all_routes.route('/model-predict', methods=['POST'])
def model_predict():
    y = list(modified_ratings.values())
    X = df.loc[list(modified_ratings.keys())]
    # Extract just necessary features
    X = X[['latitude', 'longitude', 'price', '_Entire home/apt', '_Hotel room', '_Private room', '_Shared room']]
    # Train model
    update_model(X, y)
    # Prediction
    y_pred = predict_rating(df[['latitude', 'longitude', 'price', '_Entire home/apt', '_Hotel room', '_Private room', '_Shared room']])
    # Here we can use either data or preprocessed csv, whatever.
    y_pred = np.round(y_pred)
    y_pred = np.clip(y_pred, 1, 5)
    df['rating'] = y_pred
    # TODO : Replace ids with existing rating from the user.
    
    return jsonify(df.reset_index().to_json(orient="records"))
