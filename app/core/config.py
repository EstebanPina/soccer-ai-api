import os
from pydantic import Field, Extra
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    JWT_SECRET: str = Field(..., env="JWT_SECRET_KEY")
    JWT_REFRESH_SECRET: str = Field(..., env="JWT_REFRESH_SECRET_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    # URL de la base de datos
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TEST_USER:str=Field(..., env="TEST_USER")
    TEST_PASSWORD:str=Field(..., env="TEST_PASSWORD")

    class Config:
        env_file = ".env"
        extra = Extra.allow # Define que las variables de entorno se leen desde el archivo .env

# Instanciamos los settings
settings = Settings()
