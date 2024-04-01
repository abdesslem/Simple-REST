from typing import List, Optional

import httpx
from furl import furl
from werkzeug.exceptions import BadGateway


class OMDBService:
    def __init__(self, url: str, apikey: str):
        self.url = furl(url)
        self.url.args["apikey"] = apikey
        self.headers = {"Accept": "application/json"}

    def get_movie_by_title(self, title) -> Optional[dict]:
        try:
            self.url.args["t"] = title
            response = httpx.get(url=self.url.url, headers=self.headers)
            response.raise_for_status()
            if response.json().get("Response") == "False":
                movie = None
            else:
                movie = response.json()
            return movie
        except Exception as ex:
            raise BadGateway("An error Occured while calling OMDB API") from ex

    def search_movies(self, search_term: str) -> List[dict]:
        try:
            self.url.args["s"] = search_term
            response = httpx.get(url=self.url.url, headers=self.headers)
            response.raise_for_status()
            return response.json().get("Search")
        except Exception as ex:
            raise BadGateway("An error Occured while calling OMDB API") from ex
