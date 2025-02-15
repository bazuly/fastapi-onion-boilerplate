from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"
    KAFKA_BOOTSTRAP_SERVERS: str = 'kafka:19092'
    KAFKA_TOPIC: str = "applications"
    IMAGE_UPLOAD_DIR: str = "uploads/images"

    # -------------------------------------------------------------------
    # for work with .env files we can use pydantic, like on our example,
    # or we can use python_dotenv
    # -------------------------------------------------------------------
    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class DescriptionSettings(BaseSettings):
    PAGE_DESCRIPTION: str = "Page number, starts with one"
    SIZE_DESCRIPTION: str = "Amount elements on the page"


settings = Settings()
