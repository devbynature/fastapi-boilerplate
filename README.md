# fastapi-boilerplate
FastAPI, SQLModel, Alembic, Redis, UV

NOTE: import new models in apps/\_\_init\_\_.py to make alembic migration files.

make migrations command:
```shell
cd src
alembic -c alembic.ini revision --autogenerate -m "init"
```

migrate command:
```shell
cd src
alembic -c alembic.ini upgrade head
```
