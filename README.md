# tradesman project 


This is a project that will allow tradesman to quote for projects regular users will publish

## NB: This project is in development 

## requirements

- redis
- django
- python3
 
## useful commands
- to run celery on dev env
```bash
celery -A mon.celery worker -l DEBUG -E
```

- to run the django project 
```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.