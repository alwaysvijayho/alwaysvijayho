import json
import os
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"

api_id = 36700447 
api_hash = '093117f52d27c69643b26eb2f16a2015' 
client = TelegramClient('userprotect', api_id, api_hash)

DATA_FILE = "user_data.json"

# Data load aur save karne ka tareeka
def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def check_if_i_replied(user_id):
    async for message in client.iter_messages(int(user_id), limit=5):
        if message.out: return True
    return False

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    # Whitelist check
    if await check_if_i_replied(user_id): return 

    # Warnings handle karo
    data = load_data()
    warnings = data.get(user_id, 0) + 1
    data[user_id] = warnings
    save_data(data)

    if warnings == 1:
        await event.reply("✨ Hello! Har Har Mahadev. Main abhi offline hoon. Message chhod dein. ⚠️")
    elif warnings == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein, varna block kar diye jayenge.")
    elif warnings == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai. Spamming rokein!")
    elif warnings >= 4:
        try:
            await event.reply("🚫 Spamming ke karan aapko block kiya jata hai.")
            await client(BlockRequest(sender))
            # Block hone ke baad user ko data se hata do
            del data[user_id]
            save_data(data)
            print(f"BLOCKED: {user_id}")
        except Exception as e:
            print(f"BLOCK ERROR: {e}")

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
