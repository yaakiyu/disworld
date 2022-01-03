import discord
import os
from discord.ext import commands
import logging
import utils
import dislash
import keep_alive
import data
# mode(0=normal,1=test)
mode = 0
# logging
logging.basicConfig(level=logging.INFO)

# bot settings
s = {
    "command_prefix": "g2." if mode else "g.",
    "owner_ids": [
        693025129806037003, #yaakiyu
        696950076207005717, #DrEleven
        705399971062612011, #hard Smoothyさん
        575221859642114059, #mksuke123さん
        667319675176091659, #takkunさん
        573836903091273729 #きのたこさん
    ],
    "allowed_mentions": discord.AllowedMentions(users=False, roles=False),
    "help_command": None
}
# bot object
bot = commands.Bot(**s)
bot.load_extension("jishaku")
bot.db = utils.EasyDB("disworld.db")

#data set
bot.version = data.version
bot.storydata = data.storydata
bot.talkdata = data.talkdata

slash = dislash.SlashClient(bot)
def prrint(*args, **kwargs):
    print("[SystemLog]", *args, **kwargs)
bot.print = prrint
del prrint, data

# loading first cog
bot.load_extension("cogs._first")

# run
keep_alive.keep_alive()
if mode == 0: bot.run(os.getenv("TOKEN"))
elif mode == 1: bot.run(os.getenv("TOKEN2"))
