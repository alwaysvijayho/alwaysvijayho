from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
from flask import Flask
from threading import Thread
import asyncio

# Web server setup (Render ke liye zaroori hai)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

# APNI API DETAILS YAHAN DALEIN
api_id =36700447  # Yahan apna api_id likhein
api_hash = '093117f52d27c69643b26eb2f16a2015' # Yahan apna api_hash likhein

# Filename ko 'userprotect' se hata kar '/etc/secrets/userprotect.session' kar dein
client = TelegramClient('userprotect', api_id, api_hash)

# Message blocking logic
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        sender = await event.get_sender()
        print(f"New message from: {sender.id}")
        
        # Yahan condition hai: Agar koi bhi message aaye toh block karega
        # Agar aap chahte hain ki sirf specific word pe block ho, toh if condition badal lein
        try:
            print(f"Blocking user: {sender.id}")
            await client(BlockRequest(sender.id))
            # Optional: Aap chaho toh block karne ke baad kuch reply bhi bhej sakte ho
            # await event.reply("Aapne limit exceed kar di hai.") 
        except Exception as e:
            print(f"Error blocking user: {e}")

# Bot ko background mein chalane ka function
def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    # Bot ko thread mein start karein
    Thread(target=run_bot).start()
    # Flask app ko start karein
    app.run(host='0.0.0.0', port=10000)
