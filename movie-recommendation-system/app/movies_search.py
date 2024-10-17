from app import app , mongo
from flask import request, jsonify, session
import os
import requests
from datetime import datetime
from .utils import verify_jwt_token
from app.config import Config

@app.route('/search', methods=['POST'])
def search_movies():
    try:
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

        # Parse search parameters
        data = request.get_json()
        query = data.get('query', '')

        # Validate search parameters
        if not query:
            return jsonify({'error': 'Search parameter is required.'}), 400

        # Initialize list to hold filtered movies
        filtered_movies = []

        # Fetch results from the OMDB API
        for page in range(1, 2):  # Adjust pages as needed
            search_params = {
                's': query,
                'apikey': Config.API_KEY,
                'page': page
            }
            response = requests.get('http://www.omdbapi.com/', params=search_params)
            
            if response.status_code != 200:
                print(f"Error: OMDB API returned status code {response.status_code}")
                return jsonify({'error': 'Error fetching data from OMDB API.'}), 500
            
            try:
                movies = response.json().get('Search', [])
            except ValueError as e:
                print(f"Error decoding JSON: {e}")
                return jsonify({'error': 'Invalid response from OMDB API.'}), 500

            if not movies:
                break
            
            for movie in movies:
                imdb_id = movie.get('imdbID')
                if imdb_id:
                    details_url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={Config.API_KEY}'
                    details_response = requests.get(details_url)
                    
                    if details_response.status_code != 200:
                        print(f"Error: OMDB API returned status code {details_response.status_code} for movie ID {imdb_id}")
                        continue
                    
                    try:
                        movie_details = details_response.json()
                    except ValueError as e:
                        print(f"Error decoding JSON for movie ID {imdb_id}: {e}")
                        continue

                    filtered_movies.append(movie_details)

        # Store search history in MongoDB
        search_history_entry = {
            'user_id': user_id,
            'search_query': data,
            'results': filtered_movies
        }
        mongo.db.search_history.insert_one(search_history_entry)

        return jsonify(filtered_movies)

    except Exception as e:
        # Log the error with more details
        print(f"Internal server error: {str(e)}")
        return jsonify({'error': 'An internal error occurred.'}), 500

@app.route('/top-rated-movies', methods=['GET'])
def get_top_rated_movies():
    api_key = 'dd39691a'
    all_movies = []
    for page in range(1, 2):  # Fetch results from the first 10 pages
        try:
            # Fetch a broad list of movies from OMDB API
            response = requests.get(f'http://www.omdbapi.com/?apikey={api_key}&s=movie&type=movie&page={page}')
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()

            if 'Search' in data:
                for item in data['Search']:
                    try:
                        movie_response = requests.get(f'http://www.omdbapi.com/?apikey={api_key}&i={item["imdbID"]}')
                        movie_response.raise_for_status()
                        movie_data = movie_response.json()

                        # Ensure IMDb rating is present and a valid float
                        imdb_rating = movie_data.get('imdbRating')
                        if imdb_rating and float(imdb_rating) > 7:  # Consider only valid IMDb ratings
                            all_movies.append({
                                'imdbID': item['imdbID'],
                                'title': movie_data.get('Title'),
                                'poster': movie_data.get('Poster', 'path/to/placeholder.jpg'),
                                'year': movie_data.get('Year'),
                                'language': movie_data.get('Language'),
                                'genre': movie_data.get('Genre'),
                                'imdb_rating': float(imdb_rating),
                                'trailer': ''  # Handle trailer URL separately or remove if not available
                            })
                    except Exception as e:
                        print(f"Error fetching details for {item['imdbID']}: {e}")
            else:
                print("No 'Search' key in API response")
                continue  # Go to the next page if no results on the current page

        except Exception as e:
            print(f"Error fetching movies: {e}")

    # Filter and sort the movies by IMDb rating, then get the top 15
    top_rated_movies = sorted(all_movies, key=lambda x: x['imdb_rating'], reverse=True)[:30]

    return jsonify(top_rated_movies)
