setup:
	python3 -m venv .venv
	.venv/bin/pip install poetry
	.venv/bin/poetry install

run:
	.venv/bin/poetry run start

clean:
	rm -rf .venv poetry.lock

shell:
	.venv/bin/python3