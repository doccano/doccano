THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: clean
clean:
	rm -rf build/ dist/ .eggs/
	find . -iname '*.pyc' -o -iname '__pycache__' | xargs rm -rf
	docker-compose -p doccano rm -fsv || true

.PHONY: ensure-venv
ensure-venv:
	@ [ "x${VIRTUAL_ENV}" != "x" ] || ( echo 'Please activate your venv using "source ./.venv/bin/activate"'; exit 1 )

.PHONY: setup-local
setup-local: ensure-venv
	[ -d /Applications/Docker.app ] || brew cask install docker
	which docker &>/dev/null || brew install docker
	which docker-compose &>/dev/null || brew install docker-compose
	which nvm &>/dev/null || source /usr/local/opt/nvm/nvm.sh &>/dev/null; nvm install lts/*
	( \
		set -e; \
		pip install -r requirements.txt; \
	)
	collect-static

.PHONY: collect-static
collect-static:
	@ cd ./app/; python manage.py collectstatic

.PHONY: create-admin
create-admin:
	@ ./tools/env.sh ./tools/create-admin.sh

.PHONY: update-images
update-images:
	docker-compose -p doccano pull

.PHONY: docker-start
docker-start:
	@ docker-compose -p doccano up -d

.PHONY: docker-stop
docker-stop:
	@ docker-compose -p doccano rm -fsv

.PHONY: docker-restart
docker-restart: docker-stop docker-start

.PHONY: test-local
test-local:
	@ cd ./app/; python manage.py test server.tests

.PHONY: run-local
run-local: ensure-venv docker-start
	@ cd ./app; ../tools/env.sh python manage.py runserver

.PHONY: migrate
migrate:
	@ cd ./app; python manage.py migrate
