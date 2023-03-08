from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fistbump import schemas
from fistbump.helpers import DB_user, local_now, tinydb_set
from fistbump.config import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_password(plain_password, hashed_password) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password) -> str:
#     return pwd_context.hash(password)


# async def authenticate_user(username: str, password: str):
#     user = await get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


async def get_user(user_id: int) -> schemas.User:
    async with DB_user as db:
        user = db.get(doc_id=user_id)
    return schemas.User(id=user.doc_id, **user)


def create_access_token(user_id: int):
    encoded_jwt = jwt.encode({"sub": user_id}, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user():
    # create in db
    async with DB_user as db:
        doc_id = db.insert({"last_access": local_now().isoformat()})
    return create_access_token(user_id=doc_id)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    """
    FastAPI dependency to use on authenticated endpoints.

    Returns the schemas.User of the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user


async def authenticated_user(token: str = Depends(oauth2_scheme)) -> int:
    """
    FastAPI dependency to use on authenticated endpoints.

    Returns the user_id of the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        user_id_str: Optional[str] = decoded.get("sub")
        if user_id_str is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_id = int(user_id_str)
    # log last_access
    async with DB_user as db:
        db.update(tinydb_set("last_access", local_now().isoformat()), doc_ids=[user_id])
    return user_id
