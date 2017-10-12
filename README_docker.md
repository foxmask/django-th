# Docker for Trigger Happy

This is very very early stage for docker support
but this should do the trick until next time, based on https://docs.docker.com/engine/reference/commandline/build/ and https://docs.docker.com/compose/django/ and a bit of https://hub.docker.com/_/django/

## Build

```
docker-compose build
```

## Run

```
docker-compose up 
```

## Database update/create

```
docker-compose run web  python manage.py migrate --settings=django_th.settings_docker
docker-compose run web  python manage.py createsuperuser --settings=django_th.settings_docker
```


## Running tasks

2 tasks are usually in the crontab: one to read the data source, one to publish the grabbed data:

```
docker-compose run web  python manage.py read --settings=django_th.settings_docker
docker-compose run web  python manage.py publish --settings=django_th.settings_docker
```
