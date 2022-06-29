FROM python:3.9.9

WORKDIR /opt/server

RUN pip install pipenv && apt-get update && apt-get install -y cmake libgl1

COPY Pipfile Pipfile.lock Makefile /opt/server/

RUN pipenv install --system --deploy

COPY . /opt/server/

CMD ["make", "jina-app"]
