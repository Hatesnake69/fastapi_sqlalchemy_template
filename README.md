# fastapi_sqlalchemy_template

to run this project:
- ```cp .example.env .env```
- configure .env
- ```docker-compose up --build```

to run tests:
- ```docker exec -it app /bin/bash```
- ```pytest .```

to make migrations:
- configure alembic.ini file
- ```alembic revision --autogenerate -m "migration name"```
- ```alembic upgrade head```