# MADE BY AMAN PANDEY FOR Extre USERBOT DONT KANG. OTHERWISE GET READY FOR COPYRIGHT STRIKE
from Extre import bot
from sys import argv
import sys
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from telethon import TelegramClient
from Extre import *
from Extre.variables import Var
from Extre.utils import load_module
from Extre.utils import start_assistant
from Extre import LOAD_PLUG, BOTLOG_CHATID, LOGS
from Extre import extremepro_bot
from pathlib import Path
import asyncio
import telethon.utils



                   
async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me() 
    bot.uid = telethon.utils.get_peer_id(bot.me)



if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        print("Connecting To Scratch Server")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        bot.loop.run_until_complete(add_bot(Var.TG_BOT_USER_NAME_BF_HER))
        print("Connected To Scratch Server")
    else:
        bot.start()

iampro = os.environ.get("BOT_TOKEN", None)        

if len(argv) not in (1, 3, 4):
    client.disconnect()
else:
    client.tgbot = None
    if iampro is not None:
        print("Connecting To Client 2")
        # ForTheGreatrerGood of beautification
        client.tgbot = TelegramClient(
            "ANDENCENTO",
            api_id=CLIENT_API,
            api_hash=CLIENT_API_HASH
        ).start(bot_token=iampro)
        client.loop.run_until_complete(add_bot(iampro))
        print("Connected To Client 2")
    else:
        print ("Failed to connect client 2")


import glob
path = 'assistant/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        start_assistant(shortname.replace(".py", ""))
# ForTheGreatrerGood
      
import glob

path = 'plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))



print("ExtremeProUserbot Deployed And Working Fine For Assistance Join @EXTREMEPRO_USERBOT")



if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
    extremepro_bot.run_until_disconnected()