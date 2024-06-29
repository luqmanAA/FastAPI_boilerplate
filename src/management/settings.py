import os
from dotenv import load_dotenv

load_dotenv()

MEDIA_DIR = os.environ.get("MEDIA_DIR")
DATABASE_URL = os.environ.get("DATABASE_URL")
DEBUG = os.environ.get("DEBUG")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
LOGGING_PATH = os.environ.get("LOGGING_PATH")

ACCESS_TOKEN_SETTINGS = {
    'USER_ID_CLAIM': 'user_id',
    'USER_ID_FIELD': 'id',
    'SECRET_KEY': os.environ.get('ACCESS_TOKEN_SECRET_KEY', ''),
    'ALGORITHM': os.environ.get('ACCESS_TOKEN_ALGORITHM', 'HS512'),
    'LIFETIME_IN_HOURS': int(os.environ.get('ACCESS_TOKEN_LIFETIME_HOURS', 12))
}
