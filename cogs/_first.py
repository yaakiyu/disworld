from nextcord.ext import commands, tasks
import traceback
import os

class First(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        count = 0
        self.bot.db.create_table("equipment", id="int", buki="int", buki2="int", bougu="int", akusesari="int")
        allcogs = os.listdir("cogs/")
        for s in allcogs:
            if not s.startswith("_"):
                try:
                    self.bot.load_extension(f"cogs.{s[:-3] if s.endswith('.py') else s}")
                    self.bot.print(f"loaded cogs.{s[:-3] if s.endswith('.py') else s}")
                except:
                    count += 1
                    traceback.print_exc()
        self.bot.print(f"all {len(allcogs)} cogs {'successfully ' if not count else ''}loaded{f' and {count} cogs gave an error' if count else ''}.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.print("on_ready")
        self.save.start()
        self.bot.print("started saving loop.")

    @tasks.loop(seconds=60)
    async def save(self):
        self.bot.db.commit()
        if self.bot.command_prefix == "g2.":
            self.bot.print("saved data.")


def setup(bot):
    bot.add_cog(First(bot))