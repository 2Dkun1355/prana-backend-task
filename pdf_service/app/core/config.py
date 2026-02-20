from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings.
    Loads variables from environment or .env file.
    """
    SECRET_KEY: str = Field("SECRET_KEY", description="Secret key used for signing JWT tokens")
    ALGORITHM: str = Field("HS256", description="Algorithm used for JWT encryption")

    class Config:
        """
        Pydantic config for loading environment variables.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
