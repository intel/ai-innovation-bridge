SHELL := /bin/bash # Use bash syntax

install-dockertools:
	sudo apt-get update
	sudo apt install docker.io
	sudo apt  install docker-compose
	sudo gpasswd -a $(USER) docker
	newgrp docker

setup-store:
	# create model stores
	mkdir -p ../store/models/supportbot_chatbot
	# create data stores
	mkdir -p ../store/datasets/supportbot_chatbot

launch-rag:
	docker-compose -f docker-compose-rag.yaml -p rag up

shutdown-rag:
	docker-compose -f docker-compose-rag.yaml -p rag down