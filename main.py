from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
import asyncio
import database
import config
from flask import Flask
from threading import Thread

# Web server setup (Render ke liye)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

api_id = 36700447
api_hash = '093117f52d27c69643b26eb2f16a2015'
client = TelegramClient('userprotect', api_id, api_hash)

# (Aapke baaki handlers wahi rahenge jo aapne upar diye hain)
# ... [Yahan apne incoming_handler aur outgoing_handler wahi paste karein] ...

# Bot ko background mein chalane ka function
def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    # Bot ko ek nayi thread mein shuru karein
    Thread(target=run_bot).start()
    # Flask server ko port 10000 par run karein
    app.run(host='0.0.0.0', port=10000)
