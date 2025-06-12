import os, utils, pymongo
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
myclient = pymongo.MongoClient(DATABASE_URL)
mydb  = myclient["urls_db"]
mycol = mydb["urls"]

def generate_code() -> str:
    while True:
        code = utils.generate_slug()
        if not mycol.find_one({"short": code}):
            return code

def save(long_url: str) -> dict:
    doc = mycol.find_one({"long": long_url})    
    if doc:
        return doc         

    doc = {
        "long": long_url,
        "short": generate_code(),
        "createdAt": datetime.now(timezone.utc),
        "accessCount": 0,
    }
    mycol.insert_one(doc)
    return doc

def find(code: str) -> dict | None:
    return mycol.find_one({"short": code})

def update(code: str, new_long: str) -> dict | None:
    res = mycol.find_one_and_update(
        {"short": code},
        {"$set": {"long": new_long, "updatedAt": datetime.now(timezone.utc)}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    return res

def delete(code: str) -> bool:
    return mycol.delete_one({"short": code}).deleted_count > 0

def inc_counter(code: str):
    mycol.update_one({"short": code}, {"$inc": {"accessCount": 1}})
