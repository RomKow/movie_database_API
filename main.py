## File: main.py

"""
Entry point for the Movie Application.
"""
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Initialize storage and application, then run the CLI loop.
    """
    # Use JSON file as our storage backend
    storage = StorageJson('movies.json')
    # Create the application with the chosen storage
    app = MovieApp(storage)
    # Start the interactive loop
    app.run()


if __name__ == '__main__':
    main()
