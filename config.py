import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

FIRST_WARNING = """ 
Hellow 
🙏 Har Har Mahadev! 🚩
jay shree shyam  

 
Main is samay vyast hoon.

Kripya apna message ek hi baar bhej dijiye aur mere reply ka dhairya se intezar karein.

" Meow Meow". 🙏
"""

SECOND_WARNING = """
🙏 Har Har Mahadev! 🚩
   jay shree shyam 

⚠️ Warning (2/3)

Aap lagataar messages bhej rahe hain.

Kripya spam na karein.

Agla message bhejne par aap automatically block ho  jaoge " Meow Meow" .
"""

FINAL_WARNING = """
🙏 Har Har Mahadev! 🚩
   jay shree shyam 

🚫 Auto Block

Aapne warnings ko ignore kiya.

Spam se suraksha ke liye aapko automatically block kar diya gaya hai.

" Meow Meow". 
"""

MAX_MESSAGES = 3
REPLY_TIMEOUT = 300
ENABLE_LOGS = True
IGNORE_CONTACTS = True
