from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = "AIzaSyApuGrHA2CwLB2X7x9mfb9LprhhjPTjz-M"

    class Config:
        env_file = ".env"
        extra = "allow"  # ✅ this allows extra keys like database_url, secret_key

settings = Settings()
