import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:     %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


"""
Configuration Settings for the Application
This module loads environment variables using python-dotenv to configure various settings for the application.
"""

BASE_DIR = Path(__file__).resolve().parent
# Database Configuration:
# - DATABASE_URL (str): The URL for the application's database.
DATABASE_URL = os.environ.get("DATABASE_URL")

APP_ENV = os.environ.get('APP_ENV', 'DEV')

if APP_ENV.lower() in ['production', 'prod']:
    IS_PRODUCTION = True
else:
    IS_PRODUCTION = False


# Testing Configuration:
# - TEST (str): Configuration for testing purposes.
# - if set to True, a test database will be generated and auto populated
test = os.environ.get("TEST")


# Note:
# - Make sure to set the appropriate values in the corresponding environment variables
#   for the application to function correctly.
# - DEBUG should be set to 'TRUE' for debugging purposes and 'FALSE' for production.
debug = os.environ.get("DEBUG")
production = os.environ.get("PRODUCTION")

# Security Configuration:
# - SECRET_KEY (str): The secret key used for cryptographic operations.
# - ALGORITHM (str): The algorithm used for encoding and decoding JWT tokens.
# - ACCESS_TOKEN_EXPIRE_MINUTES (str): The expiration time for access tokens in minutes.
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")


#                   Email Configuration:
# - SENDGRID_API_KEY (str): The API key for the SendGrid service.
# - FROM_EMAIL (str): The default sender email address.
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")


#               Admin User Configuration:
# - USERNAME (str): The username for creating an admin user.
# - EMAIL (str): The email address for creating an admin user.
# - PASSWORD (str): The password for creating an admin user.

USERNAME = os.environ.get("USERNAME")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
FIRST_NAME = os.environ.get("FIRST_NAME")
LAST_NAME = os.environ.get("LAST_NAME")


# Environment Variables:
# - MEDIA_DIR (str): The directory for media files.
# - LOGGING_PATH (str): The path for logging.
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)
LOGGING_PATH = os.environ.get("LOGGING_PATH")


SSO_API_KEY: str = os.environ.get("SSO_API_KEY")
SSO_SECRET_KEY: str = os.environ.get("SSO_SECRET_KEY")
SSO_URL: str = os.environ.get("SSO_URL")
#  A list of allowed origins for Cross-Origin Resource Sharing (CORS).

# This list specifies the origins that are permitted to make cross-origin requests
# to the server. It is used in configuring CORS middleware to control access to
# resources from different domains.
# ALLOW_CREDENTIALS = True


LOCAL_ALLOWED_METHODS = ["*"]
LOCAL_ALLOWED_HOST = ["*"]
LOCAL_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3013",
    "https://afex-tickets.vercel.app",
]

# for production
PRODUCTION_ALLOWED_METHODS = [""]
PRODUCTION_ALLOWED_HOST = [""]
PRODUCTION_ORIGINS = [""]


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

PRODUCTION = False
DEBUG = False
TEST = False

if debug is not None:
    DEBUG = debug.lower() == "true"
    if DEBUG:
        logger.info(
            "DEBUG has been set to 'True': Endpoints will return server error messages"
        )
        logger.info(
            "Please ensure to set DEBUG to 'False' in your .env file after debugging"
        )


if production is not None:
    PRODUCTION = production.lower() == "true"

if test is not None:
    TEST = test.lower() == "true"
    if TEST:
        logger.info("'TEST' is set to True. A test database will be created")
        logger.info("Ensure to set 'TEST' to False in your .env file after testing")


if DEBUG:
    pass
else:
    pass

if PRODUCTION:
    logger.info(
        "'PRODUCTION' is set to True. Settings have been configured for a production development"
    )
    ALLOWED_HOST = PRODUCTION_ALLOWED_HOST
    ALLOWED_METHODS = PRODUCTION_ALLOWED_METHODS
    ALLOWED_ORIGINS = PRODUCTION_ORIGINS

else:
    logger.info(
        "'PRODUCTION' is set to False. Settings have been configured for a local development"
    )
    ALLOWED_HOST = LOCAL_ALLOWED_HOST
    ALLOWED_METHODS = LOCAL_ALLOWED_METHODS
    ALLOWED_ORIGINS = LOCAL_ORIGINS


TIME_ZONE = 'Africa/Lagos'
