# Import Firebase REST API library
from .helpers import DB, where, lumo_to_grade
from .config import settings
import firebase
from tinydb.operations import delete


async def refresh_lumo():
    print("going to fetch from lumo")
    try:
        async with DB as db:
            db.update(delete("holds"), where("section") == "L")
    except Exception as ex:
        print(f"failed with {ex}")

    print("finished first update")
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

    db = app.firestore()

    for document_id in db.collection("problems").list_of_documents():
        document = db.collection("problems").document(document_id).get()
        user_document = db.collection("users").document(document["userID"]).get()
        holds_raw = document.get("holds", [])
        holds = [(x, y) for x, y in zip(holds_raw[0::2], holds_raw[1::2])]
        name = document.get("name", "n/a")
        data = {
            "lumo_id": document_id,
            "section": "L",
            "name": name,
            "grade": lumo_to_grade(document.get("setterGrade", 0)),
            "lumo_holds": holds,
            "setter": user_document["username"],
            "created": "{0:%Y-%m-%dT%H:%M:%S}".format(document["createdDate"]),
        }
        print(f"fetched problem {name} with lumo_id {document_id}")
        print(data)
        async with DB as db:
            try:
                db.upsert(data, where("lumo_id") == data["lumo_id"])
            except Exception as ex:
                print(f"failed with {ex}")
    print("finished fetching from lumo")


if __name__ == "__main__":
    refresh_lumo()
