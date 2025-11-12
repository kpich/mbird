.PHONY: dev
dev:
	cd ../data && pip install -e '.[dev,test]'
	pip install -e '.[dev,test]'

.PHONY: install
install:
	cd ../data && pip install -e .
	pip install -e .

.PHONY: test
test:
	pytest .

.PHONY: clean
clean:
	find src/ -name "__pycache__" | xargs rm -r
	rm -r ./build/

.PHONY: mypy
mypy:
	mypy --check-untyped-defs src/mbird_diffusion
