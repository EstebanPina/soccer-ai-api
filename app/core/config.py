import os
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    JWT_SECRET: str = Field(..., json_schema_extra="JWT_SECRET_KEY")
    JWT_REFRESH_SECRET: str = Field(..., json_schema_extra="JWT_REFRESH_SECRET_KEY")
    OPENAI_API_KEY: str = Field(..., json_schema_extra="OPENAI_API_KEY")

    # URL de la base de datos
    DATABASE_URL: str = Field(..., json_schema_extra="DATABASE_URL")
    TEST_USER:str=Field(..., json_schema_extra="TEST_USER")
    TEST_PASSWORD:str=Field(..., json_schema_extra="TEST_PASSWORD")

    model_config=ConfigDict(
        env_file=".env",  # Especifica el archivo .env
        env_file_encoding="utf-8"  # Encoding del archivo
    )
# Instanciamos los settings
settings = Settings()
