REQUIREMENT = requirements.txt

.PHONY: build test
build: html

%:
	cd docs && make $@

test:
	flake8 app.py
