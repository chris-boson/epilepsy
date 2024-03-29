setup-dev:
	$(info 🔨 Setting up dev environment)
	curl -sSL https://install.python-poetry.org | python - --version 1.3.2
	python3 -m pip install pre-commit
	pre-commit install

setup-latex:
	$(info 🔨 Setting up dev environment)
	sudo apt-get update
	sudo apt-get -y install texlive latexmk texlive-latex-extra
