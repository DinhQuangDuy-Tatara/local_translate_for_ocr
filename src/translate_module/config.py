from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRANSLATE_", env_file=".env", extra="ignore")
    host: str = "127.0.0.1"
    port: int = 8765
    default_target: str = "vi"
    max_text_length: int = 10000
    log_level: str = "info"
