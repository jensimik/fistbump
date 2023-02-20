import os

from hashlib import scrypt
from typing import Optional


import jwt

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
SHARE_WHITELIST: set[str] = set()

ALGORITHM = "HS256"
JWT_SECRET = "abc"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_swagger", auto_error=False)


def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(64).hex()
    return (
        scrypt(
            password=password.encode(), salt=salt.encode(), n=1 << 14, r=8, p=1
        ).hex(),
        salt,
    )


def verify_password(hashed_password, guessed_password, salt, maxtime=0.5) -> bool:
    return hashed_password == hash_password(guessed_password, salt)[0]


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def register_user():
    return create_access_token({"sub": str(uuid4())})

def authenticated_user(
    token: str = Depends(oauth2_scheme),
) -> tuple[int, dict]:
    """
    FastAPI dependency to use on authenticated endpoints
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: Optional[int] = decoded.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.exceptions.DecodeError:
        raise credentials_exception

    return user_id