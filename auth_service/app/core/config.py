from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings and environment variables loader.
    Uses pydantic-settings to automatically parse .env files.
    """

    # --- PostgreSQL Database Settings ---
    POSTGRES_USER: str = Field(..., description="Username for PostgreSQL")
    POSTGRES_PASSWORD: str = Field(..., description="Password for PostgreSQL")
    POSTGRES_DB: str = Field(..., description="Database name")
    POSTGRES_HOST: str = Field(..., description="Database host (e.g., 'localhost' or service name in Docker)")
    POSTGRES_PORT: int = Field(5432, description="Database port")

    # --- JWT Authentication Settings ---
    SECRET_KEY: str = Field(..., description="Secret key used for signing JWT tokens")
    ALGORITHM: str = Field("HS256", description="Algorithm used for JWT encryption")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Token lifetime in minutes")

    @property
    def async_database_url(self) -> str:
        """
        Constructs the asynchronous SQLAlchemy database URL.
        Required for asyncpg driver as per project specifications.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        """
        Pydantic config for loading environment variables.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()