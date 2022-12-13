from pydantic import BaseSettings


class Settings(BaseSettings):
    ML_MODULE_NAME: str = ''

    class Config:
        case_sensitive = True
        frozen = True
        env_nested_delimiter = "__"

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
