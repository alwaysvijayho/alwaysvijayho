import json
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

# Warnings ko cloud (Saved Messages) mein store karenge
async def get_warnings_from_cloud():
    try:
        async for msg in client.iter_messages('me', search='WARN_DATA:'):
            return json.loads(msg.text.replace('WARN_DATA:', ''))
    except: return {}
    return {}

async def save_warnings_to_cloud(data):
    # Purana message delete karke naya save karenge
    async for msg in client.iter_messages('me', search='WARN_DATA:'):
        await msg.delete()
    await client.send_message('me', 'WARN_DATA:' + json.dumps(data))

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    # Check: Kya maine reply diya?
    async for msg in client.iter_messages(sender.id, limit=3):
        if msg.out: return 

    # Cloud se data lo
    data = await get_warnings_from_cloud()
    count = data.get(user_id, 0) + 1
    data[user_id] = count
    await save_warnings_to_cloud(data)

    if count == 1:
        await event.reply("✨ Hello! Main abhi offline hoon. Message chhod dein.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai!")
    elif count >= 4:
        await event.reply("🚫 Spamming ke karan block.")
        await client(BlockRequest(sender))
        data[user_id] = 0
        await save_warnings_to_cloud(data)

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
