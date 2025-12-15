from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Business Project"
    VERSION: str = "1.0.0"

    # DB
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Optional WABA / extra envs (present in your .env but not required)
    WABA_VERIFY_TOKEN: str
    WABA_ACCESS_TOKEN: str
    PHONE_NUMBER_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
