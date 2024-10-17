from app import app, mongo
from flask import request, jsonify, session
import os
from bson import ObjectId
import jwt
import requests
from datetime import datetime
from .utils import verify_jwt_token, convert_objectid, fetch_movie_data, allowed_file, get_youtube_trailer, fetch_related_trailers
from app.config import Config



@app.route('/watch_home', methods=['GET'])
def watch_home():
    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithms = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithms)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401
    
    trailers = list(mongo.db.watched_trailers.find({'user_id': user_id}).sort("_id", -1).limit(5))
    # Convert ObjectId to string if needed
    trailers = [{**trailer, '_id': str(trailer['_id'])} for trailer in trailers]
    
    return jsonify(trailers)

@app.route('/save_trailer', methods=['POST'])
def save_trailer():
    token = session.get('token')
    if not token:
        return jsonify({"error": "No token found"}), 401

    secret_key = app.config['SECRET_KEY']
    algorithms = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithms)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    movie_title = data.get('movie_title')
    trailer_url = data.get('trailer_url')

    if movie_title and trailer_url:
        existing_trailer = mongo.db.watched_trailers.find_one({
            'user_id': user_id,
            'movie_title': movie_title
        })

        if not existing_trailer:
            mongo.db.watched_trailers.insert_one({
                'user_id': user_id,
                'movie_title': movie_title,
                'trailer_url': trailer_url
            })
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already_saved'}), 200
    
    return jsonify({'status': 'failed'}), 400


@app.route('/get_trailer/<imdb_id>', methods=['GET'])
def get_trailer(imdb_id):
    omdb_url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}'
    youtube_search_url = 'https://www.googleapis.com/youtube/v3/search'

    try:
        # Fetch movie details from OMDb
        omdb_response = requests.get(omdb_url)
        omdb_data = omdb_response.json()

        if omdb_data.get('Response') == 'True':
            title = omdb_data.get('Title')
            year = omdb_data.get('Year')

            # Search for trailer on YouTube
            params = {
                'part': 'snippet',
                'q': f'{title} {year} trailer',
                'key': youtube_api_key,
                'type': 'video',
                'maxResults': 2
            }
            youtube_response = requests.get(youtube_search_url, params=params)
            youtube_data = youtube_response.json()

            if youtube_data.get('items'):
                video_id = youtube_data['items'][0]['id']['videoId']
                trailer_url = f'https://www.youtube.com/embed/{video_id}'

                # Save the played trailer in MongoDB
                user_id = session.get('user_id')
                if user_id:
                    mongo.db.played_trailers.update_one(
                        {"user_id": user_id, "imdb_id": imdb_id},
                        {
                            "$set": {
                                "user_id": user_id,
                                "imdb_id": imdb_id,
                                "title": title,
                                "year": year,
                                "trailer_url": trailer_url,
                                "poster": omdb_data.get('Poster'),
                                "played_at": datetime.utcnow()
                            }
                        },
                        upsert=True
                    )

                return jsonify({'trailerUrl': trailer_url})
            else:
                return jsonify({'error': 'No trailer found on YouTube'})

        return jsonify({'error': 'Movie not found'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/recommend_trailers', methods=['GET'])
def recommend_trailers():
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

    # Fetch the last watched trailers
    trailers = list(mongo.db.watched_trailers.find({'user_id': user_id}).sort("_id", -1).limit(2))
    
    # Get related trailers based on the last watched trailers
    related_trailers = []
    for trailer in trailers:
        movie_title = trailer.get('movie_title')
        if movie_title:
            related_trailers.extend(fetch_related_trailers(movie_title))
    
    # Convert ObjectId fields to strings in the watched trailers
    convert_objectid(related_trailers)
    
    return jsonify(related_trailers)