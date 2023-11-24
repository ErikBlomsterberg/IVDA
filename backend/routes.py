import csv

from flask import Blueprint, jsonify

csv_file_path = 'Data/zurich.csv'

all_routes = Blueprint('all_routes', __name__)

@all_routes.route('/apartments', methods=['GET'])
def start_page():
    csv_encoding = 'utf-8'
    data = []
    with open(csv_file_path, 'r', encoding=csv_encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for i, row in enumerate(csv_reader):
            data.append(row)
            if(i == 9):
                break
    return jsonify(data)



