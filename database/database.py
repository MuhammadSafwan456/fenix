from pymongo import MongoClient
from config.config import DB_HOST, DB_NAME, DB_PORT

client = MongoClient(DB_HOST, DB_PORT)

db = client[DB_NAME]


def database_write_one(collection, data):
    db_collection = db[collection]
    db_collection.insert_one(data)


def database_read_one(collection, read_filter):
    data = None
    db_collection = db[collection]
    data = db_collection.find_one(read_filter)
    return data


def database_find_and_modify(collection, read_filter, update_filter, **kwargs):
    data = None
    db_collection = db[collection]
    data = db_collection.find_one_and_update(read_filter, update_filter, **kwargs)
    return data
