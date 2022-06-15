FROM python:3.8

WORKDIR /usr/src

RUN pip install pipenv && apt-get update && apt-get install -y cmake

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1


COPY Pipfile Pipfile.lock /usr/src

RUN pipenv install --system --deploy

COPY . /usr/src

ENTRYPOINT ["make", "jina-app"]