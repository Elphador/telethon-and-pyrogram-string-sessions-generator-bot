
from pyrogram import Client
from pyroaddon import listen
import os
API_ID = 18802415
API_HASH = "a8993f96404fd9a67de867586b3ddc92"
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Client(":memory:",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)
