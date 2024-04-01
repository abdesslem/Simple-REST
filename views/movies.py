from typing import Optional

from flask import Response
from flask import current_app as app
from werkzeug.exceptions import NotFound

from config import OMDB_APIKEY, OMDB_URL
from controllers.movies import MovieController
from crud.movies import MovieCRUD
from service.omdb import OMDBService


def get_movies(
    limit: int = 10, title: Optional[str] = None, start: Optional[int] = None
) -> dict:
    movie_controller = MovieController(movies=MovieCRUD)
    return movie_controller.get_movies(title=title, start=start, limit=limit)


def create_movie(payload: dict):
    title = payload.get("title")
    movie_controller = MovieController(
        movies=MovieCRUD,
        omdb_service=OMDBService(url=OMDB_URL, apikey=OMDB_APIKEY),
    )
    return movie_controller.create_new_movie(title=title)


def get_movie(id: int):
    movie_controller = MovieController(movies=MovieCRUD)
    movie = movie_controller.get_movie_by_id(id=id)
    if not movie:
        app.logger.debug(f"Movie with ID {id} could not be found in the database")
        raise NotFound(f"Movie with ID {id} not found")
    return movie


def delete_movie(id: int):
    movie_controller = MovieController(movies=MovieCRUD)
    movie = movie_controller.get_movie_by_id(id=id)
    if not movie:
        app.logger.debug(f"Movie with ID {id} could not be found in the database")
        raise NotFound(f"Movie with ID {id} not found")
    _ = movie_controller.delete_movie_by_id(id=id)
    return Response(status=204)
