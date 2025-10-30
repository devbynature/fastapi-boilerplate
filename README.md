# fastapi-boilerplate
FastAPI, SQLModel, Alembic, Redis, JWT, UV

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
