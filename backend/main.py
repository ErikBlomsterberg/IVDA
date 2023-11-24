from flask import Flask
from flask_cors import CORS
from routes import all_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(all_routes)

if __name__ == '__main__':
    app.run(debug=True)

