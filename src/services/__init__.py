from services.redis.service import RedisService
from services.postgres.service import PostgresService


class Services:
    redis: RedisService = RedisService()
    postgres: PostgresService = PostgresService()
