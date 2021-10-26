from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
	app_name: str = "Some food delivery"
	JWT_SECRET_KEY: str = None
	JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
	JWT_SESSION_KEY: str = None
	JWT_SESSION_TOKEN_EXPIRE_MINUTES: int = 1
	JWT_ALGORITHM: str = "HS256"
	DB_URL: str = None
	DB_NAME: str = None
	DEBUG_MODE: bool = True
	base_static_url: str = ""
	telegram_notif_group_id: str = None
	telegram_bot_username: str = None
	telegram_bot_token: str = None

	class Config:
		env_file = '.env'

@lru_cache()
def get_settings(env_file: str = '.env'):
	return Settings(_env_file = env_file)

settings = get_settings()
