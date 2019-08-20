.PHONY: test
test:
	cd incaffeine && nosetests --with-coverage incaffeine

dependencies:
	pip3 install -r requirements.txt
