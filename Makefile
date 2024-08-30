.DEFAULT_GOAL := test

.PHONY: clean
clean:
	rm -rf .tox .cache .venv requirements.txt .git/hooks/pre-commit testdir

.PHONY: .venv-prod
.venv-prod:
	poetry env remove --all
	poetry config virtualenvs.in-project true
	poetry install --without dev

.venv:
	poetry env remove --all
	poetry config virtualenvs.in-project true
	poetry install

.PHONY: pre-commit
pre-commit: .venv
	.venv/bin/python -m pre_commit install

.PHONY: test
test: pre-commit
	tox run

.PHONY: push
push:
	docker buildx build --platform linux/amd64,linux/arm64 -t tianlechen/sfm:latest --push .

testdir:
	.venv/bin/python make_testdir.py
