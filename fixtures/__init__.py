import os
import tempfile
from typing import List, Optional

import pytest

from app import connex_app
from config import db
from models.movies import Movie


@pytest.fixture
def client():
    db_fd, connex_app.app.config["DATABASE"] = tempfile.mkstemp()
    connex_app.app.config["TESTING"] = True

    with connex_app.test_client() as client:
        with connex_app.app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(connex_app.app.config["DATABASE"])


class MockMovieCRUD:

    @staticmethod
    def get_all(
        limit: int = 10,
        title: Optional[str] = None,
        start: Optional[int] = None,
    ) -> List[Movie]:
        if title and title == "title invalid":
            return []
        if title == "Test Movie":
            return [Movie(title="Test Movie", year=2024, imdb_id="1234")]

        movies = []
        movie = Movie(title="Test Movie", year=2024, imdb_id="1234")
        for _ in range(limit):
            movies.append(movie)
        return movies

    @staticmethod
    def create(movie: Movie) -> Movie:
        return movie

    @staticmethod
    def get_by_id(id: int):
        movie = Movie(title="Test Movie", year=2024, imdb_id="1234")
        movie.id = id
        return movie

    @staticmethod
    def delete_by_id(id: id):
        return None


class MockOMDBService:

    def get_movie_by_title(self, title) -> Optional[dict]:
        if title == "Test":
            return {
                "Title": "Test",
                "Year": 2009,
                "imdbID": "123",
                "Author": "Author 1",
            }
        else:
            return None

    def search_movies(self, search_term: str) -> List[dict]:
        return {
            "Search": [
                {
                    "Title": "Test 1",
                    "Year": 2009,
                    "imdbID": "123",
                    "Author": "Author 1",
                },
                {
                    "Title": "Test 2",
                    "Year": 2009,
                    "imdbID": "1244",
                    "Author": "Author 2",
                },
                {
                    "Title": "Test 3",
                    "Year": 2009,
                    "imdbID": "1255",
                    "Author": "Author 3",
                },
            ]
        }
