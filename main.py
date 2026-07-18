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

FILE_PATH = "data.txt"

def update_warn(user_id, count):
    lines = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            lines = f.readlines()
    
    new_lines = []
    found = False
    for line in lines:
        if line.startswith(f"{user_id}:"):
            new_lines.append(f"{user_id}:{count}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"{user_id}:{count}\n")
        
    with open(FILE_PATH, "w") as f:
        f.writelines(new_lines)

def get_warn(user_id):
    if not os.path.exists(FILE_PATH): return 0
    with open(FILE_PATH, "r") as f:
        for line in f:
            if line.startswith(f"{user_id}:"):
                return int(line.split(":")[1])
    return 0

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    async for msg in client.iter_messages(sender.id, limit=3):
        if msg.out: return

    current_count = get_warn(user_id) + 1
    update_warn(user_id, current_count)

    if current_count == 1:
        await event.reply("✨ Hello! Har Har Mahadev. Main abhi offline hoon. Message chhod dein.")
    elif current_count == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein.")
    elif current_count == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai!")
    elif current_count >= 4:
        await event.reply("🚫 Blocked.")
        await client(BlockRequest(sender))
        update_warn(user_id, 0)

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
