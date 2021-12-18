from discord.ext import commands, tasks
import traceback
import os
import discord

class First(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.version = "0.1"
        self.bot.db.create_table("users", id="integer", name="str", story="integer", level="integer", exp="integer", ch="none")

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.print("on_ready")
        for s in os.listdir("cogs/"):
            if s.endswith(".py") and not s.startswith("_"):
                try:
                    self.bot.load_extension(f"cogs.{s[:-3]}")
                    self.bot.print(f"loaded cogs.{s[:-3]}")
                except:
                    traceback.print_exc()
        self.bot.print("all cogs loaded.")
        self.save.start()
        self.bot.print("started save loop.")

    @tasks.loop(seconds=60)
    async def save(self):
        self.bot.db.commit()
        if self.bot.command_prefix == "g2.":
            self.bot.print("saved the data.")


def setup(bot):
    bot.add_cog(First(bot))