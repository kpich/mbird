.PHONY: install_precommit_hooks
install_precommit_hooks:
	pip install pre-commit
	pre-commit install

.PHONY: install
install:
	cd data && make install
	cd audiogen && make install
	cd console && make install
	cd diffusion && make install

.PHONY: dev
dev:
	cd data && make dev
	cd audiogen && make dev
	cd console && make dev
	cd diffusion && make dev

.PHONY: test
test:
	cd data && make test
	cd audiogen && make test
	cd console && make test
	cd diffusion && make test

.PHONY: mypy
mypy:
	cd data && make mypy
	cd audiogen && make mypy
	cd console && make mypy
	cd diffusion && make mypy
