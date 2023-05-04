from os import environ as env
from secrets import token_urlsafe
from dotenv import load_dotenv

load_dotenv()

TEMPLATES_AUTO_RELOAD = True
DEBUG = 1 == env.get("DEBUG", 1)
QUART_ENV = env.get("QUART_ENV", "development")
SECRET_KEY = env.get("SECRET_KEY", token_urlsafe(12))
QUART_AUTH_DURATION = 60 * 60    # 1 hour

# LWS
LWS_URL = env.get("LWS_URL", "http://127.0.0.1:8080")
LWS_ADMIN_URL = env.get("LWS_ADMIN_URL", "http://127.0.0.1:8081")