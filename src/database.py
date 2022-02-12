from pymongo import MongoClient
from bson.objectid import ObjectId

from config import MONGODB_DB_NAME, MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

def find_all_rules():
    docs = []
    rules = db.rules.find()
    for rule in rules:
        rule["_id"] = str(rule["_id"])
        docs.append(rule)

    return docs


def insert_rule(rule: dict):
    doc = db.rules.insert_one(rule)
    return doc


def update_rule(rule_id: str, new_rule: dict):
    db.rules.update_one({"_id": ObjectId(rule_id)}, {"$set": new_rule}, upsert=False)

    # find one rule by id from doc then return it
    doc = db.rules.find_one({"_id": ObjectId(rule_id)})

    return doc


def delete_rule(rule_id):
    deleted = db.rules.delete_one({"_id": ObjectId(rule_id)})
    count = deleted.deleted_count

    return count
