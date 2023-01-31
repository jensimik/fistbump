import aiofiles
from uuid import uuid4
from typing import Literal, Optional
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, Form
from fastapi.security.api_key import APIKey
from datetime import datetime
from collections import Counter
from fistbump import schemas
from fistbump.config import settings
from fistbump.helpers import DB, where, GRADE_TO_COLOR, holds_to_paths
from fistbump.depends import get_api_key

router = APIRouter(tags=["problems"])

# list all problems
@router.get("/problems")
async def problems() -> list[schemas.Problem]:
    today = datetime.now(tz=settings.tz).replace(tzinfo=None)
    async with DB as db:
        data = sorted(db, key=lambda d: d["created"], reverse=True)[:50]
    return [
        schemas.Problem(
            id=d.doc_id,
            grade_class=GRADE_TO_COLOR.get(d["grade"]),
            days_back=(today - datetime.fromisoformat(d["created"])).days,
            paths=[p for p in holds_to_paths(d["holds"])] if "holds" in d else [],
            **d,
        )
        for d in data
    ]


# get a specific problem
@router.get("/problems/{item_id}")
async def get_problem(item_id: int) -> schemas.Problem:
    async with DB as db:
        item = db.get(doc_id=item_id)

    # if "image_hex" in item:
    #     item["image_webp"] = "https://fbs.gnerd.dk/webp/{}.webp".format(
    #         item["image_hex"]
    #     )
    #     item["image_webp800"] = "https://fbs.gnerd.dk/webp/{}/800.webp".format(
    #         item["image_hex"]
    #     )
    return schemas.Problem(
        id=item.doc_id,
        grade_class=GRADE_TO_COLOR.get(item["grade"]),
        paths=[p for p in holds_to_paths(item["holds"])] if "holds" in item else [],
        **item,
    )


# create new problem
@router.post("/problems", status_code=status.HTTP_201_CREATED)
async def create_problem(
    file: UploadFile,
    name: str = Form(),
    color: str = Form(),
    grade: str = Form(),
    setter: str = Form(),
    text: Optional[str] = Form(""),
    section: Literal["S1", "S2", "S3", "S4", "S5"] = Form(),
    _: APIKey = Depends(get_api_key),
) -> schemas.Problem:
    # save image
    hex = uuid4().hex
    save_filename = f"{hex}.jpg"
    async with aiofiles.open(
        settings.static_directory / save_filename, "wb"
    ) as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    # save problem in tinydb
    today = datetime.now(tz=settings.tz).replace(tzinfo=None)
    problem = {
        "name": name,
        "grade": grade,
        "color": color,
        "section": section,
        "setter": setter,
        "text": text,
        "image": f"https://fbs.gnerd.dk/static/{save_filename}",
        "image_hex": hex,
        "created": today.isoformat(timespec="seconds"),
    }
    async with DB as db:
        insert_id = db.insert(problem)
    return schemas.Problem(
        id=insert_id,
        grade_class=GRADE_TO_COLOR.get(problem["grade"]),
        **problem,
    )


# remove a problem
@router.delete("/problems/{item_id}")
async def delete_problem(
    item_id: int,
    auth: str,
    _: APIKey = Depends(get_api_key),
) -> schemas.Status:
    async with DB as db:
        item = db.remove(doc_ids=[item_id])
    return schemas.Status(message="deleted problem")


# update a problem
@router.put("/problems/{item_id}")
async def update_problem(
    item_id: int,
    name: str = Form(),
    color: str = Form(),
    grade: str = Form(),
    setter: str = Form(),
    text: Optional[str] = Form(""),
    section: Literal["S1", "S2", "S3", "S4", "S5"] = Form(),
    file: Optional[UploadFile] = None,
    _: APIKey = Depends(get_api_key),
) -> schemas.Problem:
    today = datetime.now(tz=settings.tz)

    # get the problem from db
    async with DB as db:
        item = db.get(doc_id=item_id)

    image_url = item["image"]
    hex = item["hex"]

    # if file provided in update then save it
    if file:
        hex = uuid4().hex
        save_filename = f"{hex}.jpg"
        async with aiofiles.open(
            settings.static_directory / save_filename, "wb"
        ) as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk
        image_url = f"https://fbs.gnerd.dk/static/{save_filename}"

    problem = {
        "name": name,
        "grade": grade,
        "color": color,
        "section": section,
        "setter": setter,
        "text": text,
        "image": image_url,
        "image_hex": hex,
        "created": item["created"],
    }
    # update in tinydb
    async with DB as db:
        db.update(problem, doc_ids=[item_id])
    return schemas.Problem(
        id=item_id,
        grade_class=GRADE_TO_COLOR.get(problem["grade"]),
        **problem,
    )


# a section view
@router.get("/sections/{section_id}")
async def feed(section_id: str):
    today = datetime.now(tz=settings.tz).replace(tzinfo=None)
    async with DB as db:
        data = sorted(
            db.search(where("section") == section_id),
            key=lambda d: d["created"],
            reverse=True,
        )[:50]
    for d in data:
        d["id"] = d.doc_id
        d["grade_class"] = GRADE_TO_COLOR.get(d["grade"])
        d["days_back"] = (today - datetime.fromisoformat(d["created"])).days
        if "image_hex" in d:
            d["image_webp"] = "https://fbs.gnerd.dk/webp/{}.webp".format(d["image_hex"])
            d["image_webp800"] = "https://fbs.gnerd.dk/webp/{}/800.webp".format(
                d["image_hex"]
            )

    grades_temp = Counter([d["grade_class"] for d in data])
    colors = Counter([d["color"] for d in data])
    grades = [
        (c, grades_temp.get(c, 0))
        for c in ["green", "yellow", "blue", "purple", "red", "brown", "black", "white"]
    ]
    return {"data": data, "colors": colors, "grades": grades}


# setter stats about grades
@router.get("/grade-stats")
async def grade_stats():
    async with DB as db:
        stats_boulder = Counter(
            [
                GRADE_TO_COLOR.get(d["grade"], "?")
                for d in db
                if d["section"] in ["S1", "S2", "S3", "S4", "S5"]
            ]
        ).most_common()
        stats_stokt = Counter(
            [GRADE_TO_COLOR.get(d["grade"], "?") for d in db if d["section"] == "Ö"]
        ).most_common()

    return {
        "boulder": {
            "green": stats_boulder.get("green", 0),
            "yellow": stats_boulder.get("yellow", 0),
            "blue": stats_boulder.get("blue", 0),
            "purple": stats_boulder.get("purple", 0),
            "red": stats_boulder.get("red", 0),
            "brown": stats_boulder.get("brown", 0),
            "black": stats_boulder.get("black", 0),
            "white": stats_boulder.get("white", 0),
        },
        "stokt": {
            "green": stats_stokt.get("green", 0),
            "yellow": stats_stokt.get("yellow", 0),
            "blue": stats_stokt.get("blue", 0),
            "purple": stats_stokt.get("purple", 0),
            "red": stats_stokt.get("red", 0),
            "brown": stats_stokt.get("brown", 0),
            "black": stats_stokt.get("black", 0),
            "white": stats_stokt.get("white", 0),
        },
    }
