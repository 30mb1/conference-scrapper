# conference-scrapper

## Set up project
Install docker and docker-compose:
```bash
chmod +x shell_helpers/*
sudo ./shell_helpers/install.sh
```
Build docker images:
```bash
# for development version (use django dev server)
sudo docker-compose build
# for production (use nginx + gunicorn)
sudo docker-compose -f docker-compose.prod.yml build
```

## Run app
Parse data and upload to db:
```bash
sudo docker-compose run --rm django python manage.py parse_data acm.json wikicfp.json
```
Start all containers:
```bash
sudo docker-compose (-f docker-compose.prod.yml if production) up -d
```
Now you can go to browser and explore application:
```bash
# development
127.0.0.1:8000
# production
0.0.0.0
```
