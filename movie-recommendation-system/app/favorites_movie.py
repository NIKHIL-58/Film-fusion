from app import app, mongo
from flask import request, jsonify, session, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename 
import os
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import requests
from datetime import datetime
from .utils import verify_jwt_token, convert_objectid, fetch_movie_data, allowed_file, get_youtube_trailer, fetch_related_trailers
from app.config import Config

@app.route('/api/add_favorite', methods=['POST'])
def add_favorite():
    # Check if user is logged in
    if 'token' not in session:
        return jsonify({'error': 'User not logged in.'}), 401

    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')
    movie_id = request.json.get('imdbID')

    if not user_id or not movie_id:
        return jsonify({"error": "Invalid request"}), 400

    mongo.db.favorites.update_one(
        {"user_id": user_id},
        {"$addToSet": {"favorites": movie_id}},
        upsert=True
    )

    return jsonify({"message": "Movie added to favorites"}), 200

@app.route('/api/get_favorites', methods=['GET'])
def get_favorites():
    # Check if user is logged in
    if 'token' not in session:
        return jsonify({'error': 'User not logged in.'}), 401

    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')

    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    user_favorites = mongo.db.favorites.find_one({"user_id": user_id})

    if user_favorites:
        favorite_movie_ids = user_favorites.get('favorites', [])
        favorite_movies = []

        for imdbID in favorite_movie_ids:
            response = requests.get(f"http://www.omdbapi.com/?i={imdbID}&apikey={app.config['API_KEY']}")
            if response.status_code == 200:
                movie_data = response.json()
                favorite_movies.append({
                    "Title": movie_data.get("Title"),
                    "Poster": movie_data.get("Poster"),
                    "Year": movie_data.get("Year"),
                    "imdbID": movie_data.get("imdbID")
                })

        return jsonify(favorite_movies), 200

    return jsonify([]), 200

@app.route('/api/remove_favorite', methods=['POST'])
def remove_favorite():
    # Check if user is logged in
    if 'token' not in session:
        return jsonify({'error': 'User not logged in.'}), 401

    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')
    movie_id = request.json.get('imdbID')

    if not user_id or not movie_id:
        return jsonify({"error": "Invalid request"}), 400

    mongo.db.favorites.update_one(
        {"user_id": user_id},
        {"$pull": {"favorites": movie_id}}
    )

    return jsonify({"message": "Movie removed from favorites"}), 200

@app.route('/api/check_favorite/<string:imdbID>', methods=['GET'])
def check_favorite(imdbID):
    # Check if user is logged in
    if 'token' not in session:
        return jsonify({'error': 'User not logged in.'}), 401

    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')

    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    user_favorites = mongo.db.favorites.find_one({"user_id": user_id})
    # Check if the user has any favorites; if not, default to an empty list 
    if user_favorites is None:
        is_favorited = False
    else:
        is_favorited = imdbID in user_favorites.get('favorites', [])

    return jsonify({"isFavorited": is_favorited}), 200


