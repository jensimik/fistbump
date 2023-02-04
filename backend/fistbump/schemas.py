from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class Circle(BaseModel):
    cx: int
    cy: int


class Strip(BaseModel):
    datetime: datetime
    section: str
    setters: str
    days_to_strip: int
    date_formatted: str


class Hours(BaseModel):
    today: str
    hours_today: str


class SetterToken(BaseModel):
    access_token: str


class Problem(BaseModel):
    id: int
    grade: str
    grade_class: Literal[
        "green",
        "yellow",
        "blue",
        "purple",
        "red",
        "brown",
        "black",
        "white",
        "turquoise",
    ]
    name: str
    section: Literal["Ö", "S1", "S2", "S3", "S4", "S5", "L"]
    setter: str
    created: datetime
    days_back: Optional[int] = None
    # hold color only for problems in the boulder
    color: Optional[
        Literal[
            "yellow",
            "red",
            "blue",
            "green",
            "black",
            "white",
            "purple",
            "brown",
            "orange",
        ]
    ]
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    annotations: Optional[list[Circle]] = []
    # image_hex only for problems in the boulder
    image_hex: Optional[str] = None
    # paths only for stokt
    paths: Optional[list[dict[str, str]]]
    # stokts_id only for stokt
    stokt_id: Optional[str] = None
    # holds only for stokt
    holds: Optional[str] = None


class Status(BaseModel):
    message: str
