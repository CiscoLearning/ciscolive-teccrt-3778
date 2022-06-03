SHELL := /bin/bash

setup: 
	if [[ ! -d netbox-docker ]]; then git clone -b release https://github.com/netbox-community/netbox-docker.git; else cd netbox-docker && git pull; fi
	cp netbox-configs/docker-compose.override.yml netbox-docker/
	cd netbox-docker && docker-compose pull

startup:
	cd netbox-docker && docker-compose up -d

shutdown: 
	cd netbox-docker && docker-compose down

clean: 
	cd netbox-docker && docker-compose down -v 

netbox-logs: 
	cd netbox-docker && docker-compose logs -f netbox