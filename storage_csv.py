import csv
import os
from istorage import IStorage


class StorageCsv(IStorage):
    """
    CSV-based implementation of the IStorage interface.
    Stores movies in a CSV file with columns: title, year, rating, poster.
    """

    def __init__(self, file_path):
        """
        Initialize CSV storage with the given file path.
        :param file_path: Path to CSV file
        """
        self._file_path = file_path

    def list_movies(self):
        """
        Load and return all movies from CSV storage.
        :return: dict of movies keyed by title
        """
        if not os.path.exists(self._file_path):
            return {}

        movies = {}
        with open(self._file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['title']
                movies[title] = {
                    'year': int(row['year']),
                    'rating': float(row['rating']),
                    'poster': row.get('poster', '')
                }
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to CSV storage and save changes.
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
        Delete a movie from CSV storage by title.
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
        Save all movies to the CSV file, overwriting existing data.
        :param movies: dict of movies keyed by title
        """
        # Ensure directory exists
        dirpath = os.path.dirname(self._file_path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(self._file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'year', 'rating', 'poster']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for title, info in movies.items():
                writer.writerow({
                    'title': title,
                    'year': info['year'],
                    'rating': info['rating'],
                    'poster': info.get('poster', '')
                })
