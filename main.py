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

# Warnings ko permanent file mein save karenge
WARNINGS_FILE = "warnings.txt"

def get_warnings():
    if not os.path.exists(WARNINGS_FILE): return {}
    data = {}
    with open(WARNINGS_FILE, "r") as f:
        for line in f:
            uid, count = line.strip().split(":")
            data[uid] = int(count)
    return data

def save_warning(user_id, count):
    warnings = get_warnings()
    warnings[user_id] = count
    with open(WARNINGS_FILE, "w") as f:
        for uid, c in warnings.items():
            f.write(f"{uid}:{c}\n")

async def check_if_i_replied(user_id):
    async for message in client.iter_messages(int(user_id), limit=5):
        if message.out: return True
    return False

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    if await check_if_i_replied(user_id): return 

    # Warnings load karo
    warnings = get_warnings()
    count = warnings.get(user_id, 0) + 1
    save_warning(user_id, count)

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
            # Block hone ke baad warning reset
            save_warning(user_id, 0)
            print(f"BLOCKED: {user_id}")
        except Exception as e:
            print(f"BLOCK ERROR: {e}")

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
