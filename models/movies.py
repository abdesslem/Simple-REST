from config import db


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    imdb_id = db.Column(db.String(32))

    def __init__(self, title, year, imdb_id):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "imdb_id": self.imdb_id,
        }
