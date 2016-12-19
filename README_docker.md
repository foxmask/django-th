# Docker for Trigger Happy

This is a very very early stage for docker support
but this should do the trick until next time

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
docker-compose run web  python manage.py migrate
docker-compose run web  python manage.py createsuperuser
```
