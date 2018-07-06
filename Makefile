build:
	docker build -t snapshots:latest .

sh: build
	docker run --rm -it -v $$(pwd):/app -v $(HOME)/.aws:/root/.aws snapshots /bin/bash
