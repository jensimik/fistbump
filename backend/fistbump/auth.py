import os
from hashlib import scrypt
from typing import Optional
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fistbump.config import settings

SHARE_WHITELIST: set[str] = set()

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_swagger", auto_error=False)


def hash_password(password, salt=None) -> tuple[str, str]:
    if not salt:
        salt = os.urandom(64).hex()
    return (
        scrypt(
            password=password.encode(), salt=salt.encode(), n=1 << 14, r=8, p=1
        ).hex(),
        salt,
    )


def verify_password(hashed_password, guessed_password, salt) -> bool:
    """
    Verifies if a password is valid by checking a hashed password with a salt
    """
    return hashed_password == hash_password(guessed_password, salt)[0]


def create_access_token(data: dict) -> str:
    """
    Encodes an access token with the given data.
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def register_user():
    """
    Registers a new anon user with just a random UUID for now.

    Can be extended to take username/password etc. and also save the user in some kind of DB.
    """
    return create_access_token({"sub": str(uuid4())})


def authenticated_user(
    token: str = Depends(oauth2_scheme),
) -> UUID:
    """
    FastAPI dependency to use on authenticated endpoints.

    Returns the UUID of the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        user_uuid: Optional[str] = decoded.get("sub")
        if user_uuid is None:
            raise credentials_exception

        return UUID(user_uuid)

    except (jwt.exceptions.DecodeError, ValueError):
        raise credentials_exception