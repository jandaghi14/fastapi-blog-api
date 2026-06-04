from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


from app.core.config import settings_jwt
from app.models.model_user import User

EXPIRE_ACCESS_TIME = settings_jwt.JWT_DEFAULT_TIME_EXPIRE
SECRET_KEY = settings_jwt.JWT_SECRET_KEY
ALGORITHM = settings_jwt.JWT_ALGORITHM


class Token:

    def create_access_token(self, user_object: User, delta_time: timedelta | None = None):
        try:
            payload = {
                'sub': user_object.username,
                'exp': datetime.now(timezone.utc) + (delta_time if delta_time is not None else timedelta(minutes=int(EXPIRE_ACCESS_TIME)))
            }
            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except JWTError as i:
            raise JWTError(f"Failure in creating token: {i}")

    def decode_token_access(self, token):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
