from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for movie storage, defining the CRUD operations.
    """

    @abstractmethod
    def list_movies(self):
        """
        Return a dictionary of all movies in storage.
        :return: dict mapping title to info dict
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Add a movie to storage.
        :param title: Movie title
        :param year: Release year
        :param rating: Movie rating
        :param poster: URL or path to poster image
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie by title.
        :param title: Movie title to delete
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Update an existing movie's rating.
        :param title: Movie title
        :param rating: New rating
        """
        pass
