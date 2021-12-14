test-all:
	python -m unittest discover test

requirements:
	pip install -r requirements.txt;
	brew install graphviz;