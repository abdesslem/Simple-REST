FROM python:3.11-slim

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /data

WORKDIR /data
CMD /app.py