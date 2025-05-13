from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_NAME: str = "your_database_name"

    SECRET_KEY: str  # Must be set in the .env file
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = False

    @property
    def DATABASE_URL(self) -> str:
        """Construct the database URL dynamically."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

# Instantiate the settings object
settings = Settings()
