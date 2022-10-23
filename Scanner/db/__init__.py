import asyncio
import sys

from motor import motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from Scanner import LOGGER
from Scanner.vars import MONGO_DB_URI 


client = MongoClient()
client = MongoClient(MONGO_DB_URI, 27017)["Scanner"]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, 27017)
db = motor["Scanner"]
db = client["Scanner"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(LOGGER.critical("Can't connect to mongodb! Exiting..."))