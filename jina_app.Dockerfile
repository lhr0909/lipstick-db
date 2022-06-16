FROM python:3.9.9

ARG vika_api_key

WORKDIR /opt/server

RUN pip install pipenv && apt-get update && apt-get install -y cmake libgl1

COPY Pipfile Pipfile.lock Makefile /opt/server/

RUN pipenv install --system --deploy

COPY . /opt/server/

RUN VIKA_API_KEY=${vika_api_key} make importer

CMD ["make", "jina-app"]
