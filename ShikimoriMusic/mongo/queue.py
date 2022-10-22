from ShikimoriMusic.mongo import db

pytgdb = db.pytg
admindb = db.admin

def get_active_chats() -> list:
    chats_list = []
    for chat in pytgdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

def is_active_chat(chat_id: int) -> bool:
    chat = pytgdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

def add_active_chat(chat_id: int):
    is_served = is_active_chat(chat_id)
    if is_served:
        return
    return pytgdb.insert_one({"chat_id": chat_id})

def remove_active_chat(chat_id: int):
    is_served = is_active_chat(chat_id)
    if not is_served:
        return
    return pytgdb.delete_one({"chat_id": chat_id})

def is_music_playing(chat_id: int) -> bool:
    chat = admindb.find_one({"chat_id_toggle": chat_id})
    if not chat:
        return True
    return False

def music_on(chat_id: int):
    is_karma = is_music_playing(chat_id)
    if is_karma:
        return
    return admindb.delete_one({"chat_id_toggle": chat_id})

def music_off(chat_id: int):
    is_karma = is_music_playing(chat_id)
    if not is_karma:
        return
    return admindb.insert_one({"chat_id_toggle": chat_id})
