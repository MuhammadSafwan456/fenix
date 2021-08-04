from database import database
from bson.objectid import ObjectId
user_collection = "user"


def read_user_by_email(email):
    read_filter = {"email": email}
    user = database.database_read_one(user_collection, read_filter)
    return user


def read_user_by_id(_id):
    read_filter = {"_id": ObjectId(_id)}
    user = database.database_read_one(user_collection, read_filter)
    return user


def write_user(user):
    return database.database_write_one(user_collection, user)


def update_user_session_key(user, session_key):
    read_filter = {
        "email": user["email"]
    }
    update_filter = {
        "$set": {
            "session_key": session_key
        }
    }

    database.database_find_and_modify(user_collection, read_filter, update_filter)
