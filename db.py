import pymongo
import os

client = pymongo.MongoClient(os.environ["MONGO"])
db = client.main

def get_member(email):
    member = db.members.find_one({"email":email})
    if member:
        member.pop("_id")
        return member
    return None

def add_member(member_dict):
    db.members.insert_one(member_dict)

def delete_member(email):
    db.members.delete_one({"email":email})

def update_member(member_dict):
    email = member_dict["email"]
    db.members.find_one_and_replace({"email":email},member_dict)