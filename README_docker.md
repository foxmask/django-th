# Docker for Trigger Happy

This is a very very early stage for docker support
but this should do the trick until next time

## Build

```
docker-compose -f docker-compose.yml build
```

## Run

```
docker-compose -f docker-compose.yml up -d
```

## Database update/create

```
docker-compose -f docker-compose.yml run web  python manage.py migrate
docker-compose -f docker-compose.yml run web  python manage.py createsuperuser
```