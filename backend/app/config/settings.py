from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the Library Management System.
    
    This class uses Pydantic's BaseSettings to automatically load environment variables
    and validate them against the defined types. The configuration is loaded from a .env file
    in the project root directory.
    """

    # Application settings
    APP_NAME: str = "Library Management System"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging settings
    LOG_LEVEL: str = "INFO"

    class Config:
        """
        Pydantic configuration to load environment variables from a .env file.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()