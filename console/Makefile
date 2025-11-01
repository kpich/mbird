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

.PHONY: install_precommit_hooks
install_precommit_hooks:
	pip install pre-commit
	pre-commit install

.PHONY: mypy
mypy:
	mypy --check-untyped-defs src/mbird_console
