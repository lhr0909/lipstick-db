-include .env
export

clean:
	rm -rf data

importer:
	python importer.py

full-import: clean importer

main-app:
	uvicorn main:app $(args)

jina-app:
	jina flow --uses flow.yml

build-jina-docker:
	docker build -f jina_app.Dockerfile -t lipstick-db-jina . --build-arg vika_api_key=$$VIKA_API_KEY

build-fastapi-docker:
	docker build -f fastapi.Dockerfile -t lipstick-db-fastapi .
