## File: main.py

"""
Entry point for the Movie Application with dynamic storage selection.
"""
import argparse

from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


def parse_args():
    parser = argparse.ArgumentParser(
        description="Movie App: Choose storage type and file path."
    )
    parser.add_argument(
        "--storage",
        choices=["json", "csv"],
        default="json",
        help="Storage backend to use (json or csv)."
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Path to the storage file. If omitted, uses default based on storage type."
    )
    return parser.parse_args()


def main():
    """
    Initialize storage and application based on CLI args, then run.
    """
    args = parse_args()

    # Determine default file names if not provided
    if args.file:
        file_path = args.file
    else:
        file_path = "data/movies.json" if args.storage == "json" else "data/movies.csv"

    # Instantiate the selected storage backend
    if args.storage == "json":
        storage = StorageJson(file_path)
    else:
        storage = StorageCsv(file_path)

    # Create and run the application
    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main()
