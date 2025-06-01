# omdb_client.py

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = 'http://www.omdbapi.com/'


class OmdbAPIError(Exception):
    """Raised when the OMDb API call fails due to network or HTTP errors."""
    pass


class MovieNotFoundError(Exception):
    """Raised when the requested movie is not found in OMDb."""
    pass


def get_movie_data(title: str) -> dict:
    """
    Fetch movie details from OMDb by title.

    :param title: Movie title to search for
    :return: Dict with keys 'Title', 'Year', 'imdbRating', 'Poster', ...
    :raises MovieNotFoundError: If OMDb responds with no such movie
    :raises OmdbAPIError: On network issues or HTTP errors
    """
    if not API_KEY:
        raise OmdbAPIError('OMDB_API_KEY is not set in environment')

    params = {
        'apikey': API_KEY,
        't': title,
    }

    try:
        response = requests.get(OMDB_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OmdbAPIError(f'Failed to reach OMDb API: {exc}') from exc

    data = response.json()
    if data.get('Response') == 'False':
        # OMDb returns {"Response":"False","Error":"Movie not found!"}
        raise MovieNotFoundError(data.get('Error', 'Movie not found'))

    return data
