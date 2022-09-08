# Disworld program - main

import discord
import os
import keep_alive
import core


# mode(0=normal, 1=test, 2=special)
mode = 0

# bot object
bot = core.Bot(**{
    "command_prefix": "g2." if mode else "g.",
    "help_command": None,
    "activity":discord.Game("help: g.help")
})


# run
keep_alive.keep_alive()
bot.print(f"running mode {mode}...", mode="main")

if mode == 0:
    bot.run(os.environ["TOKEN"])
elif mode in [1, 2]:
    bot.run(os.environ["TOKEN2"])