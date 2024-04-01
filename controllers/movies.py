from typing import Optional

from werkzeug.exceptions import BadRequest

from crud.movies import MovieCRUD
from models.movies import Movie
from service.omdb import OMDBService


class MovieController:
    def __init__(self, movies: MovieCRUD, omdb_service: Optional[OMDBService] = None):
        self.movies = movies
        self.omdb_service = omdb_service

    def get_movies(
        self,
        limit: int = 10,
        title: Optional[str] = None,
        start: Optional[int] = None,
    ):
        movies = self.movies.get_all(title=title, start=start, limit=limit)
        return {"movies": [mv.json() for mv in movies]}

    def get_movie_by_id(self, id: int):
        movie = self.movies.get_by_id(id=id)
        if movie:
            movie = movie.json()
        return movie

    def create_new_movie(self, title: str):
        omdb_movie = self.omdb_service.get_movie_by_title(title=title)
        if omdb_movie:
            new_movie = self.movies.create(
                movie=Movie(
                    title=omdb_movie.get("Title"),
                    year=omdb_movie.get("Year"),
                    imdb_id=omdb_movie.get("imdbID"),
                )
            )
            return new_movie.json()
        else:
            raise BadRequest("Please use a Valid Movie name")

    def delete_movie_by_id(self, id: int):
        _ = self.movies.delete_by_id(id=id)
