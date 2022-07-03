# Lipstick DB

Find the right lipstick using AI!

[中文文档](./README.md)

[YouTube](https://www.youtube.com/watch?v=KMeyjn3fcKY)

[Demo](https://lipstick-db.senses.chat/en)

# Local Development Steps

## Prerequisites

- Docker Desktop (for minio installation on local, if you don't use Docker, then you will need to get an S3 bucket from AWS)
- Python v3.8+, recommended v3.9+ (use pyenv to manage Python environment)
- NodeJS v14+ (recommended v16 LTS) and yarn v1 (recommended), use nvm to manage NodeJS environment
- make (for environment variable injection)

## Docker Dependency

Start minio service:

```
docker compose up -d minio-service
```

Log into minio at http://localhost:9001 with `minio` as username and `minio123` as password. Create a bucket named `lipstick-db`.

## Code Dependencies

```shell
# python deps
pip install pipenv
pipenv install
# enter pipenv shell
pipenv shell
# nodejs deps
cd ui
yarn
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values during the later steps.

## Get the data

Currently the data is hosted on an airtable-like product in China, and we are working on migrating this part to use Airtable.

Please contact me if you have time to help me update the importer to point to Airtable. Happy to work with you to migrate the data over.

## Start Jina Flow

```shell
make jina-local

# use this one if on MacOS
JINA_MP_START_METHOD=forkserver make jina-local
```

Jina Flow server will start at port 8888

## Start FastAPI Server

```shell
make main-app

# turn on reload mode for development
make main-app args="--host 0.0.0.0 --reload"

# use this one if on MacOS
JINA_MP_START_METHOD=forkserver make main-app args="--host 0.0.0.0 --reload"
```

FastAPI server will start at port 8000

## Start UI

```shell
cd ui
yarn dev
```

UI server will start at port 3000

# Deployment

## Build Docker images

```shell
make build-jina-docker # please run this only after the data is imported locally
make build-fastapi-docker
```

start using docker-compose after build：

```shell
docker compose up -d
```

I recommend to deploy on a server with 4 cores and 8GB RAM.

As for UI, I recommend you deploy onto [Vercel](https://vercel.com/guides/deploying-nextjs-with-vercel).

## Kubernetes Deployment

Please refer to the `k8s` directory for the kubernetes deployment.

Note that the kubernetes deployment is reference only, since the project uses annlite as document store, and it will OOM often during search. Please change to an [external document store](https://docarray.jina.ai/advanced/document-store/benchmark/) if you want to use kubernetes.

# License

[Apache License v2](./LICENSE)
