from app import app, mongo
from flask import request, jsonify, session, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename 
import os
import requests
from .utils import verify_jwt_token, convert_objectid, fetch_movie_data, allowed_file, get_youtube_trailer, fetch_related_trailers
from app.config import Config
from .login import login
from .movies_search import search_movies , get_top_rated_movies
from .signup import signup
from .reset_password import forgot_password, reset_password, verify_otp
from .logout import logout
from .favorites_movie import add_favorite, get_favorites, remove_favorite, check_favorite
from .profile import user_profile, update_profile, upload_profile_picture
from .watch_trailers  import watch_home, save_trailer , get_trailer , recommend_trailers 
from .searched_history import get_recently_watched_movies





@app.route('/')
def indexs():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/styles.css', methods=['GET'])
def styles():
    return render_template('styles.css')

@app.route('/scripts.js', methods=['GET'])
def scripts():
    return render_template('scripts.js')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/forgot-password', methods=['GET'])
def reset():
    return render_template('forgot-password.html')


@app.route('/verify-otp', methods=['GET'])
def verify_otps():
    return render_template('verify-otp.html')


@app.route('/reset-password', methods=['GET'])
def reset_form():
    return render_template('reset-password.html')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/movie_details/<imdbID>', methods=['GET'])
def movie_details(imdbID):
    return render_template('movie_details.html')

@app.route('/movie_detail.html', methods=['GET'])
def movie_detail():
    return render_template('movie_detail.html')


###################### MOVIES__DETAILS AND PLAY TRAILERS #########################


@app.route('/api/movie_details/<imdbID>', methods=['GET'])
def api_movie_details(imdbID):
    movie = mongo.db.search_history.find_one({"results.imdbID": imdbID}, {"results.$": 1})
    if not movie or not movie.get("results"):
        return jsonify({"error": "Movie not found"}), 404

    movie_details = movie["results"][0]

    # Assuming you have a function to get the YouTube trailer URL
    trailer_url = get_youtube_trailer(movie_details["Title"])

    movie_details['trailer_url'] = trailer_url
    return jsonify(movie_details)

@app.route('/api/movie_detail.html', methods=['GET'])
def api_movie_detail():
    # Get the imdbID from the query string
    imdb_id = request.args.get('imdbID')
    
    if not imdb_id:
        return jsonify({"error": "No imdbID provided"}), 400
    
    # Fetch movie details from OMDB API
    omdb_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={app.config['API_KEY']}"
    response = requests.get(omdb_url)

    
    if response.status_code != 200:
        return "Error fetching movie details", 500
    
    movie_detail = response.json()
    
    if movie_detail['Response'] == 'False':
        return "Movie not found", 404

    # Return the movie details as JSON
    return jsonify(movie_detail)

@app.route('/api/movie/search', methods=['POST'])
def search_movie():
    data = request.json
    movie_name = data.get('movie_name')

    if not movie_name:
        return jsonify({'error': 'No movie name provided'}), 400

    movie_data = fetch_movie_data(movie_name, app.config['API_KEY'])
    if movie_data:
        return jsonify(movie_data), 200
    else:
        return jsonify({'error': 'No data found for the provided movie name'}), 404

@app.route('/api/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    token = session.get('token')
    secret_key = app.config['secret_key']
    algorithm = app.config['algorithm']
    
    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    movie = mongo.db.movies.find_one({'imdbID': movie_id})
    if movie:
        convert_objectid([movie])
        return jsonify(movie), 200
    else:
        return jsonify({'error': 'Movie not found'}), 404

@app.route('/api/youtube/search', methods=['POST'])
def search_youtube():
    data = request.json
    query = data.get('query')

    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={app.config['YOUTUBE_API_KEY']}"

    response = requests.get(youtube_url)
    youtube_data = response.json()

    video_ids = []
    for item in youtube_data.get('items', []):
        video_id = item.get('id', {}).get('videoId')
        if video_id:
            video_ids.append(video_id)

    if video_ids:
        youtube_links = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
        return jsonify(youtube_links), 200
    else:
        return jsonify({'error': 'No videos found'}), 404
   