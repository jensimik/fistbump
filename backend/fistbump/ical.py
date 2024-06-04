import httpx
import re
import uuid
import json
from fistbump.parse import HTML

event_id_regex = re.compile(
    r"^CalendarEventShowPopUp\.aspx\?CalendarEventID=(?P<eventid>\d+)&CalendarEventTimeID=\d+&HashCode=[\d-]+$"
)


async def get_calendar_agenda():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://nkk.klub-modul.dk/cms/Activity.aspx")
        if r.is_success:
            html = HTML(html=r.content)
            script_tag = html.find("script")[-3]
            data = json.loads(
                script_tag.text.split("var jsonData = ")[1].split(
                    ";new Sys.WebForms.Menu"
                )[0]
            )
            for event in data:
                hour_start = event["start"].split("T")[1]
                hour_end = event["end"].split("T")[1]
                yield {
                    "eventid": event["id"] + event["start"],
                    "datetime": event["start"],
                    "date": event["start"][:10],
                    "time": " - ".join([hour_start, hour_end]),
                    "title": event["title"],
                }
