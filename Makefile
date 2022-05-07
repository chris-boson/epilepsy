setup-dev:
	$(info 🔨 Setting up dev environment)
	git submodule update --init --recursive --remote
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=~/.poetry python3.8 -
	sudo ln -s ~/.poetry/bin/poetry /usr/local/bin/poetry
	curl https://pre-commit.com/install-local.py | python3
	pre-commit install
