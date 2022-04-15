import datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from typing import Dict
from secrets import token_urlsafe

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

# token reqirements
SECRET_KEY = token_urlsafe(64)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


class Hash:
    @staticmethod
    def hash_password(password: str) -> str:
        return PWD_CONTEXT.hash(password)

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(password, hashed_password)


class JWT:
    @staticmethod
    def create(data: Dict):
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() +\
            datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials!",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str | None = payload.get('sub')
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
