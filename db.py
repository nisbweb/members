import pymongo
import os

client = pymongo.MongoClient(os.environ["MONGO"], connect=False)
db = client.main


def get_members(page_no=None, no_items=50):
    members = []
    if page_no:
        ms = db.members.find().skip((page_no-1)*no_items).limit(no_items)
    else:
        ms = db.members.find()
    for m in ms:
        m.pop("_id")
        members.append(m)
    if len(members) > 0:
        return members
    else:
        return None


def get_member(email):
    member = db.members.find_one({"email": email})
    if member:
        member.pop("_id")
        return member
    return None


def add_member(member_dict):
    db.members.insert_one(member_dict)


def delete_member(email):
    db.members.delete_one({"email": email})


def update_member(member_dict):
    email = member_dict["email"]
    db.members.find_one_and_replace({"email": email}, member_dict)
