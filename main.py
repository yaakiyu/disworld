print("disworld loading...")
import discord
import os
from discord.ext import commands
import utils
import dislash
import keep_alive
import data
# mode(0=normal, 1=test, 2=DB_special)
mode = 0

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
    "help_command": None,
    "activity":discord.Game("help: g.help")
}
# bot object
bot = commands.Bot(**s)
bot.db = utils.EasyDB("disworld.db")

#data set
bot.version = data.version
bot.storydata = data.storydata
bot.talkdata = data.talkdata
bot.commandsdata = data.commandsdata
bot.fielddata = data.fielddata
bot.itemdata = data.itemdata

slash = dislash.SlashClient(bot)
def prrint(*args, **kwargs):
    args = [a for a in args] + ["\033[0m"]
    kwargs["sep"] = ""
    if kwargs.get("mode"):
        args = [f"\033[0m[\033[92m{kwargs.get('mode')}\033[0m]\033[93m"] + args
        del kwargs["mode"]
    print("[SystemLog]\033[93m", *args, **kwargs)
bot.print = prrint
del prrint, data

# loading first cog
if mode != 2:
    bot.load_extension("cogs._first")
else:
    bot.load_extension("cogs._special")

# run
keep_alive.keep_alive()
bot.print("running...", mode="special")
if mode == 0: bot.run(os.getenv("TOKEN"))
elif mode in [1, 2]: bot.run(os.getenv("TOKEN2"))