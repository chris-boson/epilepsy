setup-dev:
	$(info 🔨 Setting up dev environment)
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=~/.poetry python3 -
	echo "export PATH=\"\$$HOME/.poetry/bin:\$$PATH\"" >> ~/.bash_profile
	python3 -m pip install pre-commit
	pre-commit install
