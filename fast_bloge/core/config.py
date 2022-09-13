from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn

_env = None


class Settings(BaseSettings):
    sqlalchemy_database_url: PostgresDsn
    jwt_pubkey: str
    debug: bool
    port: str
    host: str
    origin: str
    service_name: str
    otel_server: str
    debug: bool = False
    api_key: str

    class Config:
        env_file = ".env_example"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
