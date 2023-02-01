import asyncio
from fastapi import APIRouter, Request, HTTPException, status
from datetime import datetime
from fistbump import schemas
from fistbump.config import settings

router = APIRouter(tags=["misc"])


@router.get("/strip")
async def strip() -> schemas.Strip:
    today = datetime.now(tz=settings.tz).replace(tzinfo=None)
    STRIPDATA = [
        (datetime(2023, 1, 26, 12, 0, 0), "probyg", "Section 4"),
        (datetime(2023, 2, 3, 12, 0, 0), "workshop", "Section 5"),
        (datetime(2023, 2, 9, 12, 0, 0), "probyg", "Section 1"),
        (datetime(2023, 2, 17, 12, 0, 0), "fribyg", "Section 2"),
        (datetime(2023, 2, 23, 12, 0, 0), "probyg", "Section 3"),
        (datetime(2023, 3, 3, 12, 0, 0), "forbund", "Section 4+5"),
        (datetime(2023, 3, 9, 12, 0, 0), "probyg", "Section 1"),
        (datetime(2023, 3, 17, 12, 0, 0), "fribyg", "Section 2"),
        (datetime(2023, 3, 23, 12, 0, 0), "probyg", "Section 3"),
        (datetime(2023, 3, 31, 12, 0, 0), "workshop", "Section 4"),
        (datetime(2023, 4, 18, 12, 0, 0), "juniorbattle", "Section 1+2+3+4+5"),
    ]
    for next_strip, setters, section in STRIPDATA:
        if next_strip >= today:
            return schemas.Strip(datetime=next_strip, section=section, setters=setters)


LIMITER = []


@router.get("/setter-code/{setter_code}")
async def link_setter_code(setter_code: str, request: Request) -> schemas.SetterToken:
    h = request.client.host
    if h in LIMITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="go away")
    LIMITER.append(h)
    await asyncio.sleep(10)
    if setter_code == settings.setter_code:
        LIMITER.remove(h)
        return schemas.SetterToken(access_token=settings.auth_token)
    # else
    LIMITER.remove(h)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="go away")
