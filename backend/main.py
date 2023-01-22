from pprint import pprint
from datetime import date, timedelta
from fastapi import FastAPI
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

app = FastAPI()
session = AsyncHTMLSession()
# mqtt setup
# mqtt_config = MQTTConfig()
# fast_mqtt = FastMQTT(config=mqtt_config)
# fast_mqtt.init_app(app)

origins = [
    "http://localhost:8000",
    "https://fistbump-api.gnerd.dk"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FEED_DB = "/data/feed.json"
STOKT_TOKEN = "3ea0c2f73089ed54ea0b13325204f3be45bd7788"
GOOGLE_MAPS_API_KEY = "AIzaSyAWEoNtxFZFCNxOi-9il0whTnRr7dP331w"
GOOGLE_MAPS_PLACE_ID = "ChIJ7etYrU1SUkYRu9v7IHXpF5c"

WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}


@lru_cache(maxsize=1)
def _get_popular_times():
    data = get_populartimes_by_place_id(GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_PLACE_ID)
    return {WEEKDAYS.get(d["name"]) : d["data"] for d in data["populartimes"]}

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
    "Lørdag - Søndag": [5, 6]
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
    data, today, tomorrow = await _get_opening_hours(date.today())
    return {"hours_today": today, "hours_tomorrow": tomorrow, "data": data}

@alru_cache(maxsize=2)
async def _get_calendar_agenda(today):
    data = []
    today_str = "{0:%d}.{0:%m}.{0:%Y}".format(today)
    tomorrow_str = "{0:%d}.{0:%m}.{0:%Y}".format(today + timedelta(days=1))
    today = []
    tomorrow = []
    r = await session.get("https://nkk.klub-modul.dk/cms/activity.aspx?CalendarType=Agenda")
    if r.ok:
        div_calendar = r.html.find("div#km_cal_agenda", first=True)
        for row in div_calendar.find("div.km-agenda-item"):
            entry_datetime = row.find("div.km-agenda-time", first=True).text
            entry_date = entry_datetime[:10]
            entry_time = entry_datetime[11:]
            entry_title = row.find("div.km-agenda-eventname", first=True).text
            d = {"datetime": entry_datetime, "date": entry_date, "time": entry_time, "title": entry_title}
            data.append(d)
            if entry_date == today_str:
                today.append(d)
            elif entry_date == tomorrow_str:
                tomorrow.append(d)
    return data, today, tomorrow

@app.get("/calendar")
async def get_calendar_agenda():
    data, today, tomorrow = await _get_calendar_agenda(date.today())
    return {"today": today, "tomorrow": tomorrow, "data": data}


@app.get("/popular_hours")
def get_popular_hours():
    today = date.today().weekday()
    return [(i, x) for i, x in enumerate(_get_popular_times()[today])]


@app.get("/")
async def read_root():
    return {"noting": "tofindhere"}

@app.on_event("startup")
@repeat_every(seconds=60*30) # every half hour?
async def _refresh_stokt():
    problems = []
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "stokt/1 CFNetwork/1402.0.8 Darwin/22.2.0",
        "Accept-Language": "en-GB,en;q=0.9",
        "Authorization": f"Token {STOKT_TOKEN}"
    }
    params = {
        "grade_from": "4",
        "grade_to": "?",
        "ordering": "most_recent",
        "tags": "",
        "search": "",
        "exclude_mine": "false",
        "show_circuit_only": "false",
        "cursor": "",
        "tags": "",
    }
    r = await session.get(
        "https://www.sostokt.com/api/faces/54c4b9f2-2e12-4f60-8243-6f520bc81d13/latest-climbs/paginated", 
        params=params, 
        headers=headers
    )
    if r.ok:
        data = r.json()
        problems = [
            {
                "stokt_id": p["id"], 
                "section": "S", 
                "name": p["name"], 
                "grade": p["crowdGrade"]["font"], 
                "created": p["dateCreated"][:10]
            } for p in data["results"]]
    async with AIOTinyDB(FEED_DB) as db:
        for problem in problems:
            db.upsert(problem, where("stokt_id") == problem["stokt_id"])
    return problems
    

@app.get("/feed")
async def feed():
    async with AIOTinyDB(FEED_DB) as db:
        data = sorted(db, key=lambda d: d["created"], reverse=True)[:20]
        today = date.today()
        for d in data:
            d["days_back"] = (today - date.fromisoformat(d["created"])).days
        return data

@app.post("/feed")
async def feed_post():
    pass
    # TODO: implement adding an entry to the feed