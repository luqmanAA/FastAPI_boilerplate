from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional, Any

from jose import jwt, JWTError
from starlette.authentication import AuthenticationError

from src.management import settings


class Token:
    invalid_token_error = "Token is invalid or expired"
    SECRET_KEY = settings.ACCESS_TOKEN_SETTINGS['SECRET_KEY']
    ALGORITHM = settings.ACCESS_TOKEN_SETTINGS['ALGORITHM']

    def __init__(self, token=None):
        self.current_time = datetime.now()
        self.lifetime = timedelta(hours=settings.ACCESS_TOKEN_SETTINGS['LIFETIME_IN_HOURS'])
        if token:
            try:
                self.payload = jwt.decode(
                    token,
                    self.SECRET_KEY,
                    algorithms=self.ALGORITHM
                )
            except (ValueError, UnicodeDecodeError, JWTError):
                raise AuthenticationError(self.invalid_token_error)

        else:
            self.payload = {}
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

    def __str__(self) -> str:
        return jwt.encode(
            self.payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def __setitem__(self, key: str, value: Any) -> None:
        self.payload[key] = value

    def get(self, key: str) -> Any:
        return self.payload.get(key)

    def set_exp(
            self,
            claim: str = "exp",
            from_time: Optional[datetime] = None,
            lifetime: Optional[timedelta] = None
    ) -> None:
        if from_time is None:
            from_time = self.current_time

        if lifetime is None:
            lifetime = self.lifetime

        exp_date_time = from_time + lifetime
        self.payload[claim] = timegm(exp_date_time.utctimetuple())

    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, settings.ACCESS_TOKEN_SETTINGS.get('USER_ID_FIELD'))
        if not isinstance(user_id, str):
            user_id = str(user_id)

        token = cls()
        token[settings.ACCESS_TOKEN_SETTINGS.get('USER_ID_CLAIM')] = user_id
        return token
