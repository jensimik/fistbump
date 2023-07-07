# Import Firebase REST API library
import itertools

import firebase
from tinydb.operations import delete

from .config import settings
from .helpers import DB, lumo_to_grade, where


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

    # Firebase Authentication
    auth = app.auth()

    # Create new user and sign in
    user = auth.sign_in_with_email_and_password(
        settings.lumo_username, settings.lumo_password
    )

    fire_db = app.firestore()

    for document_id in fire_db.collection("problems").list_of_documents():
        try:
            document = fire_db.collection("problems").document(document_id).get()
            user_document = (
                fire_db.collection("users").document(document["userID"]).get()
            )
            holds_raw = document.get("holds", [])
            hands_index = holds_raw.index(255)
            hands = list(itertools.pairwise(holds_raw[:hands_index]))
            feet_index = holds_raw.index(255, hands_index + 1)
            feet = list(itertools.pairwise(holds_raw[hands_index + 1 : feet_index]))
            sf_index = holds_raw.index(255, feet_index + 1)
            sf = list(itertools.pairwise(holds_raw[feet_index + 1 : sf_index]))
            name = document.get("name", "n/a")
            data = {
                "lumo_id": document_id,
                "section": "L",
                "name": name,
                "grade": lumo_to_grade(document.get("setterGrade", 0)),
                "lumo_hands": hands,
                "lumo_feet": feet,
                "lumo_sf": sf,
                "setter": user_document["username"],
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
