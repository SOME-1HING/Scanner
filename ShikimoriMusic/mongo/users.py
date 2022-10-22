from typing import Union
from ShikimoriMusic.mongo import db

usersdb = db.users

def is_served_user(user_id: int) -> bool:
    user = usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


def get_served_users() -> list:
    users_list = []
    for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


def add_served_user(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    return usersdb.insert_one({"user_id": user_id})

async def get_userid_by_name(username):
    for user in usersdb.find():
        if user["username"] == username.lower():
            return user["user_id"]
    for chat in usersdb.find():
        if chat.get("chat_username") == username.lower():
            return chat["chat_id"]


async def get_user_id(username: str) -> Union[int, None]:
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    user_id = await get_userid_by_name(username)

    if user_id:
        return user_id
    else:
        return None