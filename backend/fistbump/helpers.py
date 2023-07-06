import json
import shutil
from datetime import datetime
from functools import lru_cache
from itertools import cycle
from PIL import Image, ImageOps
from aiotinydb import AIOTinyDB
from tinydb import where
from tinydb.operations import set as tinydb_set
from .config import settings

# the database instance(s)
DB = AIOTinyDB(settings.problem_db_file)
DB_user = AIOTinyDB(settings.user_db_file)


async def maintenance():
    # clean out stale images
    pass
    # async with DB as db:
    #     hexes = [d["image_hex"] for d in db if "image_hex" in d]
    #     for p in settings.images_directory.iterdir:
    #         if p.suffix == "jpg":
    #             if p.stem not in hexes:
    #                 p.unlink()


# def jpg_to_webp(hex, remove_jpg=True):
#     webp_filename = settings.images_directory / hex / "original.webp"
#     webp800_filename = settings.images_directory / hex / "800.webp"
#     jpg_filename = settings.images_directory / hex / "original.jpg"
#     with Image.open(jpg_filename) as im:
#         # rotate it before save as webp don't have the exif about rotation
#         im = ImageOps.exif_transpose(im)
#         im.save(webp_filename, format="webp", method=6, quality=40)
#         width, height = im.size
#         new_height = int(800 * height / width)
#         im.thumbnail((800, new_height))
#         im.save(webp800_filename, format="webp", method=6, quality=50)
#     if remove_jpg:
#         jpg_filename.unlink(missing_ok=True)


# stökt setup of hold path definitions
@lru_cache
def get_stokt_setup():
    with open("setup.json", "r") as f:
        return {h["id"]: h for h in json.load(f)["holds"]}


# get a string with hold ids seperated by space - and yield {"path": path, "type": class}
def holds_to_paths(holds_str):
    HOLDS_PATH = get_stokt_setup()
    holds = holds_str.split(" ")
    leftrightcycle = cycle(["leftTapeStr", "rightTapeStr"])
    starting_hold_count = sum([1 if hold.startswith("S") else 0 for hold in holds])
    for hold in holds:
        sw = hold[0]
        hit = int(hold[1:]) if sw.isalpha() else (int(hold))
        yield {
            "path": HOLDS_PATH[hit]["pathStr"],
            "type": "foot" if sw == "F" else "hand",
        }
        if sw == "S":
            if starting_hold_count == 1:
                yield {"path": "M" + HOLDS_PATH[hit]["leftTapeStr"], "type": "hand"}
                yield {"path": "M" + HOLDS_PATH[hit]["rightTapeStr"], "type": "hand"}
            elif starting_hold_count == 2:
                yield {
                    "path": "M" + HOLDS_PATH[hit][next(leftrightcycle)],
                    "type": "hand",
                }
        elif sw == "T":
            yield {"path": "M" + HOLDS_PATH[hit]["topPolygonStr"], "type": "hand"}


# grade to color TODO: needs update!
GRADE_TO_COLOR = {
    "?": "turquoise",
    "4": "green",
    "4+": "green",
    "5": "green",
    "4-5A": "green",
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


def lumo_to_grade(lumo_grade) -> str:
    grades = [
        "4",
        "5",
        "5+",
        "6A",
        "6A+",
        "6B",
        "6B+",
        "6C",
        "6C+",
        "7A",
        "7A+",
        "7B",
        "7B+",
        "7C",
        "7C+",
        "8A",
        "8A+",
        "8B",
        "8B+",
        "8C",
        "8C+",
        "9A",
    ]
    return grades[lumo_grade]


def local_now():
    return datetime.now(tz=settings.tz).replace(tzinfo=None)
