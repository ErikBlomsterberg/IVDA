import json

from flask import Blueprint, request, jsonify
import pandas as pd 
import numpy as np
from model import update_model, predict_rating, model_error
import csv

training_path = 'Data/data.csv'
df = pd.read_csv(training_path, index_col='id')
df_clean = pd.read_csv('Data/preprocessed.csv', index_col='id')
#df = pd.read_csv(training_path)
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
    modified_ratings.update({int(request.json['id']): int(request.json['rating'])})
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
    #y_pred = np.round(y_pred)
    y_pred = np.clip(y_pred, 1, 5)
    df_clean['rating'] = y_pred
    # TODO : Replace ids with existing rating from the user.
    return json.loads(df_clean.reset_index().to_json(orient="records"))


@all_routes.route('/model-stats', methods=['GET'])
def model_stats():
    y_label = list(modified_ratings.values())
    X = df.loc[list(modified_ratings.keys())]
    y_pred = predict_rating(X[['latitude', 'longitude', 'price', '_Entire home/apt', '_Hotel room', '_Private room', '_Shared room']])
    error = round(model_error(y_label, y_pred), 3)
    n_ratings = f'{len(modified_ratings)} / {df.shape[0]}'
    return jsonify({'error': error, 'n_ratings': n_ratings})