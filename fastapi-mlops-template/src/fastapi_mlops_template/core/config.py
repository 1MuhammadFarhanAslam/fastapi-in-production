class Settings:
    APP_NAME: str = "FastAPI MLOps Template"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "mlops_db"


settings = Settings()