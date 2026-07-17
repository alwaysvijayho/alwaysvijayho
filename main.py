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
WHITELIST_FILE = "whitelist.txt"

def get_whitelist():
    if not os.path.exists(WHITELIST_FILE): return set()
    with open(WHITELIST_FILE, "r") as f:
        return set(line.strip() for line in f)

# Yeh function check karega ki kya aapne user ko reply diya hai
async def check_if_i_replied(user_id):
    async for message in client.iter_messages(int(user_id), limit=5):
        if message.out: # Agar aapka koi bhi message wahan gaya hai
            return True
    return False

user_warnings = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    # 1. Check history: Kya aapne pehle reply diya hai?
    if await check_if_i_replied(user_id):
        return 

    # 2. Warning Logic
    user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
    count = user_warnings[user_id]

    if count == 1:
        await event.reply("✨ Hello! Har Har Mahadev. Main abhi offline hoon. Agar urgent kaam hai toh message chhod dein. ⚠️ Meow Meow.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Ye ek automated system hai. Please wait karein, baar-baar message karne par block kar diye jayenge.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye meri akhri warning hai. Spamming rok dein, varna agle message par block ho jayenge.")
    elif count >= 4:
        try:
            await event.reply("🚫 Aapne spamming jari rakhi, isliye bot ne aapko block kar diya hai.")
            await client(BlockRequest(sender))
            print(f"BLOCKED: {user_id}")
        except Exception as e:
            print(f"BLOCK ERROR: {e}")

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)