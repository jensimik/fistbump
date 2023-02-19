import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import calendar, problems, webp, misc
from .repeat_every_helper import repeat_every
from .stokt import refresh_stokt
from .helpers import maintenance
from .config import settings
from fistbump import __version__


if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        release=__version__,
    )

app = FastAPI(
    title="fistbump-api",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex="https://fistbump-pr-.*\.onrender\.com",  # allow onrender.com pull-requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calendar.router)
app.include_router(problems.router)
app.include_router(misc.router)
app.include_router(webp.router)


# sync stokt every hour
if settings.stokt_refresh == 1:

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60)
    async def _refresh_stokt():
        await refresh_stokt()


@app.on_event("startup")
@repeat_every(seconds=60 * 60)
async def _maintenance():
    maintenance()
