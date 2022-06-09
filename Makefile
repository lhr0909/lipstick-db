-include .env
export

clean:
	rm -rf data

importer:
	pipenv run python importer.py

full-import: clean importer