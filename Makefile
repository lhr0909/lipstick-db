-include .env
export

clean:
	rm -rf data

importer:
	pipenv run python importer.py

full-import: clean importer

main-app:
	JINA_MP_START_METHOD=forkserver pipenv run uvicorn main:app $(args)

jina-app:
	pipenv run jina flow --uses flow.yml