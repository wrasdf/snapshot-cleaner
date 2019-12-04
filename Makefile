build:
	docker build -t cleaner:latest .

sh: build
	docker run --rm -it -v $$(pwd):/app -v $(HOME)/.aws:/root/.aws snapshots /bin/bash

test: build
	docker run --rm -it -v $$(pwd):/app snapshots python -m unittest discover
