build:
	docker build -t cleaner:latest .

sh: build
	docker run --rm -it -v $$(pwd):/app -v $(HOME)/.aws:/root/.aws cleaner /bin/bash

test: build
	docker run --rm -it -v $$(pwd):/app cleaner python -m unittest discover
