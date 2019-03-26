#!/bin/sh

mkdir data
sudo docker-compose -f docker-compose.prod.yml pull
sudo docker-compose -f docker-compose.prod.yml run --rm django python manage.py migrate
sudo docker-compose -f docker-compose.prod.yml run --rm django python manage.py load_data use_prepared
sudo docker-compose -f docker-compose.prod.yml up -d