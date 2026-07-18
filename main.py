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

    # Check if I have already replied (Reset logic)
    async for msg in client.iter_messages(user_id, limit=5):
        if msg.out:
            warnings[user_id] = 0  # Aapka reply aate hi count reset
            return

    # Update count
    warnings[user_id] = warnings.get(user_id, 0) + 1
    count = warnings[user_id]

    # Female Tone Warnings
    if count == 1:
        await event.reply("🙏 Har Har Mahadev! Main abhi busy hoon aur offline hoon. Aap apna message chhod dijiye, main free hokar reply karungi.")
    elif count == 2:
        await event.reply("⚠️ Warning 2/3: Kripya baar-baar message karke spam na karein. Main busy hoon, thoda dhairya rakhein.")
    elif count == 3:
        await event.reply("⚠️ Warning 3/3: Ye meri aakhri warning hai! Kripya spamming band karein, varna mujhe majboor hokar aapko block karna padega.")
    elif count >= 4:
        await event.reply("🚫 Aapne meri warning ignore ki, isliye ab aap block ho chuke hain.")
        await client(BlockRequest(sender))
        warnings[user_id] = 0 # Block karne ke baad reset

def run_bot():
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
