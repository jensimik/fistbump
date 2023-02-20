import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from fistbump import __version__

from .config import settings
from .helpers import maintenance
from .repeat_every_helper import repeat_every
from .routers import auth, calendar, misc, problems, webp
from .stokt import refresh_stokt

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.1,
        release=__version__,
    )

app = FastAPI(
    title="fistbump-api",
    version=__version__,
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="fistbump",
    group_paths=True,
    skip_paths=["/healtz"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex="https://fistbump-pr-.*\.onrender\.com",  # allow onrender.com pull-requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(calendar.router)
app.include_router(problems.router)
app.include_router(misc.router)
app.include_router(webp.router)


@app.get("/healtz")
async def healthz():
    return {"everything": "is awesome"}


app.add_route("/metrics", handle_metrics)


# sync stokt every hour
if settings.stokt_refresh == 1:

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60)
    async def _refresh_stokt():
        await refresh_stokt()


@app.on_event("startup")
@repeat_every(seconds=60 * 60)
async def _maintenance():
    await maintenance()
