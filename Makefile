build:
	docker build -t cleaner:latest .

sh: build
	docker run --rm -it -v $$(pwd):/app -v $(HOME)/.aws:/root/.aws cleaner /bin/bash

test: build
	docker run --rm -it -v $$(pwd):/app cleaner python -m unittest discover

clean: build
	docker run --rm -it -v $$(pwd):/app -v $(HOME)/.aws:/root/.aws cleaner python ./index.py -type=snapshot -filters='[{"Name": "tag:Name", "Values": [ "kubernetes-dynamic-pvc*"]}]' -age=60 -dryrun=false
