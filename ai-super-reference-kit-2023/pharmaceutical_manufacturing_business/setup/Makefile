SHELL := /bin/bash # Use bash syntax

install-python:
	sudo apt install software-properties-common
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt install python3.9
	sudo apt install python3-pip

install-python-packages:
	pip install pandas numpy

install-dockertools:
	sudo apt-get update
	sudo apt install docker.io
	sudo apt  install docker-compose
	sudo gpasswd -a $(USER) docker
	newgrp docker

install-tools: install-python install-python-packages install-dockertools

setup-store-full:
	# create model stores
	mkdir -p ../store/models/{supportbot_chatbot,medication_demand_forecast,medication_qaqc,robot_maintenance}
	# create data stores
	mkdir -p ../store/datasets/{supportbot_chatbot,medication_demand_forecast,medication_qaqc,robot_maintenance}
	# create output stores
	mkdir -p ../store/outputs/{supportbot_chatbot,medication_demand_forecast,medication_qaqc,robot_maintenance}

setup-store-slim:
	# create model stores
	mkdir -p ../store/models/{medication_demand_forecast,robot_maintenance}
	# create data stores
	mkdir -p ../store/datasets/{medication_demand_forecast,robot_maintenance}
	# create output stores
	mkdir -p ../store/outputs/{medication_demand_forecast,robot_maintenance}

create-synthethic-data:
	python3 ../medication_demand_forecast/src/utils/generate_data.py --save_path '../store/datasets/medication_demand_forecast/'
	python3 ../robot_maintenance/src/utils/generate_data.py --save_path '../store/datasets/robot_maintenance/'

configure-pills-mvtec:
	cd ../store/datasets/medication_qaqc && \
	wget https://www.mydrive.ch/shares/43421/11a215a5749fcfb75e331ddd5f8e43ee/download/420938129-1629953099/pill.tar.xz && \
	tar -xf pill.tar.xz && \
	mkdir -p data/{train/{good,bad},test/{good,bad},blind/} && \
	cd pill/train/good/ && \
	cp `ls | head -n 210` ../../../data/train/good/ && \
	cp `ls | tail -n 65` ../../../data/test/good/ && \
	cd ../../../ && \
	cd pill/test/combined && \
	cp `ls | head -n 17` ../../../data/train/bad/ && \
	cp `ls | tail -n 5` ../../../data/test/bad/ && \
	cd ../../../ && \
	cd pill/test/combined && \
	cp `ls | head -n 50` ../../../data/blind/ && \
	cd ../../../ && \
	rm pill.tar.xz

launch-full: setup-store-full create-synthethic-data configure-pills-mvtec
	docker-compose -f docker-compose-full.yaml -p full up

launch-slim: setup-store-slim create-synthethic-data
	docker-compose -f docker-compose-slim.yaml -p slim up

shutdown-full:
	docker-compose -f docker-compose-full.yaml -p full down

shutdown-slim:
	docker-compose -f docker-compose-slim.yaml -p slim down
