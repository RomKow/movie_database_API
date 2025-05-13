import json
import os

DATA_FILE = 'data.json'


def get_movies():
    """Load and return the movies dict from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_movies(movies):
    """Save the movies dict to the JSON data file."""
    json_str = json.dumps(movies, indent=2)
    with open(DATA_FILE, 'w', encoding='utf-8') as fh:
        fh.write(json_str)


def add_movie(title, year, rating):
    """Add a movie and save the updated dict."""
    movies = get_movies()
    movies[title] = {
        'year': year,
        'rating': rating,
    }
    save_movies(movies)


def delete_movie(title):
    """Delete a movie and save the updated dict."""
    movies = get_movies()
    if title in movies:
        del movies[title]
    save_movies(movies)


def update_movie(title, rating):
    """Update a movie's rating and save the updated dict."""
    movies = get_movies()
    if title in movies:
        movies[title]['rating'] = rating
        save_movies(movies)
