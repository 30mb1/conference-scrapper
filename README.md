# conference-scrapper

## Installing dependencies
Install docker and docker-compose:
```bash
chmod +x shell_helpers/*
sudo ./shell_helpers/install.sh
```
Build docker images:
```bash
# development version, build main image (django) from scratch
# django uses dev web-server
sudo docker-compose build

# for production, use prebuilt image with some initial data installed in image
# django uses nginx + gunicorn
sudo docker-compose -f docker-compose.prod.yml pull
```

## Run app
#### Data installation
Before first run, you should upload data to application db.
Initially, production version has some data included in image and development version doesn't.
To upload data to db, place it in data directory of application and run:
```bash
# add -f docker-compose.prod.yml if production
sudo docker-compose run --rm django python manage.py load_data
```
Prepared data for production is placed in image already, so that to upload it, run:
```bash
sudo docker-compose -f docker-compose.prod.yml  run --rm django python manage.py load_data use_prepared
```
Set up database:
```bash
(-f docker-compose.prod.yml if production)
sudo docker-compose run --rm django python manage.py migrate
```

#### Starting containers
To start containers use:
```bash
# for development
sudo docker-compose up -d

# and for production
sudo docker-compose -f docker-compose.prod.yml up -d
```
Now you can go to browser and explore application:
```bash
# development version
127.0.0.1:8000

# production version
0.0.0.0
```

## Managing data with admin interface
Django have powerful tools that allows us creating flexible and easy to use admin interface. 
We have set up several for managing scrapped conferences and modify their links (edges).
To use it, first of all, create superuser:
```bash
# add -f docker-compose.prod.yml if it is production
sudo docker-compose run --rm django python manage.py createsuperuser
>> enter credentials
```
Now go to *127.0.0.1/admin*, login and have fun. (replace 127.0.0.1 for appropriate url if production)
