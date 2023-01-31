from typing import Any
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from pathlib import Path
from dateutil.tz import tzfile, gettz


class Settings(BaseSettings):
    app_name: str = "Fistbump"
    cors_origins: list = [
        "https://fistbump.nkk.dk",
    ]
    auth_token: str
    static_directory: Path = "/static"
    problem_db_file: Path = "/data/feed.json"
    google_maps_api_key: str
    google_maps_place_id: str
    stokt_token: str
    sentry_dsn: str = None
    stokt_refresh: int = 0
    tz: tzfile = gettz("Europe/Copenhagen")

    class Config:
        # parse tz field as a dateutil.tz
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "tz":
                return gettz(raw_val)
            return cls.json_loads(raw_val)

        # do not try to load from file
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings


settings = Settings()
