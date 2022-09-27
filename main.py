# Disworld program - main

import discord
import os
import core
from dotenv import load_dotenv


load_dotenv()

# mode(0=normal, 1=test, 2=special)
mode = int(os.environ.get("MODE", 0))

# bot object
bot = core.Bot(**{
    "command_prefix": "g2." if mode else "g.",
    "help_command": None,
    "activity": discord.Game("help: g.help"),
    "mode": mode
})

# run
bot.print(f"running mode {mode}...", mode="main")

if mode == 0:
    bot.run(os.environ["TOKEN"])
elif mode in [1, 2]:
    bot.run(os.environ["TOKEN2"])
