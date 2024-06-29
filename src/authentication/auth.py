import traceback
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, Request, status, WebSocket, WebSocketException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.authentication import AuthenticationBackend, AuthenticationError

from src.accounts.models import User
from src.management.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Defining an OAuth2 password bearer schema for token authentication
oauth2_schema = HTTPBearer()

# Creating a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


# Defining a Pydantic model for the Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Defining a Pydantic model for the TokenData
class TokenData(BaseModel):
    email: str | None = None


def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_schema)):
    """
    Get the current user based on the provided JWT token.
    This function decodes the JWT token using the secret key and verifies the user's credentials.
    Parameters:
        token (str): The JWT token for authentication.
    Raises:
        HTTPException:
            - If the token cannot be decoded or is invalid.
            - If the username retrieved from the token is None.
            - If the user does not exist in the system.
    Returns:
        User: An instance of the User model representing the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    try:
        user = User.valid_objects.get(email=token_data.email)
        return user
    except User.DoesNotExist:
        raise credentials_exception


def hash_password(password):
    """This hash password into another format"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class JWTAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """

    invalid_token_error = "Invalid or expired token."

    @classmethod
    async def authenticate(
        cls,
        request: Request = None,
        token: HTTPAuthorizationCredentials = Depends(oauth2_schema),
    ):
        # This function is inherited from the base class and called by some other class

        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            # token = token.credentials
            if scheme.lower() != "bearer":
                return None
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (ValueError, UnicodeDecodeError, JWTError) as exc:
            raise AuthenticationError(cls.invalid_token_error)

        email: str = payload.get("sub")
        if email is None:
            raise AuthenticationError(cls.invalid_token_error)

        try:
            user = User.valid_objects.get(email=email)
            # return user
        except User.DoesNotExist:
            raise AuthenticationError(cls.invalid_token_error)

        return auth, user
