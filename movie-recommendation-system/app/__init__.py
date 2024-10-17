import os
import secrets #his can generating secret key for the token and set it for the session 
import json
from bson import ObjectId
from flask import Flask, session, jsonify
from flask_pymongo import PyMongo #his contains tools for interacting with MongoDB database from python.
from flask_cors import CORS
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import dotenv
from .config import Config


dotenv.load_dotenv()


# Initialize the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)
CORS(app) #Cross origin resource sharing

# Generate a secret key and set it for the session
app.secret_key = secrets.token_hex(32)

# Initialize MongoDB with Flask-PyMongo
mongo = PyMongo(app)

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Custom JSON Encoder for handling ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

app.json_encoder = JSONEncoder 

from app import routes # working are correct then go routes.py 
