.PHONY: install_precommit_hooks
install_precommit_hooks:
	pip install pre-commit
	pre-commit install

.PHONY: test
test:
	cd data && make test
	cd console && make test

.PHONY: mypy
mypy:
	cd data && make mypy
	cd console && make mypy
