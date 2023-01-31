import json
from functools import lru_cache
from aiotinydb import AIOTinyDB
from tinydb import where
from tinydb.operations import set as tinydb_set
from .config import settings

# the database instance
DB = AIOTinyDB(settings.problem_db_file)

# stökt setup of hold path definitions
@lru_cache
def get_stokt_setup():
    with open("setup.json", "r") as f:
        return {h["id"]: h for h in json.load(f)["holds"]}


# get a string with hold ids seperated by space - and yield {"path": path, "type": class}
def holds_to_paths(holds_str):
    HOLDS_PATH = get_stokt_setup()
    holds = holds_str.split(" ")
    starting_hold_count = sum([1 if hold.startswith("S") else 0 for hold in holds])
    for hold in holds:
        sw = hold[0]
        hit = int(hold[1:]) if sw.isalpha() else (int(hold))
        yield {
            "path": HOLDS_PATH[hit]["pathStr"],
            "type": "foot" if sw == "F" else "hand",
        }
        if sw == "S" and starting_hold_count == 1:
            yield {"path": "M" + HOLDS_PATH[hit]["leftTapeStr"], "type": "hand"}
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
