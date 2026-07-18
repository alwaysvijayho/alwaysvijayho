import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

FIRST_WARNING = """
🙏 Har Har Mahadev! 🚩

Main is samay vyast hoon.

Kripya apna message ek hi baar bhej dijiye aur mere reply ka dhairya se intezar karein.

Dhanyavaad. 🙏
"""

SECOND_WARNING = """
🙏 Har Har Mahadev! 🚩

⚠️ Warning (2/3)

Aap lagataar messages bhej rahe hain.

Kripya spam na karein.

Agla message bhejne par aap automatically block ho jayenge.
"""

FINAL_WARNING = """
🙏 Har Har Mahadev! 🚩

🚫 Auto Block

Aapne warnings ko ignore kiya.

Spam se suraksha ke liye aapko automatically block kar diya gaya hai.

Dhanyavaad.
"""

MAX_MESSAGES = 3
REPLY_TIMEOUT = 600
ENABLE_LOGS = True
IGNORE_CONTACTS = True
