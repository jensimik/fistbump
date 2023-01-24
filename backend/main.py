import json
import aiofiles
from pprint import pprint
from uuid import uuid4
from collections import Counter
from datetime import date, datetime, timedelta
from dateutil import tz
from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from requests_html import AsyncHTMLSession
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from async_lru import alru_cache
from functools import lru_cache
from livepopulartimes import get_populartimes_by_place_id
from aiotinydb import AIOTinyDB
from tinydb import where
from tasks import repeat_every
from pydantic import BaseModel, Field
from pydantic.typing import Literal

app = FastAPI()
session = AsyncHTMLSession()
# mqtt setup
# mqtt_config = MQTTConfig()
# fast_mqtt = FastMQTT(config=mqtt_config)
# fast_mqtt.init_app(app)

origins = ["http://localhost:5173", "https://fistbump.gnerd.dk"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="/static"), name="static")

FEED_DB = "/data/feed.json"
STOKT_TOKEN = "3ea0c2f73089ed54ea0b13325204f3be45bd7788"
GOOGLE_MAPS_API_KEY = "AIzaSyAWEoNtxFZFCNxOi-9il0whTnRr7dP331w"
GOOGLE_MAPS_PLACE_ID = "ChIJ7etYrU1SUkYRu9v7IHXpF5c"
TZ = tz.gettz("Europe/Copenhagen")

# load holds setup from json file
with open("setup.json", "r") as f:
    HOLDS_PATH = {h["id"]: h for h in json.load(f)["holds"]}

GRADE_TO_COLOR = {
    "?": "turquoise",
    "4": "green",
    "5+": "yellow",
    "5B": "yellow",
    "5B+": "yellow",
    "5B-5B+": "yellow",
    "5C": "blue",
    "5C+": "blue",
    "6A": "blue",
    "6A+": "blue",
    "5C-6A+": "blue",
    "6B": "purple",
    "6B+": "purple",
    "6B-6B+": "purple",
    "6C": "red",
    "6C+": "red",
    "6C-6C+": "red",
    "7A": "brown",
    "7A+": "brown",
    "7A-7A+": "brown",
    "7B": "black",
    "7B+": "black",
    "7C": "black",
    "7B-7C": "black",
    "7C+": "white",
    "8A": "white",
    "7C+-8C": "white",
}

WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


@lru_cache(maxsize=1)
def _get_popular_times():
    data = get_populartimes_by_place_id(GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_PLACE_ID)
    return {WEEKDAYS.get(d["name"]): d["data"] for d in data["populartimes"]}


WEEKDAY_REVERSE = {
    "Mandag": [0],
    "Tirsdag": [1],
    "Onsdag": [2],
    "Torsdag": [3],
    "Fredag": [4],
    "Lørdag": [5],
    "Søndag": [6],
    "Mandag - Torsdag": [0, 1, 2, 3],
    "Mandag - Fredag": [0, 1, 2, 3, 4],
    "Lørdag - Søndag": [5, 6],
}


@alru_cache(maxsize=2)
async def _get_opening_hours(today):
    data = {}
    hours_today = "n/a"
    hours_tomorrow = "n/a"
    weekday_today = today.weekday()
    weekday_tomorrow = (today + timedelta(days=1)).weekday()
    r = await session.get("https://kulturogfritidn.kk.dk/noerrebrohallen")
    if r.ok:
        div_opening_hours = r.html.find("div.kk-contact-opening-hours", first=True)
        for row in div_opening_hours.find("div.kk-contact-opening-hours__row"):
            label = row.find("div.kk-contact-opening-hours__label", first=True).text
            value = row.find("div.kk-contact-opening-hours__value > p", first=True).text
            data[label] = value
            if weekday_today in WEEKDAY_REVERSE.get(label, []):
                hours_today = value
            elif weekday_tomorrow in WEEKDAY_REVERSE.get(label, []):
                hours_tomorrow = value
    return data, hours_today, hours_tomorrow


@app.get("/hours")
async def get_opening_hours():
    today = datetime.now(tz=TZ).date()
    data, hours_today, hours_tomorrow = await _get_opening_hours(today)
    return {
        "today": f"{today:%Y-%m-%d}",
        "hours_today": hours_today,
        "hours_tomorrow": hours_tomorrow,
        "data": data,
    }


@alru_cache(maxsize=2)
async def _get_calendar_agenda(today):
    data = []
    today_str = "{0:%d}.{0:%m}.{0:%Y}".format(today)
    tomorrow_str = "{0:%d}.{0:%m}.{0:%Y}".format(today + timedelta(days=1))
    today = []
    tomorrow = []
    r = await session.get(
        "https://nkk.klub-modul.dk/cms/activity.aspx?CalendarType=Agenda"
    )
    if r.ok:
        div_calendar = r.html.find("div#km_cal_agenda", first=True)
        for row in div_calendar.find("div.km-agenda-item"):
            entry_datetime = row.find("div.km-agenda-time", first=True).text
            entry_date = entry_datetime[:10]
            entry_time = entry_datetime[11:]
            entry_title = row.find("div.km-agenda-eventname", first=True).text
            d = {
                "datetime": entry_datetime,
                "date": entry_date,
                "time": entry_time,
                "title": entry_title,
            }
            data.append(d)
            if entry_date == today_str:
                today.append(d)
            elif entry_date == tomorrow_str:
                tomorrow.append(d)
    return data, today, tomorrow


@app.get("/calendar")
async def get_calendar_agenda():
    today = datetime.now(tz=TZ).date()
    data, today, tomorrow = await _get_calendar_agenda(today)
    return today
    # return {"today": today, "tomorrow": tomorrow, "data": data}


