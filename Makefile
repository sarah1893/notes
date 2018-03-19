REQUIREMENT = requirements.txt

.PHONY: build test
build: html

%:
	cd docs && make $@

test: clean build
	flake8 app.py app_test.py
	python app_test.py
