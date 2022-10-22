from ShikimoriMusic.mongo import db

chatsdb = db.chats
blacklist_chatdb = db.blacklistChat

def is_served_chat(chat_id: int) -> bool:
    chat = chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

def get_served_chats() -> list:
    chats_list = []
    for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


def add_served_chat(chat_id: int):
    is_served = is_served_chat(chat_id)
    if is_served:
        return
    return chatsdb.insert_one({"chat_id": chat_id})


def remove_served_chat(chat_id: int):
    is_served = is_served_chat(chat_id)
    if not is_served:
        return
    return chatsdb.delete_one({"chat_id": chat_id})


def blacklisted_chats() -> list:
    chats = blacklist_chatdb.find({"chat_id": {"$lt": 0}})
    return [chat["chat_id"] for chat in chats.to_list(length=1000000000)]


def blacklist_chat(chat_id: int) -> bool:
    if not blacklist_chatdb.find_one({"chat_id": chat_id}):
        blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False


def whitelist_chat(chat_id: int) -> bool:
    if blacklist_chatdb.find_one({"chat_id": chat_id}):
        blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False
