
install: 
	poetry install

build: 
	poetry build

package-install: 
	pip3 install --user dist/*.whl

selfcheck:
	poetry check

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv --cov=page_loader --cov-report xml tests
