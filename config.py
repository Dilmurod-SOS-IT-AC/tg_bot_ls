import os

from dotenv import load_dotenv

load_dotenv() # .env -> keys

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()] #111,222 -> [111, 222]

DATA_FILE = "data/db.json"
PHOTOS_DIR = "data/photos"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not defined, please chech .env file.")