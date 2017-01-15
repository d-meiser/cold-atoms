init:
	pip install -r requirements.txt

test:
	nosetests

.PHONY: init test

