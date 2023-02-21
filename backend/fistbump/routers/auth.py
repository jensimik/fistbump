from fastapi import APIRouter, Depends
from fistbump.auth import authenticated_user, register_user

from fistbump import schemas

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register() -> schemas.Token:
    access_token = await register_user()
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me", dependencies=[Depends(authenticated_user)], response_model=schemas.Me
)
def me(user_id=Depends(authenticated_user)) -> schemas.Me:
    return schemas.Me(user_id=user_id)
