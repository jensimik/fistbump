import httpx
import re
from fistbump.parse import HTML

event_id_regex = re.compile(
    r"^CalendarEventShowPopUp\.aspx\?CalendarEventID=(?P<eventid>\d+)&amp;CalendarEventTimeID=\d+&amp;HashCode=\d+$"
)


async def get_calendar_agenda():
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
                event_name = row.find("div.km-agenda-eventname", first=True)
                entry_title = event_name.text
                eventid = event_id_regex.search(
                    event_name.find("a", first=True).attrs["href"]
                ).group("eventid")
                yield {
                    "eventid": eventid,
                    "datetime": entry_datetime,
                    "date": entry_date,
                    "time": " - ".join(entry_time.split("-")),
                    "title": entry_title,
                }
