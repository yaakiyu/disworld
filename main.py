# Disworld program - main

import discord
import os
import utils
import keep_alive
import data
import core


# mode(0=normal, 1=test, 2=special)
mode = 0

# bot object
bot = core.Bot(**{
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
})
bot.db = utils.EasyDB("disworld.db")

#data set
bot.storydata = data.storydata
bot.talkdata = data.talkdata
bot.commandsdata = data.commandsdata
bot.fielddata = data.fielddata
bot.itemdata = data.itemdata

del data


# run
keep_alive.keep_alive()
bot.print(f"running mode {mode}...", mode="special")

if mode == 0:
    bot.run(os.getenv("TOKEN"))
elif mode in [1, 2]:
    bot.run(os.getenv("TOKEN2"))