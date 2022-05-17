
## Local development

1. set up local environment

- create .env file at the project root, the same folder where manage.py is located
- add required variables to .env file like the example below:
```
DATABASE_name="bpmnus"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
```
2. Migrate database
### ```python manage.py migrate```
3. Start project
### ```python manage.py runserver```



----
----
----




docker.exe build . -t bpmnus 

