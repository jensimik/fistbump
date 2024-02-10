import httpx
from datetime import datetime
from .helpers import DB, where
from .config import settings


async def refresh_stokt():
    print("going to fetch stokt")
    hour = datetime.now(tz=settings.tz).hour
    if hour not in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]:
        print("skipping")
        return
    problems = []
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "stokt/1 CFNetwork/1402.0.8 Darwin/22.2.0",
        "Accept-Language": "en-GB,en;q=0.9",
        "Authorization": f"Token {settings.stokt_token}",
    }
    timestamp = int(datetime.utcnow().timestamp())
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://www.sostokt.com/api/gyms/1ada530f-887b-44b2-b817-976f058e6696/new-climbs",
            headers=headers,
        )
        if r.is_success:
            data = r.json()
            problems = [
                {
                    "stokt_id": p["id"],
                    "section": "Ö",
                    "name": p["name"],
                    "grade": p["crowdGrade"]["font"],
                    "holds": p["holdsList"],
                    "setter": p["climbSetters"]["fullName"],
                    "hidden": p["isPrivate"],
                    "created": "{0:%Y-%m-%dT%H:%M:%S}".format(
                        datetime.fromisoformat(p["dateCreated"])
                    ),
                }
                for p in data
            ]
    problem_ids = [p["stokt_id"] for p in problems]
    async with DB as db:
        for problem in problems:
            if problem["hidden"]:
                db.remove(where("stokt_id") == problem["stokt_id"])
            else:
                db.upsert(problem, where("stokt_id") == problem["stokt_id"])
        db.remove(~where("stokt_id").any(problem_ids))

    print("finished fetching from stokt")
