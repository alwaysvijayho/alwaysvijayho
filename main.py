import asyncio
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

# Cloud se warn count lena
async def get_warn_count(user_id):
    async for msg in client.iter_messages('me', search=f"WARN:{user_id}:"):
        return int(msg.text.split(":")[2])
    return 0

# Cloud par warn count save karna
async def save_warn_count(user_id, count):
    # Purana record delete karo
    async for msg in client.iter_messages('me', search=f"WARN:{user_id}:"):
        await msg.delete()
    # Naya record save karo
    if count > 0:
        await client.send_message('me', f"WARN:{user_id}:{count}")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    # Agar maine pehle reply diya hai, toh stop
    async for msg in client.iter_messages(sender.id, limit=3):
        if msg.out: return

    # Count badhao
    count = await get_warn_count(user_id) + 1
    await save_warn_count(user_id, count)

    # Messages
    if count == 1:
        await event.reply("✨ Hello! Har Har Mahadev. Main abhi offline hoon. Message chhod dein.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai!")
    elif count >= 4:
        await event.reply("🚫 Spamming ke karan block.")
        await client(BlockRequest(sender))
        await save_warn_count(user_id, 0) # Reset

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
