.SILENT: bump-version release

.PHONY: init lint tests e2e coverage bump-version release

init:
	poetry install --no-root

lint:
	poetry run flake8 py3server

tests:
	poetry run tox -e tests

e2e:
	poetry run tox -e e2e

coverage:
	poetry run tox -e coverage

release:
	$(eval MESSAGE=$(shell poetry version $(BUMP)))
	$(eval NEW_VERSION=$(word 4,$(subst -, ,$(MESSAGE))))
	git add pyproject.toml
	git commit -m '$(MESSAGE)'
	git tag -a v$(NEW_VERSION) -m 'v$(NEW_VERSION)'
	git push --atomic origin main v$(NEW_VERSION)
