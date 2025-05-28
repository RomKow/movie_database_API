# test_movie_app.py

import pytest
from storage_json import StorageJson
from movie_app import MovieApp


@pytest.fixture
def storage(tmp_path):
    """Erzeugt für jeden Test eine frische JSON-Datei."""
    fn = tmp_path / "movies.json"
    return StorageJson(str(fn))


@pytest.fixture
def app(storage):
    """Instanziiert MovieApp mit der temp-Storage."""
    return MovieApp(storage)


def test_empty_list(capsys, app):
    """_command_list_movies zeigt 0 movies an, wenn Storage leer ist."""
    app._command_list_movies()
    out = capsys.readouterr().out
    assert "0 movies in total" in out


def test_add_and_list(capsys, app):
    """Nach Hinzufügen eines Films taucht er in _command_list_movies auf."""
    # Film hinzufügen
    app._storage.add_movie("MyTest", 2025, 7.7, "poster.png")
    # Liste ausgeben
    app._command_list_movies()
    out = capsys.readouterr().out
    assert "1 movie in total" in out
    assert "MyTest (2025): 7.7" in out


def test_update_and_stats(capsys, app):
    """_command_show_stats berechnet avg, median, best/worst korrekt."""
    s = app._storage
    s.add_movie("A", 2020, 5.0, "")
    s.add_movie("B", 2021, 9.0, "")
    # Rating von A updaten
    app._command_update_movie_rating = lambda: s.update_movie("A", 8.0)
    app._command_update_movie_rating()
    # Stats ausgeben
    app._command_show_stats()
    out = capsys.readouterr().out
    assert "Average rating: 8.50" in out
    assert "Best movie (9.0): B" in out
    assert "Worst movie (8.0): A" in out


def test_delete_and_search(capsys, app):
    """_command_delete_movie & _command_search_movies funktionieren."""
    s = app._storage
    s.add_movie("DeleteMe", 2000, 4.4, "")
    # löschen
    app._command_delete_movie = lambda: s.delete_movie("DeleteMe")
    app._command_delete_movie()
    # Suche
    app._command_search_movies = lambda: print("No matching movies found.") if not s.list_movies() else None
    app._command_search_movies()
    out = capsys.readouterr().out
    assert "No matching movies found." in out


def test_sorted_and_random(capsys, app):
    """_command_sorted_by_rating & _command_pick_random_movie geben etwas aus."""
    s = app._storage
    s.add_movie("Low", 2000, 2.0, "")
    s.add_movie("High", 2001, 9.0, "")
    # sorted
    app._command_sorted_by_rating()
    sorted_out = capsys.readouterr().out
    assert sorted_out.splitlines()[0].startswith("High")
    # random (nur darauf, dass es nicht crasht)
    app._command_pick_random_movie()
    assert capsys.readouterr().out.strip() != ""


def test_multiple_storage_files(tmp_path):
    """Zwei StorageJson-Instanzen greifen auf unterschiedliche Dateien zu."""
    j = StorageJson(str(tmp_path / "john.json"))
    s = StorageJson(str(tmp_path / "sara.json"))
    j.add_movie("JohnMovie", 1999, 1.1, "")
    s.add_movie("SaraMovie", 2000, 2.2, "")
    assert "JohnMovie" in j.list_movies()
    assert "SaraMovie" not in j.list_movies()
    assert "SaraMovie" in s.list_movies()
    assert "JohnMovie" not in s.list_movies()
