from typing import List, Optional

from config import db
from models.movies import Movie


class MovieCRUD:

    @staticmethod
    def get_all(
        limit: int = 10,
        title: Optional[str] = None,
        start: Optional[int] = None,
    ) -> List[Movie]:
        if title:
            return Movie.query.filter_by(title=title).all()

        query = Movie.query.order_by(Movie.title).limit(limit)
        if start and start > 0:
            query = query.offset(start - 1)
        return query.all()

    @staticmethod
    def create(movie: Movie) -> Movie:
        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def get_by_id(id: int) -> Optional[Movie]:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        return movie

    @staticmethod
    def delete_by_id(id: id):
        Movie.query.filter(Movie.id == id).delete()
        db.session.commit()
