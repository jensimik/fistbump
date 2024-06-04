import httpx
import pytz
from fastapi import APIRouter, Response
from functools import lru_cache
from async_lru import alru_cache
from livepopulartimes import get_populartimes_by_place_id
from datetime import datetime, timedelta
from fistbump import schemas
from fistbump.config import settings
from fistbump.parse import HTML
from fistbump.ical import get_calendar_agenda
from icalendar import Calendar, Event, vText

router = APIRouter(tags=["calendar"])

WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
WEEKDAY_REVERSE = {
    "Mandag": [0],
    "Tirsdag": [1],
    "Onsdag": [2],
    "Torsdag": [3],
    "Fredag": [4],
    "Lørdag": [5],
    "Søndag": [6],
    "Mandag - Tirsdag": [0, 1],
    "Mandag - Onsdag": [0, 1, 2],
    "Mandag - Torsdag": [0, 1, 2, 3],
    "Mandag - Fredag": [0, 1, 2, 3, 4],
    "Tirsdag - Torsdag": [1, 2, 3],
    "Lørdag - Søndag": [5, 6],
    "Fredag - Søndag": [4, 5, 6],
    "Torsdag - Søndag": [3, 4, 5, 6],
}


@lru_cache(maxsize=1)
def _get_popular_times():
    data = get_populartimes_by_place_id(
        settings.google_maps_api_key, settings.google_maps_place_id
    )
    return {WEEKDAYS.get(d["name"]): d["data"] for d in data["populartimes"]}


@alru_cache(maxsize=2)
async def _get_opening_hours(today):
    # return {}, "n/a", "n/a"
    data = {}
    hours_today = "n/a"
    hours_tomorrow = "n/a"
    weekday_today = today.weekday()
    weekday_tomorrow = (today + timedelta(days=1)).weekday()
    async with httpx.AsyncClient() as client:
        r = await client.get("https://kulturogfritidn.kk.dk/noerrebrohallen")
        if r.is_success:
            html = HTML(html=r.content)
            div_opening_hours = html.find("div.kk-contact-opening-hours", first=True)
            for row in div_opening_hours.find("div.kk-contact-opening-hours__row"):
                label = row.find("div.kk-contact-opening-hours__label", first=True).text
                value = row.find(
                    "div.kk-contact-opening-hours__value > p", first=True
                ).text
                data[label] = value
                if weekday_today in WEEKDAY_REVERSE.get(label, []):
                    hours_today = value
                elif weekday_tomorrow in WEEKDAY_REVERSE.get(label, []):
                    hours_tomorrow = value
    return data, hours_today, hours_tomorrow


@router.get("/hours")
async def get_opening_hours() -> schemas.Hours:
    today = datetime.now(tz=settings.tz).date()
    data, hours_today, hours_tomorrow = await _get_opening_hours(today)
    return schemas.Hours(today=f"{today:%Y-%m-%d}", hours_today=hours_today)


@alru_cache(maxsize=2)
async def _get_calendar_agenda(today):
    today_str = "{0:%Y}-{0:%m}-{0:%d}".format(today)
    return [
        entry async for entry in get_calendar_agenda() if entry["date"] == today_str
    ]


@router.get("/calendar")
async def get_calendar():
    today = datetime.now(tz=settings.tz).date()
    return await _get_calendar_agenda(today)


@router.get("/calendar.ics")
async def get_calendar_ics():
    cal = Calendar()
    cal.add("prodid", "-//NKK calandar//nkk.dk//")
    cal.add("version", "2.0")
    noerrebrohallen = vText("Nørrebrohallen, Copenhagen, Denmark")
    tz = pytz.timezone("Europe/Copenhagen")
    async for entry in get_calendar_agenda():
        event = Event()
        day = datetime.strptime(entry["date"], "%Y-%m-%d")
        rdtstart, rdtend = entry["time"].split(" - ")
        rdtend = "23:59" if rdtend == "24:00" else rdtend
        event["uid"] = entry["eventid"] + "@nkk.dk"
        event.add("priority", 5)
        dtstart = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=int(rdtstart.split(":")[0]),
            minute=int(rdtstart.split(":")[1]),
            tzinfo=tz,
        )
        dtend = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=int(rdtend.split(":")[0]),
            minute=int(rdtend.split(":")[1]),
            tzinfo=tz,
        )
        event.add("summary", entry["title"])
        event.add("dtstart", dtstart)
        event.add("dtend", dtend)
        event.add("dtstamp", dtstart)
        event["location"] = noerrebrohallen
        cal.add_component(event)
    return Response(content=cal.to_ical(), media_type="text/calendar")


@router.get("/popular_hours")
def get_popular_hours():
    today = datetime.now(tz=settings.tz).date().weekday()
    return [(i, x) for i, x in enumerate(_get_popular_times()[today])]
