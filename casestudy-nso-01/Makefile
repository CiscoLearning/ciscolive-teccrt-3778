SHELL := /bin/bash

setup: setup-netsim setup-nso 
start: setup start-apps syncfrom
clean: clean-nso clean-netsim 

start-apps: start-netsim start-nso check-nso-up
stop-apps: stop-netsim stop-nso

source-nso: 
	source ~/nso/ncsrc 

setup-nso: source-nso
	ncs-setup --package ~/nso/packages/neds/cisco-ios-cli-6.77 --dest .

clean-nso: source-nso stop-nso
	rm -rf logs/ ncs-cdb/ packages/ scripts/ state/ ncs.conf README.ncs target/ storedstate

start-nso: 
	ncs

check-nso-up: 
	echo "Waiting for NSO to be available"
	while :; do curl -sSf -o /dev/null -u admin:admin http://localhost:8080/.well-known/host-meta && break; sleep 5; done

stop-nso: source-nso
	-ncs --stop 

syncfrom:  
	curl -X POST -u admin:admin http://localhost:8080/restconf/data/tailf-ncs:devices/sync-from

setup-netsim: source-nso 
	ncs-netsim create-network cisco-ios-cli-6.77 2 ios-

clean-netsim: source-nso stop-netsim
	rm -rf netsim/ README.netsim

start-netsim: source-nso 
	ncs-netsim start 

stop-netsim: 
	-ncs-netsim -a stop