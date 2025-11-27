from pydantic_settings import BaseSettings as PydanticBaseConfig


class BaseConfig(PydanticBaseConfig):
    class Config:
        env_file = ".env"


class AppConfig(BaseConfig):
    secret_key: str = "secret_key"
    debug: bool = True

    class Config:
        env_prefix = "APP_"


app_config = AppConfig()


class PostgresConfig(BaseConfig):
    username: str = "postgres"
    password: str = "postgres"
    database: str = "database"
    host: str = "localhost"
    port: int = 5432
    pool_size: int = 10
    max_overflow: int = 5
    echo: bool = (
        False  # True means write sql queries in std.out. Set False in production.
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    class Config:
        env_prefix = "POSTGRES_"


postgres_config = PostgresConfig()


class RedisConfig(BaseConfig):
    host: str = "localhost"
    port: int = 6379
    database: str = "shop"
    max_connections: int = 10
    decode_responses: bool = True

    @property
    def redis_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.database}"

    class Config:
        env_prefix = "REDIS_"


redis_config = RedisConfig()


class MongoConfig(BaseConfig):
    host: str = "localhost"
    port: int = 27017
    username: str = "mongo"
    password: str = "mongo"

    @property
    def mongo_url(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"

    class Config:
        env_prefix = "MONGO_"


mongo_config = MongoConfig()
