-include .env
export

clean:
	rm -rf data

importer:
	pipenv run python importer.py

full-import: clean importer

main-app:
	pipenv run uvicorn main:app $(args)

jina-app:
	pipenv run python app.py