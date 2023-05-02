
import os
import re
import sys
import time
import datetime
import random 
import asyncio

from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

from apscheduler.schedulers.background import BackgroundScheduler

from database import adduser, addchat

API_ID = 3147700 
API_HASH = "e660ea4d20e70a3897aa8cf3a6dc60af"
BOT_TOKEN = "5702528336:AAGRZjzP-KzL-DEgjqScLPeJC8zs3RWJIEU"
DEVS = [1854700253]

ALL_GROUPS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
"1 Hour complete, I'm doing my work...",
"Its time to delete all medias!",
"No one can Copyright until I'm alive 😤",
"Hue hue, let's delete media...",
"I'm here to delete medias 🙋", 
]
DELETE_DONE = [
"😮‍💨 Finally i delete total {} medias"
"Great work done by me 🥲 Medias: {}",
"All media cleared! total {}",
"hue hue {} medias deleted by me 😮‍💨",
"🥲 {} medias....",
"it's hard to delete {} medias 🙄",
]

START_MESSAGE = """
**Hello {}, I'm Anti - CopyRight Bot**

 > **I can save your groups from Copyrights 😉**

 **Work:** I'll Delete all medias of your group every 1 hour 😮‍💨
 
 **Process?:** Simply add me in your group and promote as admin with delete messages right!
"""

BUTTON = [[InlineKeyboardButton("+ Add me in group +", url="http://t.me/AntiCopyRightRobot?startgroup=s&admin=delete_messages")]]

RiZoeL = Client('RiZoeL-Anti-CopyRight', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@RiZoeL.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   adduser(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await rep.edit_text(f"🤖 **PONG**: `{ms}`ᴍs")

@RiZoeL.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
   adduser(message.from_user.id)
   await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(BUTTON))

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await RiZoeL.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
   wait = await message.reply("Fetching.....")
   stats = "**Here is total stats of me!** \n\n"
   stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
   stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
   stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
   #stats += f"**© @Team6Teen**"
   await wait.edit_text(stats)

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["broadcast", "gcast"]))
async def gcast_(_, e: Message):
    txt = ' '.join(e.command[1:])
    if txt:
        msg = str(txt)
        buttons = None
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
        if e.reply_to_message.reply_markup:
           buttons = e.reply_to_message.reply_markup
        else:
           buttons = None
    else:
        await e.reply_text("Give Message for Broadcast or reply to any msg")
        return

    Han = await e.reply_text("Broadcasting...")
    err = 0
    dn = 0
    for x in ALL_GROUPS:
       try:
          await RiZoeL.send_message(chat_id=x, text=msg, reply_markup=buttons)
          await asyncio.sleep(1)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")

   
@RiZoeL.on_message(filters.command(["anticopyright", "copyright"]))
async def enable_disable(_, message: Message):
   chat = message.chat
   txt = message.text.split(" ", 1)[1]
   if txt:
      if re.search("on|yes|enable".lower(), txt.lower()):
         if chat.id in DISABLE_CHATS:
            await message.reply(f"Enabled anti-copyright! for {chat.title}")
            DISABLE_CHATS.remove(chat.id)
            return
         message.reply("Already enabled!")

      elif re.search("no|off|disable".lower(), txt.lower()):
         if chat.id in DISABLE_CHATS:
            await message.reply("Already disabled!")
            return
         DISABLE_CHATS.append(chat.id)
         if chat.id in MEDIA_GROUPS:
            MEDIA_GROUPS.remove(chat.id)
         await message.reply(f"Disable Anti-CopyRight for {chat.title}!")
      else:
         if chat.id in DISABLE_CHATS:
            await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
         else:
            await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")
   else:
       if chat.id in DISABLE_CHATS:
          await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
       else:
          await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")

@RiZoeL.on_message(filters.all)
async def watcher(_, message: Message):
   chat = message.chat
   if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
      
      if chat.id not in ALL_GROUPS:
         ALL_GROUPS.append(chat.id)
      if chat.id in DISABLE_CHATS:
         return
      if chat.id not in MEDIA_GROUPS:
         if chat.id in DISABLE_CHATS:
            return
         MEDIA_GROUPS.append(chat.id)
      if (message.video or message.photo or message.animation or message.document):
         adduser(message.from_user.id)
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
       addchat(i)
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = RiZoeL.send_message(i, random.choice(DELETE_MESSAGE))
          RiZoeL.delete_messages(i, message_list, revoke=True)
          hue.delete()
          RiZoeL.send_message(i, random.choice(DELETE_DONE).format(message_list.count()))
          GROUP_MEDIAS[i].delete()
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias ✓")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler()
scheduler.add_job(AutoDelete, "interval", seconds=3600)

scheduler.start()

def starter():
   print('starting bot...')
   RiZoeL.start()
   print('bot Started ✓')
   idle()

if __name__ == "__main__":
   starter()
