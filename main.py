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

# Global memory (taaki fast chale)
user_warnings = {}

async def load_warnings():
    global user_warnings
    async for msg in client.iter_messages('me', search='WARN_DATA:'):
        user_warnings = json.loads(msg.text.replace('WARN_DATA:', '')
        return
    user_warnings = {}

async def save_warnings():
    # Purane warning messages delete karo
    async for msg in client.iter_messages('me', search='WARN_DATA:'):
        await msg.delete()
    # Naya data save karo
    await client.send_message('me', 'WARN_DATA:' + json.dumps(user_warnings)

@client.on(events.NewMessage(incoming=True)
async def handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    user_id = str(sender.id)

    # 1. Reply check (History se)
    async for msg in client.iter_messages(sender.id, limit=3):
        if msg.out: return 

    # 2. Memory update
    await load_warnings()
    user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
    count = user_warnings[user_id]
    await save_warnings()

    # 3. Warnings
    if count == 1:
        await event.reply("✨ Hello! har har mahadev Main abhi offline hoon. Message chhod dein.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Dobara message na karein, varna block kar diye jayenge.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye akhri warning hai!")
    elif count >= 4:
        await event.reply("🚫 Spamming ke karan block.")
        await client(BlockRequest(sender))
        user_warnings[user_id] = 0 # Reset
        await save_warnings()

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
