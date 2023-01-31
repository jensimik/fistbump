import sentry_sdk
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import calendar, problems, webp, misc
from .repeat_every_helper import repeat_every
from .stokt import refresh_stokt
from .config import settings

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="fistbump-api",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=settings.static_directory), name="static")

app.include_router(calendar.router)
app.include_router(problems.router)
app.include_router(misc.router)
app.include_router(webp.router)


# sync stokt every hour
@app.on_event("startup")
@repeat_every(seconds=60 * 60)
async def _refresh_stokt():
    await refresh_stokt()
