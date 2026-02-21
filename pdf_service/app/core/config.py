from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings.
    Loads variables from environment or .env file.
    """

    # --- AWS / Localstack Configuration ---
    AWS_ENDPOINT_URL: str = Field(
        default="http://localstack:4566",
        description="URL for AWS services. Use http://localstack:4566 for local development."
    )
    AWS_ACCESS_KEY_ID: str = Field(
        default="test",
        description="AWS access key. Can be any string for Localstack."
    )
    AWS_SECRET_ACCESS_KEY: str = Field(
        default="test",
        description="AWS secret key. Can be any string for Localstack."
    )
    AWS_DEFAULT_REGION: str = Field(
        default="us-east-1",
        description="Default AWS region for SQS and S3 services."
    )

    SQS_QUEUE_NAME: str = Field(
        default="pdf-tasks",
        description="Name of the SQS queue for PDF generation tasks."
    )
    S3_BUCKET_NAME: str = Field(
        default="user-pdfs",
        description="Name of the S3 bucket where generated PDFs are stored."
    )

    # --- JWT Authentication Settings ---
    SECRET_KEY: str = Field(
        default="SECRET_KEY",
        description="Secret key used for signing JWT tokens")
    ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm used for JWT encryption")

    class Config:
        """
        Pydantic config for loading environment variables.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
