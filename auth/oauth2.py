from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

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


