import config
from config import MAX_AUTHORIZED_NUMBER, OMDB_APIKEY, OMDB_URL
from crud.movies import MovieCRUD
from models.movies import Movie
from service.omdb import OMDBService

if __name__ == "__main__":
    omdb_service = OMDBService(url=OMDB_URL, apikey=OMDB_APIKEY)
    with config.app.app_context():
        config.db.create_all()

    with config.app.app_context():
        existing_movies = MovieCRUD.get_all()
        if existing_movies:
            exit("The DB already contains movies")

    """
        The API does not allow to reteive the first 100 movies with
        pagination, we used the search functionality to get movies
    """
    movie_numbers = 0
    search_terms = [
        "play",
        "game",
        "speed",
        "dead",
        "alive",
        "best",
        "worst",
        "top",
        "love",
        "day",
        "hate",
        "night",
    ]
    for term in search_terms:
        movies = omdb_service.search_movies(search_term=term)
        for mv in movies:
            if movie_numbers < MAX_AUTHORIZED_NUMBER:
                movie = Movie(
                    title=mv.get("Title"),
                    year=mv.get("Year"),
                    imdb_id=mv.get("imdbID"),
                )
                with config.app.app_context():
                    MovieCRUD.create(movie=movie)
                movie_numbers += 1
            else:
                break
