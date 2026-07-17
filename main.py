from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
import asyncio
import database
import config 

api_id = 36700447  # Yahan apni ID daalein
api_hash = '093117f52d27c69643b26eb2f16a2015' # Yahan apna hash daalein

client = TelegramClient('userprotect', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def incoming_handler(event):
    if not event.is_private: return
    sender = await event.get_sender()
    if sender.bot: return

    database.add_user(sender.id)
    user = database.get_user(sender.id) # (id, count, protection)
    
    # Agar protection ON (1) hai, toh bot chup rahega
    if user[2] == 1: return

    new_count = user[1] + 1
    database.update_count(sender.id, new_count)

    if new_count == 1:
        await event.reply(config.FIRST_WARNING)
    elif new_count == 2:
        await event.reply(config.SECOND_WARNING)
    elif new_count >= 3:
        await event.reply(config.FINAL_MESSAGE)
        await client(BlockRequest(sender.id))
        database.reset_user(sender.id)

@client.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):
    if not event.is_private: return
    chat = await event.get_chat()
    
    # Aapne message bheja, toh Protection ON (1) kar do
    database.set_protection(chat.id, 1)
    
    # 10 minute (600 seconds) wait karo
    await asyncio.sleep(600)
    
    # 10 minute baad Protection OFF (0) kar do
    database.set_protection(chat.id, 0)

print("Bot is running perfectly...")
client.start()
client.run_until_disconnected()