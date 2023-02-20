
from fastapi import APIRouter, Depends
from fistbump.auth import authenticated_user, register_user

from fistbump import schemas

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.AuthToken)
def register():
    return {"access_token": register_user(), "token_type": "bearer"}


@router.get("/me", dependencies=[Depends(authenticated_user)], response_model=schemas.Me)
def me(user = Depends(authenticated_user)):
    return {"uuid": user}