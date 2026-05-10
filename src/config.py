from pydantic_settings import BaseSettings, SettingsConfigDict


# todo: add validation
class Settings(BaseSettings):
    postgres_user: str = "refvault"
    postgres_password: str = "refvault"
    postgres_db: str = "refvault"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    server_addr: str = "0.0.0.0"
    server_port: int = 8000
    reload: bool = True

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
