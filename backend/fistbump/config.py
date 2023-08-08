from pathlib import Path
from typing import Any, Optional, Type, Tuple

from dateutil.tz import gettz, tzfile
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if field_name == "tz":
            return gettz(value)
        elif field_name == "admin_user_ids":
            if value:
                return [int(v) for v in value.split()]
        return value


class Settings(BaseSettings):
    app_name: str = "Fistbump"
    cors_origins: list = [
        "http://localhost:5173",
        "http://192.168.1.44:5173",
        "http://192.168.1.168:5173",
        "https://fistbump.nkk.dk",
    ]
    auth_token: Optional[str] = None
    images_directory: Path = "/data"
    problem_db_file: Path = "/data/feed.json"
    user_db_file: Path = "/data/user.json"
    google_maps_api_key: Optional[str] = None
    google_maps_place_id: str = "ChIJ7etYrU1SUkYRu9v7IHXpF5c"
    stokt_token: Optional[str]
    sentry_dsn: str = None
    stokt_refresh: int = 0
    lumo_firebase_apikey: str = None
    lumo_username: str = None
    lumo_password: str = None
    setter_code: Optional[str] = None

    jwt_secret: str = "CHANGE_ME"

    hold_colors: list = [
        "yellow",
        "red",
        "blue",
        "green",
        "black",
        "white",
        "purple",
        "brown",
        "orange",
        "rainbow",
    ]
    tz: tzfile = gettz("Europe/Copenhagen")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)


settings = Settings()
