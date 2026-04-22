from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN_ENDPOINT = os.getenv("LOGIN_ENDPOINT")
REGISTER_ENDPOINT = os.getenv("REGISTER_ENDPOINT")
MOVIE_BASE_URL = os.getenv("MOVIE_BASE_URL")
MOVIES_ENDPOINT = os.getenv("MOVIES_ENDPOINT")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")

if not SUPER_ADMIN_EMAIL or not SUPER_ADMIN_PASSWORD:
    raise ValueError("SUPER_ADMIN_EMAIL or SUPER_ADMIN_PASSWORD is not set.")
