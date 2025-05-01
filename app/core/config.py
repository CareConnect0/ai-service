from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    google_application_credentials: str  
    jwt_secret_key: str 
    jwt_algorithm: str 
    jwt_issuer: str 
    springboot_url: str 
    openai_api_key: str

settings = Settings()
