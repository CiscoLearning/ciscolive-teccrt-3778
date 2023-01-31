SHELL := /bin/bash

start: setup startup-netbox check-netbox-up run_initializer device-types-setup device-creation

setup: 
	echo "Preparing to run netbox-docker"
	if [[ ! -d netbox-docker ]]; then git clone -b release https://github.com/netbox-community/netbox-docker.git; else cd netbox-docker && git pull; fi
	cp netbox-configs/docker-compose.override.yml netbox-docker/
	cp netbox-configs/Dockerfile-Plugins netbox-docker/
	cp netbox-configs/plugin_requirements.txt netbox-docker/
	cp netbox-configs/plugins.py netbox-docker/configuration/
	cp -r netbox-configs/demo-initializers netbox-docker/
	cp netbox-configs/000_users.py netbox-docker/startup_scripts
	cd netbox-docker && docker-compose build --no-cache && docker-compose pull

startup-netbox:
	echo "Starting netbox-docker"
	cd netbox-docker && docker-compose up -d

check-netbox-up: 
	echo "Waiting for NetBox to be available"
	while :; do curl -sSf -o /dev/null http://localhost:8000 && break; sleep 5; done

shutdown: 
	echo "Shutting down netbox-docker, but saving the state"
	cd netbox-docker && docker-compose down

clean: 
	echo "Shutting down and deleting netbox-docker state"
	cd netbox-docker && docker-compose down -v 
	rm netbox-docker/docker-compose.override.yml 
	rm -rf netbox-docker/demo-initalizers 

netbox-logs: 
	cd netbox-docker && docker-compose logs -f netbox

device-types-setup: 
	echo "Creating NetBox Device-Types for Cisco gear"
	docker pull ghcr.io/minitriga/netbox-device-type-library-import
	docker run --rm --name netbox-devicetypes-import \
		-e "NETBOX_URL=http://netbox:8080/" \
		-e "NETBOX_TOKEN=0123456789abcdef0123456789abcdef01234567" \
		-e "VENDORS=cisco" \
		--network netbox-docker_default \
		ghcr.io/minitriga/netbox-device-type-library-import

device-refresh: device-clean device-creation

device-creation: 
	echo "Creating sample network switches for demo"
	netbox-configs/device_creation.py 

device-clean: 
	echo "Deleteing all network devices from NetBox"
	netbox-configs/device_clean.py 

run_initializer:
	@echo "\n== Initializing NetBox with starting data"
	cd netbox-docker && docker-compose exec netbox ./manage.py load_initializer_data --path /opt/netbox/initializer_data