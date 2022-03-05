import os
from datetime import datetime
# import datetime as dt
from dateutil import tz
# from main import auction_channel

def get_token():
  token = os.getenv("TOKEN")
  return (token)

reset = '\u001b[0m'
red = '\u001b[31m'
green = '\u001b[32m'

tzstr = "EST"
tz = tz.gettz(tzstr)

POPULAR_LAB_ICON_URL = "https://i.imgur.com/Oa929It.png"
AUCTION_CATEGORY_ID = 949619006829113354
AUCTION_ROLES = [929405912794427453,929405779381993493,929405560435126392,929405327496069190]
GUILD_ID = 914573451329699880
INCREMENT_AMOUNT = 100
PR = "$"
def get_authorised_users():
  return ["Bunyod#0503"]

def now():
  return datetime.now(tz)

def sanitise(string):
  chars = ["!","@","#","$","%","^","&","*","(",")","+","=","[","]","{","}","'",'"',";",":","|","<",">",",",".","?","/"]
  for char in chars:
    string = string.replace(char, "")
  string = string.lower()
  return (string)