@app.get("/popular_hours")
def get_popular_hours():
    today = datetime.now(tz=TZ).date().weekday()
    return [(i, x) for i, x in enumerate(_get_popular_times()[today])]


@app.get("/")
async def read_root():
    return {"noting": "tofindhere"}


@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # every hour?
async def _refresh_stokt():
    print("going to fetch stokt")
    hour = datetime.now(tz=TZ).hour
    if hour not in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]:
        print("skipping")
        return
    problems = []
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "stokt/1 CFNetwork/1402.0.8 Darwin/22.2.0",
        "Accept-Language": "en-GB,en;q=0.9",
        "Authorization": f"Token {STOKT_TOKEN}",
    }
    r = await session.get(
        "https://www.sostokt.com/api/gyms/1ada530f-887b-44b2-b817-976f058e6696/new-climbs",
        headers=headers,
    )
    if r.ok:
        data = r.json()
        problems = [
            {
                "stokt_id": p["id"],
                "section": "Ö1",
                "name": p["name"],
                "grade": p["crowdGrade"]["font"],
                "holds": p["holdsList"],
                "setter": p["climbSetters"]["fullName"],
                "created": "{0:%Y-%m-%dT%H:%M:%S}".format(
                    datetime.fromisoformat(p["dateCreated"])
                ),
            }
            for p in data
        ]
    async with AIOTinyDB(FEED_DB) as db:
        for problem in problems:
            db.upsert(problem, where("stokt_id") == problem["stokt_id"])

    print("finished fetching from stokt")


@app.get("/feed")
async def feed():
    async with AIOTinyDB(FEED_DB) as db:
        data = sorted(db, key=lambda d: d["created"], reverse=True)[:50]
        today = datetime.now(tz=TZ).replace(tzinfo=None)
        for d in data:
            d["id"] = d.doc_id
            d["grade_class"] = GRADE_TO_COLOR.get(d["grade"])
            d["days_back"] = (today - datetime.fromisoformat(d["created"])).days
        return data


@app.post("/feed")
async def feed_post(
    file: UploadFile,
    name: str = Form(),
    grade: str = Form(),
    setter: str = Form(),
    text: str = Form(),
    section: Literal["S1", "S2", "S3", "S4", "S5"] = Form(),
):
    today = datetime.now(tz=TZ).date()
    save_filename = f"{uuid4().hex}.jpg"
    problem = {
        "name": name,
        "grade": grade,
        "section": section,
        "setter": setter,
        "text": text,
        "image": f"https://fbs.gnerd.dk/static/{save_filename}",
        "created": f"{today:%Y-%m-%dT%H:%M:%S}",
    }
    async with aiofiles.open(f"/static/{save_filename}", "wb") as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    async with AIOTinyDB(FEED_DB) as db:
        db.insert(problem)
    return problem


@app.get("/feed/{item_id}")
async def feed_get_item(item_id: int):
    async with AIOTinyDB(FEED_DB) as db:
        item = db.get(doc_id=item_id)
        # parse hold paths if stökt
        paths = []
        if item["section"] == "Ö1":
            starting_hold_count = sum(
                [1 if hold.startswith("S") else 0 for hold in item["holds"].split(" ")]
            )
            for hold in item["holds"].split(" "):
                hit = int(hold[1:])
                if hold.startswith("S"):
                    paths.append({"path": HOLDS_PATH[hit]["pathStr"], "type": "hand"})
                    if starting_hold_count == 2:
                        paths.append(
                            {
                                "path": "M" + HOLDS_PATH[hit]["rightTapeStr"],
                                "type": "hand",
                            }
                        )
                    else:
                        paths.append(
                            {
                                "path": "M" + HOLDS_PATH[hit]["rightTapeStr"],
                                "type": "hand",
                            }
                        )
                        paths.append(
                            {
                                "path": "M" + HOLDS_PATH[hit]["leftTapeStr"],
                                "type": "hand",
                            }
                        )
                elif hold.startswith("F"):
                    paths.append({"path": HOLDS_PATH[hit]["pathStr"], "type": "foot"})
                elif hold.startswith("T"):
                    paths.append({"path": HOLDS_PATH[hit]["pathStr"], "type": "hand"})
                    paths.append(
                        {
                            "path": "M" + HOLDS_PATH[hit]["topPolygonStr"],
                            "type": "hand",
                        }
                    )
                elif hold.startswith("O"):
                    paths.append({"path": HOLDS_PATH[hit]["pathStr"], "type": "hand"})
                else:
                    paths.append(
                        {"path": HOLDS_PATH[int(hold)]["pathStr"], "type": "hand"}
                    )

        return {
            "id": item.doc_id,
            "paths": paths,
            "grade_class": GRADE_TO_COLOR.get(item["grade"]),
            **item,
        }


@app.get("/strip")
async def strip():
    today = datetime.now(tz=TZ).date()
    next_strip = date(2023, 1, 26)

    return {
        "date": f"{next_strip:%d %b}",
        "until": (next_strip - today).days,
        "section": "section4",
    }


@app.get("/grade-stats")
async def grade_stats():
    async with AIOTinyDB(FEED_DB) as db:
        stats_boulder = Counter(
            [
                GRADE_TO_COLOR.get(d["grade"], "?")
                for d in db
                if d["section"] in ["S1", "S2", "S3", "S4", "S5"]
            ]
        ).most_common()
        stats_stokt = Counter(
            [GRADE_TO_COLOR.get(d["grade"], "?") for d in db if d["section"] == "Ö1"]
        ).most_common()

        return {"stokt": stats_stokt, "boulder": stats_boulder}
