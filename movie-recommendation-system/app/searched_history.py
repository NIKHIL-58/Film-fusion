from app import app, mongo
from flask import request, jsonify, session
from bson import ObjectId
import jwt
from datetime import datetime
from .utils import verify_jwt_token, convert_objectid, fetch_movie_data, get_youtube_trailer, fetch_related_trailers
from app.config import Config

@app.route('/api/recently_watched', methods=['GET'])
def get_recently_watched_movies():
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

    search_history = mongo.db.search_history.find({"user_id": user_id}).sort("_id", -1)
    movies = {}

    for history in search_history:
        results = history.get("results", [])
        for movie in results:
            video_id = movie.get("imdbID")
            if video_id not in movies:
                title = movie.get("Title")
                poster = movie.get("Poster")

                movies[video_id] = {
                    "title": title,
                    "poster": poster,
                    "details_url": f"/movie_details/{video_id}"
                }

    return jsonify(list(movies.values()))

