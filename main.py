from telethon import TelegramClient, events
from telethon.tl.functions.contacts import (
    BlockRequest,
    GetContactsRequest
)

import asyncio
import logging
import time

import config
import database


# ==========================
# Logging
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("UserProtectBOT")


# ==========================
# Telegram Client
# ==========================

client = TelegramClient(
    "userprotect",
    config.API_ID,
    config.API_HASH
)


print("=" * 60)
print("🚩 UserProtectBOT v2 Starting...")
print("=" * 60)


# ==========================
# Helper Functions
# ==========================

def log(message):
    if config.ENABLE_LOGS:
        print(message)


async def is_contact(user_id):
    """
    Return True if user exists in contacts.
    """

    try:

        contacts = await client(GetContactsRequest(hash=0))

        for user in contacts.users:

            if user.id == user_id:
                return True

        return False

    except Exception as e:

        logger.error(e)

        return False


async def enable_after_timeout(user_id):
    """
    Re-enable protection after timeout.
    """

    await asyncio.sleep(config.REPLY_TIMEOUT)

    database.enable_protection(user_id)

    log(f"🛡 Protection Enabled Again -> {user_id}")


def get_message_count(user):

    return user[3]


def protection_enabled(user):
    return user[4] == 1


# ==========================
# Incoming Messages
# ==========================

@client.on(events.NewMessage(incoming=True))
async def incoming_handler(event):

    # Sirf private chats
    if not event.is_private:
        return

    sender = await event.get_sender()

    # Bots ignore
    if getattr(sender, "bot", False):
        return

    # Khud ke outgoing messages ignore
    if event.out:
        return

    # Contacts ignore
    if config.IGNORE_CONTACTS:
        if await is_contact(sender.id):
            return

    # Database me user add karo
    database.add_user(
        sender.id,
        sender.username or "",
        sender.first_name or ""
    )

    user = database.get_user(sender.id)

    if user is None:
        return

    # Protection OFF hai to kuch mat karo
    if not protection_enabled(user):
        return

    count = get_message_count(user) + 1

    database.update_count(sender.id, count)

    log("=" * 60)
    log(f"📩 New DM : {sender.first_name}")
    log(f"🆔 User ID : {sender.id}")
    log(f"📨 Count : {count}")

    # -----------------------------
    # Warning 1
    # -----------------------------
    if count == 1:

        await event.reply(config.FIRST_WARNING)

        log("✅ First Warning Sent")
        return

    # -----------------------------
    # Warning 2
    # -----------------------------
    if count == 2:

        await event.reply(config.SECOND_WARNING)

        log("⚠️ Second Warning Sent")
        return

  # -----------------------------
# Third Message = Block
# -----------------------------
if count >= config.MAX_MESSAGES:

    await event.reply(config.FINAL_WARNING)

    try:
        await client(BlockRequest(id=sender.id))

        database.disable_protection(sender.id)
        database.reset_count(sender.id)

        log("🚫 User Blocked Successfully")

    except Exception as e:
        logger.error(f"Block Error : {e}")
# ==========================
# Outgoing Messages
# ==========================

@client.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):

    if not event.is_private:
        return

    user = await event.get_chat()

    database.add_user(
        user.id,
        getattr(user, "username", "") or "",
        getattr(user, "first_name", "") or ""
    )

    database.disable_protection(user.id)
    database.reset_count(user.id)
    database.update_reply_time(user.id, int(time.time()))

    log("=" * 60)
    log(f"💬 You replied to : {user.id}")
    log("🛡 Protection Disabled")

    asyncio.create_task(enable_after_timeout(user.id))


# ==========================
# Startup
# ==========================

async def main():

    print("✅ Connected Successfully")
    print("🚩 UserProtectBOT v2 Running...")
    print("=" * 60)

    await client.run_until_disconnected()


if __name__ == "__main__":

    client.start()

    client.loop.run_until_complete(main())
