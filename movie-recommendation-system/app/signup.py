from app import app, mongo
from flask import request, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
from .utils import verify_jwt_token, convert_objectid, fetch_movie_data, allowed_file, get_youtube_trailer, fetch_related_trailers
from app.config import Config


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name', '')
    mobile = data.get('mobile', '')
    email = data.get('email', '')
    password = data.get('password', '')
    confirmpassword = data.get('confirmpassword', '')

    if password != confirmpassword:
        return jsonify({'message': "Passwords do not match"}), 400

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': "Email already exists"}), 400
    
    if mongo.db.users.find_one({'mobile': mobile}):
        return jsonify({'message': "Number is already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    mongo.db.users.insert_one({
        'name': name,
        'mobile': mobile,
        'email': email,
        'password': hashed_password
    })
    return jsonify({"message": "User registered successfully"}), 201
