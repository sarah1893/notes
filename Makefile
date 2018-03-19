REQUIREMENT = requirements.txt

.PHONY: build test
build: html

%:
	cd docs && make $@

test: clean build
	flake8 app.py app_test.py
	coverage run app_test.py && coverage report --fail-under=80 -m app.py app_test.py
