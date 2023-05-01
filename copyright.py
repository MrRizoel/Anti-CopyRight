
import os
import sys
import time
import datetime

from pyrogram import filters, Client, idle
from pyrogram.types import Message
from pyrogram.enums import ChatType

from apscheduler.schedulers.background import BackgroundScheduler

#from database import adduser, addchat

API_ID = 3147700 
API_HASH = "e660ea4d20e70a3897aa8cf3a6dc60af"
BOT_TOKEN = "5702528336:AAGLMc4mVdmKdU34b9BCIz8EXTn2zuZwzic"
#DEVS = []

ALL_GROUPS = []
MEDIA_GROUPS = []
GROUP_MEDIAS = {}

RiZoeL = Client('Anti-CopyRight', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@RiZoeL.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   #adduser(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await rep.edit_text(f"🤖 **PONG**: `{ms}`ᴍs")

"""@RiZoeL.on_message(filters.user(Devs) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await RiZoeL.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()"""

@RiZoeL.on_message(filters.all)
async def watcher(_, message: Message):
   chat = message.chat
   if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
   
      if chat.id not in MEDIA_GROUPS:
         MEDIA_GROUPS.append(chat.id)
      if (message.video or message.photo):
         check = GROUP_MEDIAS.get(chat.id)
         if check:
            GROUP_MEDIAS[chat.id].append(message.id)
            print(f"Chat: {chat.title}, message ID: {message.id}")
      else:
         GROUP_MEDIAS[chat.id] = [message.id]

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return
    for i in MEDIA_GROUPS:
       message_list = list(GROUP_MEDIAS[i].values())
       try:
          RiZoeL.delete_messages(i, message_list)
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias ✓")
    print("waiting for 1 HR")

scheduler = BackgroundScheduler()
scheduler.add_job(AutoDelete, "interval", seconds=20)

scheduler.start()

def starter():
   print('starting bot...')
   RiZoeL.start()
   print('bot Started ✓')
   idle()

if __name__ == "__main__":
   starter()
