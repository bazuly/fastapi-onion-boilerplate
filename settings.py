from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str
    KAFKA_BOOTSTRAP_SERVERS: str = 'localhost:9092'
    KAFKA_TOPIC: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class DescriptionSettings(BaseSettings):
    PAGE_DESCRIPTION: str = "Page number, starts with one"
    SIZE_DESCRIPTION: str = "Amount elements on the page"


settings = Settings()
