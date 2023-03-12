import httpx
from fastapi import APIRouter
from functools import lru_cache
from async_lru import alru_cache
from livepopulartimes import get_populartimes_by_place_id
from datetime import datetime, timedelta
from fistbump import schemas
from fistbump.config import settings
from requests_html import HTML

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
    "Mandag - Torsdag": [0, 1, 2, 3],
    "Mandag - Fredag": [0, 1, 2, 3, 4],
    "Lørdag - Søndag": [5, 6],
}


@lru_cache(maxsize=1)
def _get_popular_times():
    data = get_populartimes_by_place_id(
        settings.google_maps_api_key, settings.google_maps_place_id
    )
    return {WEEKDAYS.get(d["name"]): d["data"] for d in data["populartimes"]}


@alru_cache(maxsize=2)
async def _get_opening_hours(today):
    return {}, "n/a", "n/a"
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
    today_str = "{0:%d}.{0:%m}.{0:%Y}".format(today)
    # tomorrow_str = "{0:%d}.{0:%m}.{0:%Y}".format(today + timedelta(days=1))
    today = []
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://nkk.klub-modul.dk/cms/activity.aspx?CalendarType=Agenda"
        )
        if r.is_success:
            html = HTML(html=r.content)
            div_calendar = html.find("div#km_cal_agenda", first=True)
            for row in div_calendar.find("div.km-agenda-item"):
                entry_datetime = row.find("div.km-agenda-time", first=True).text
                entry_date = entry_datetime[:10]
                entry_time = entry_datetime[11:]
                entry_title = row.find("div.km-agenda-eventname", first=True).text
                d = {
                    "datetime": entry_datetime,
                    "date": entry_date,
                    "time": " - ".join(entry_time.split("-")),
                    "title": entry_title,
                }
                if entry_date == today_str:
                    today.append(d)
    return today


@router.get("/calendar")
async def get_calendar_agenda():
    today = datetime.now(tz=settings.tz).date()
    return await _get_calendar_agenda(today)


@router.get("/popular_hours")
def get_popular_hours():
    today = datetime.now(tz=settings.tz).date().weekday()
    return [(i, x) for i, x in enumerate(_get_popular_times()[today])]
