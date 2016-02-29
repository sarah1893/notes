REQUIREMENT = requirements.txt

.PHONY: build
build: html

%:
	cd docs && make $@
