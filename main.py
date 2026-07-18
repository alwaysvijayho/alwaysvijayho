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

# Temporary memory
warnings = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = sender.id

    # Check if already replied
    async for msg in client.iter_messages(user_id, limit=3):
        if msg.out: return

    # Update count
    warnings[user_id] = warnings.get(user_id, 0) + 1
    count = warnings[user_id]

    if count == 1:
        await event.reply("✨ Hello! Har Har Mahadev. Main abhi offline hoon. Message chhod dein.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai!")
    elif count >= 4:
        await event.reply("🚫 Spamming ke karan block.")
        await client(BlockRequest(sender))
        warnings[user_id] = 0

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
