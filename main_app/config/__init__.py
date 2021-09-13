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

	class Config:
		env_file = ".env"

@lru_cache()
def get_settings():
	print('execute get_settings function')
	return Settings()

settings = get_settings()
