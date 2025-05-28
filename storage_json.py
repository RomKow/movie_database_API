import json
import os
from istorage import IStorage


class StorageJson(IStorage):
    """
    JSON-based implementation of the IStorage interface.
    """

    def __init__(self, file_path):
        """
        Initialize storage with the given JSON file path.
        :param file_path: Path to JSON file
        """
        self._file_path = file_path

    def list_movies(self):
        """
        Load and return all movies from JSON storage.
        :return: dict of movies
        """
        if not os.path.exists(self._file_path):
            return {}
        with open(self._file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to storage and save changes.
        :param title: Movie title
        :param year: Release year
        :param rating: Movie rating
        :param poster: URL or path to poster image
        """
        movies = self.list_movies()
        movies[title] = {
            'year': year,
            'rating': rating,
            'poster': poster,
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie from storage by title.
        :param title: Movie title to delete
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update an existing movie's rating and save changes.
        :param title: Movie title
        :param rating: New rating
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Save the given movies dictionary to the JSON file.
        :param movies: dict of movies
        """
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2)