from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"

    database_url: str = "sqlite:///./data/calbell.db"

    openfoodfacts_base_url: str = "https://world.openfoodfacts.org/api/v2"
    openfoodfacts_user_agent: str = "CalBell/1.0 (self-hosted)"

    food_model_name: str = "nateraw/food"
    food_model_top_k: int = 3
    default_serving_grams: float = 150.0

    class Config:
        env_prefix = "CALBELL_"
        env_file = ".env"


settings = Settings()
