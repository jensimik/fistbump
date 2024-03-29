import logging
from datetime import datetime, timedelta

import firebase
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from requests.exceptions import HTTPError

from .config import settings
from .helpers import DB, lumo_to_grade, where

log = logging.getLogger(__name__)


async def refresh_lumo():
    print("going to fetch from lumo")
    # Firebase configuration
    config = {
        "apiKey": settings.lumo_firebase_apikey,
        "authDomain": "send-app-4961e.firebaseapp.com",
        "databaseURL": "https://send-app-4961e.firebaseio.com",
        "projectId": "send-app-4961e",
        "storageBucket": "send-app-4961e.appspot.com",
        "messagingSenderId": "258508440101",
        "appId": "1:258508440101:web:e58b88c6dbb2acf7c8f5cc",
    }

    # Instantiates a Firebase app
    app = firebase.initialize_app(config)

    print("firebase init")

    # Firebase Authentication
    auth = app.auth()

    # Create new user and sign in
    auth.sign_in_with_email_and_password(settings.lumo_username, settings.lumo_password)

    fire_db = app.firestore()

    print("lumo signed in")

    offset = DatetimeWithNanoseconds.now() - timedelta(days=3)

    for raw_document in (
        fire_db.collection("problems")
        .order_by("createdDate")
        .start_at({"createdDate": offset})
        .limit_to_first(50)
        .get()
    ):
        [(document_id, document)] = raw_document.items()
        try:
            username = "n/a"
            try:
                user_document = (
                    fire_db.collection("users").document(document["userID"]).get()
                )
                username = user_document["username"]
            except HTTPError:
                log.info("could not get username of this problem")
            holds_raw = document.get("holds", [])
            hands_index = holds_raw.index(255)
            hands_raw = holds_raw[:hands_index]
            hands = list(zip(hands_raw[0::2], hands_raw[1::2]))
            feet_index = holds_raw.index(255, hands_index + 1)
            feet_raw = holds_raw[hands_index + 1 : feet_index]
            feet = list(zip(feet_raw[0::2], feet_raw[1::2]))
            sf_index = holds_raw.index(255, feet_index + 1)
            sf_raw = holds_raw[feet_index + 1 : sf_index]
            sf = list(zip(sf_raw[0::2], sf_raw[1::2]))
            name = document.get("name", "n/a")
            data = {
                "lumo_id": document_id,
                "section": "L",
                "name": name,
                "grade": lumo_to_grade(document.get("setterGrade", 0)),
                "lumo_hands": hands,
                "lumo_feet": feet,
                "lumo_sf": sf,
                "setter": username,
                "created": "{0:%Y-%m-%dT%H:%M:%S}".format(document["createdDate"]),
            }
            print(f"fetched problem {name} with lumo_id {document_id}")
            async with DB as db:
                try:
                    db.upsert(data, where("lumo_id") == data["lumo_id"])
                except Exception as ex:
                    print(f"failed with {ex}")
        except Exception as ex:
            print(f"failed with {ex}")
    print("finished fetching from lumo")


if __name__ == "__main__":
    refresh_lumo()
