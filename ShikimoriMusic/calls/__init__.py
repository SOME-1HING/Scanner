from os import listdir, mkdir
from pyrogram import Client
from ShikimoriMusic import vars
from ShikimoriMusic.calls.queues import clear, get, is_empty, put, task_done
from ShikimoriMusic.calls import queues
from ShikimoriMusic.calls.youtube import download
from ShikimoriMusic.calls.calls import run, pytgcalls
from ShikimoriMusic.calls.calls import client

if "raw_files" not in listdir():
    mkdir("raw_files")

from ShikimoriMusic.calls.convert import convert
