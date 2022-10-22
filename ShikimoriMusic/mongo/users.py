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
