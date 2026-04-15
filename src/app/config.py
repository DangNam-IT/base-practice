from pydantic_settings import BaseSettings, SettingsConfigDict
 
 
class Settings(BaseSettings):
    SECRET_KEY: str = "fallback-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://bookstore_user:bookstore_pass@localhost:5432/library_management"
    DATABASE_URL_SYNC: str = "postgresql://bookstore_user:bookstore_pass@localhost:5432/library_management"
    # Application
    APP_NAME: str = "Library Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool=True
    model_config = SettingsConfigDict(env_file=".env")
 
 
settings = Settings()