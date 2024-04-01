from contextlib import nullcontext as does_not_raise

import pytest
from werkzeug.exceptions import BadRequest

from config import ADMIN_APIKEY
from controllers.movies import MovieController
from fixtures import MockMovieCRUD, MockOMDBService, client

movie_controller = MovieController(movies=MockMovieCRUD)


@pytest.mark.parametrize(
    "title,start,limit,expectation",
    [
        ("Test Movie", None, None, 1),
        ("Test Movie", 1, 5, 1),
        (None, None, 5, 5),
        (None, 5, 5, 5),
    ],
)
def test_get_movies(title, start, limit, expectation):
    movies = movie_controller.get_movies(title=title, start=start, limit=limit)
    assert type(movies.get("movies")) is list
    assert len(movies.get("movies")) == expectation


def test_filter_movie_by_title():
    movie_controller = MovieController(movies=MockMovieCRUD)
    result = movie_controller.get_movies(title="title invalid")
    assert type(result) is dict
    assert result.get("movies") == []


@pytest.mark.parametrize(
    "title,expectation",
    [
        ("Test", does_not_raise()),
        ("Invalid", pytest.raises(BadRequest)),
    ],
)
def test_create_movie_exceptions(title, expectation):
    with expectation:
        movie_controller = MovieController(
            movies=MockMovieCRUD, omdb_service=MockOMDBService()
        )
        movie_controller.create_new_movie(title=title)


def test_create_movie():
    movie_controller = MovieController(
        movies=MockMovieCRUD, omdb_service=MockOMDBService()
    )
    movie = movie_controller.create_new_movie(title="Test")
    assert type(movie) is dict
    assert movie.get("title") == "Test"
    assert movie.get("year") == 2009
    assert movie.get("imdb_id") == "123"


def test_delete_movie():
    movie_controller = MovieController(movies=MockMovieCRUD)
    movie = movie_controller.delete_movie_by_id(id=1)
    assert movie is None


def test_get_movies_endpoint(client):
    rv = client.get("/movies")
    assert rv.status_code == 200


def test_movie_not_found(client):
    rv = client.get("/movies/890")
    assert rv.status_code == 404


def test_secure_delete(client):
    rv = client.delete("/movies/1")
    assert rv.status_code == 401


def test_delete(client):
    headers = {"X-Auth": ADMIN_APIKEY}
    rv = client.delete("/movies/1", headers=headers)
    assert rv.status_code == 204
