from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest, GetContactsRequest
from telethon.tl.types import User

import asyncio
import logging
import time

import config
import database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("UserProtectBOT")


client = TelegramClient(
    "userprotect",
    config.API_ID,
    config.API_HASH
)


print("=" * 60)
print("🚩 UserProtectBOT v2 Starting...")
print("=" * 60)


# -----------------------------
# Helpers
# -----------------------------

async def is_contact(user_id):

    try:

        contacts = await client(GetContactsRequest(hash=0))

        for user in contacts.users:

            if user.id == user_id:
                return True

        return False

    except Exception as e:

        logger.error(e)

        return False


def log(text):

    if config.ENABLE_LOGS:
        print(text)


async def enable_after_timeout(user_id):

    await asyncio.sleep(config.REPLY_TIMEOUT)

    database.enable_protection(user_id)

   log(f"Protection Enabled Again -> {user_id}")

# -----------------------------
# Incoming Messages
# -----------------------------

@client.on(events.NewMessage(incoming=True))
async def incoming_handler(event):

    # Sirf Private Chat
    if not event.is_private:
        return

    sender = await event.get_sender()

    # Bots ignore
    if getattr(sender, "bot", False):
        return

    # Apne khud ke messages ignore
    if event.out:
        return

    # Contacts ignore
    if config.IGNORE_CONTACTS:
        if await is_contact(sender.id):
            return

    # User Database me add karo
    database.add_user(
        sender.id,
        sender.username if sender.username else "",
        sender.first_name if sender.first_name else ""
    )

    user = database.get_user(sender.id)

    if user is None:
        return

    # Protection OFF hai to kuch mat karo
    if user[4] == 0:
        return

    count = user[3] + 1

    database.update_count(sender.id, count)

    log("=" * 50)
    log(f"📩 New Message From : {sender.first_name}")
    log(f"🆔 User ID : {sender.id}")
    log(f"📨 Message Count : {count}")

    # -----------------------------
    # First Warning
    # -----------------------------
    if count == 1:

        await event.reply(config.FIRST_WARNING)

        log("✅ First Warning Sent")

    # -----------------------------
    # Second Warning
    # -----------------------------
    elif count == 2:

        await event.reply(config.SECOND_WARNING)

        log("⚠️ Second Warning Sent")

    # -----------------------------
    # Third Message = Block
    # -----------------------------
    elif count >= config.MAX_MESSAGES:

        await event.reply(config.FINAL_WARNING)

       await client(BlockRequest(id=sender.id))

        database.reset_count(sender.id)

        log("🚫 User Blocked Successfully")# -----------------------------
# Outgoing Messages (Your Reply)
# -----------------------------

@client.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):

    if not event.is_private:
        return

    # Sirf reply par protection OFF hogi
    if not event.is_reply:
        return

    reply = await event.get_reply_message()

    if reply is None:
        return

    user_id = reply.sender_id

    database.disable_protection(user_id)
    database.reset_count(user_id)
    database.update_reply_time(user_id, int(time.time()))

    log("=" * 50)
    log(f"💬 You Replied : {user_id}")
    log("🛡 Protection Disabled For 10 Minutes")

    asyncio.create_task(enable_after_timeout(user_id))


# -----------------------------
# Startup
# -----------------------------

async def main():

    print("✅ Connected Successfully")
    print("🚩 UserProtectBOT v2 Running...")
    print("=" * 60)

    await client.run_until_disconnected()


if __name__ == "__main__":

    client.start()

    client.loop.run_until_complete(main())
