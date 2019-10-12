import pymongo
import os
import error
import datetime

client = pymongo.MongoClient(os.environ["MONGO"], connect=False)
db = client.main


def get_members_count():
    return db.members.find().count()


def get_members(page_no=None, no_items=50):
    members = []
    if page_no:
        ms = db.members.find() \
            .skip((int(page_no)-1)*int(no_items)) \
            .limit(int(no_items))
    else:
        ms = db.members.find()
    for m in ms:
        m.pop("_id")
        members.append(m)
    if len(members) > 0:
        return members, None
    else:
        return None, error.ResourceNotFound("Members could not be found")


def get_member(email):
    member = db.members.find_one({"email": email})
    if member:
        member.pop("_id")
        return member, None
    return None, error.ResourceNotFound("Member could not be found")


def add_member(member_dict):
    try:
        m, err = get_member(member_dict["email"])
        if err:
            raise err
        return None, error.ResourceAlreadyExists("Member already exists")
    except error.ResourceNotFound:
        member_dict["scope"] = "member"
        member_dict["timestamp"] = datetime.datetime.today()
        return db.members.insert_one(member_dict), None


def delete_member(email):
    m, err = get_member(email)
    if err:
        return None, err
    return db.members.delete_one({"email": email}), None


def update_member(email, member_dict):
    m, err = get_member(email)
    if err:
        return None, err
    return db.members \
        .update_one({
            "email": email
        }, {
            "$set": member_dict
        }, upsert=True), None


def validate_member(member_dict):
    for k in ["email", "mobile", "name", "membership"]:
        if k not in member_dict.keys():
            return False
    for k in ["active", "isIEEE", "isCS"]:
        if k not in member_dict["membership"].keys():
            return False
    return True
