# test_storage_json.py

import pytest

from storage.storage_json import StorageJson


@pytest.fixture
def temp_storage_path(tmp_path):
    # Creates a temporary JSON file path for isolation
    return str(tmp_path / "test_movies.json")


@pytest.fixture
def storage(temp_storage_path):
    # Instantiates StorageJson using the temp file path
    return StorageJson(temp_storage_path)


def test_list_empty(storage):
    """Listing movies on empty storage returns empty dict."""
    assert storage.list_movies() == {}


def test_add_movie(storage):
    """Adding a movie persists it correctly."""
    storage.add_movie("Test Movie", 2025, 7.5, "poster_url")
    movies = storage.list_movies()
    assert "Test Movie" in movies

    info = movies["Test Movie"]
    assert info["year"] == 2025
    assert info["rating"] == 7.5
    assert info["poster"] == "poster_url"


def test_update_movie(storage):
    """Updating an existing movie adjusts its rating."""
    storage.add_movie("Test", 2025, 6.0, "")
    storage.update_movie("Test", 8.0)
    movies = storage.list_movies()
    assert movies["Test"]["rating"] == 8.0


def test_delete_movie(storage):
    """Deleting a movie removes it from storage."""
    storage.add_movie("DeleteMe", 2025, 5.0, "")
    storage.delete_movie("DeleteMe")
    movies = storage.list_movies()
    assert "DeleteMe" not in movies
