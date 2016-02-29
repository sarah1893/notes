REQUIREMENT = requirements.txt

.PHONY: build
build: html

%:
	pip -q install -r $(REQUIREMENT)
	cd docs && make $@
