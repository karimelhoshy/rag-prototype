from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")

    # AWS
    aws_access_key_id: str = Field(default="", env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="", env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_s3_bucket: str = Field(default="", env="AWS_S3_BUCKET")

    # GCP
    gcp_project_id: str = Field(default="", env="GCP_PROJECT_ID")
    gcp_bucket_name: str = Field(default="", env="GCP_BUCKET_NAME")
    google_application_credentials: str = Field(default="", env="GOOGLE_APPLICATION_CREDENTIALS")

    # Azure
    azure_storage_connection_string: str = Field(default="", env="AZURE_STORAGE_CONNECTION_STRING")
    azure_container_name: str = Field(default="", env="AZURE_CONTAINER_NAME")

    # Vector DB
    chroma_persist_directory: str = Field(default="./chroma_db", env="CHROMA_PERSIST_DIRECTORY")
    collection_name: str = Field(default="documents", env="COLLECTION_NAME")

    # Embedding
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL")

    # LLM
    llm_model: str = Field(default="gpt-3.5-turbo", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
