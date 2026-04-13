from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    SECRET_KEY: str = "fallback-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/library_management"
    DATABASE_URL_SYNC: str = "postgresql://user:password@localhost:5432/library_management"
 
    class Config:
        env_file = ".env"
 
 
settings = Settings()