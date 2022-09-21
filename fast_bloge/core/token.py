import enum
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from jose import JWTError, constants
from jose import jwt
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from fast_bloge.core.config import get_settings
from .config import Settings

role_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Operation not permitted",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate request token",
    headers={"WWW-Authenticate": "Bearer"},
)


class Role(enum.Enum):
    user = 'USER'
    admin = 'ADMIN'


class Auth(BaseModel):
    user_id: int
    kyc_level: int = 0
    phone_number: str = ""
    email: Optional[str] = ""
    user_type: str

    def __json__(self, **options):
        return self.json()


def auth_required(permissions):
    def outer_wrapper(function):
        @wraps(function)
        def inner_wrapper(*args, **kwargs):
            if 'user' in kwargs:
                if kwargs['user'].user_type in permissions:
                    return function(*args, **kwargs)
                else:
                    raise role_exception
            else:
                raise forbidden_exception

        return inner_wrapper

    return outer_wrapper


def get_current_user(request: Request, settings: Settings = Depends(get_settings)) -> Union[Auth, None]:
    if 'authorization' in request.headers:

        try:
            key = settings.jwt_pubkey
            tkn = request.headers['Authorization'].split(' ')[1]
            payload = jwt.decode(tkn, key,
                                 algorithms=[constants.ALGORITHMS.ES256, ])
            username: str = payload.get("user_id")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = payload
        if user is None:
            raise credentials_exception
        return Auth(user_id=payload['user_id'], kyc_level=payload['kyc_level'],
                    email=payload['email'], phone_number=payload['phone_number'], user_type=payload['user_type'])
    return None


api_key_header = APIKeyHeader(name="X-service-key", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == get_settings().api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


oath2_schema = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'fe0b42c7207f0f15090293b0aa2a15be7f236c35901b962820d0979db88c7cac'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRED_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
