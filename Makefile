install:
	echo "Installing python dependencies"
	pip install --upgrade pip && pip install -r requirements.txt

test:
	python -m pytest --cov=src -v --cov-config=.coveragerc --cov-report term --cov-report xml:coverage.xml tests

help:
	@echo "    install"
	@echo "        Install python dependencies"
	@echo "    test"
	@echo "        Run tests on the project"
	@echo "    help"
	@echo "        Show this help message"