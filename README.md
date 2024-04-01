
# Brite OMDB test API

A simple CRUD API for movies

### Install requirements
```
python3 -m pip install pipenv --user
pipenv install --dev
```
### Set Env vars
```
export OMDB_URL="API URL"
export OMDB_APIKEY="API KEY"
export MAX_AUTHORIZED_NUMBER="Max Numbers of movies to import"
export ADMIN_APIKEY="Admin token, needed to delete movies"
```

### Import Data

To get the list of movies, run this command

```
pipenv run python scrape_movies.py
```

This command will initialiate the DB and insert 100 movies.

### Run locally

```
pipenv run python app.py
```

or using uvicorn

```
uvicorn app:connex_app
```

Visit the swagger at: http://127.0.0.1:8000/ui/#/

### Run Test
```
pipenv run pytest
```

### Build and Run with docker
```
docker build -t movies-api .
docker run --env OMDB_URL=<url> --env OMDB_APIKEY=<key> --env ADMIN_APIKEY=<secret> --env MAX_AUTHORIZED_NUMBER=<number> -d -p 8000:8000 movies-api
```


