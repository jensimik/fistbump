import asyncio
import secrets
from fastapi import APIRouter, Request, HTTPException, status
from datetime import datetime
from fistbump import schemas
from fistbump.config import settings
from fistbump.helpers import DB_user, iso_now
from tinydb.operations import set as tiny_set

router = APIRouter(tags=["me"])


@router.get("/me/{id}/{token}")
async def me(id: int, token: str) -> schemas.User:
    async with DB_user as db:
        user = db.get(doc_id=id)
        if user["token"] != token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        # update in db when last active
        db.update(
            tiny_set(
                field="active",
                val=iso_now(),
            ),
            doc_ids=[id],
        )
    return schemas.User(**user)


@router.post("/me")
async def me_create():
    async with DB_user as db:
        user_id = db.insert(
            {
                "topped": [],
                "active": iso_now(),
                "token": secrets.token_hex(16),
            }
        )
        user = db.get(doc_id=user_id)
    return schemas.User(**user)
