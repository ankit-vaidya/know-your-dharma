from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_db: str = "know_your_dharma"
    postgres_user: str = "kyd_user"
    postgres_password: str

    redis_password: str

    keycloak_url: str = "http://localhost:8080"
    keycloak_realm: str = "know-your-dharma"
    keycloak_client_id: str = "kyd-api"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    @property
    def keycloak_issuer(self) -> str:
        return (
            f"{self.keycloak_url}"
            f"/realms/{self.keycloak_realm}"
        )

    @property
    def keycloak_jwks_url(self) -> str:
        return (
            f"{self.keycloak_issuer}"
            "/protocol/openid-connect/certs"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()