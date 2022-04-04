from discord.ext import commands, tasks
import traceback
import os

class First(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener("on_full_ready")
    async def ready(self):
        self.bot.print("on_full_ready.", mode="first")
        count = 0
        allcogs = os.listdir("cogs/")

        # load cogs
        for s in allcogs:
            if not s.startswith("_"):
                try:
                    await self.bot.load_extension(
                        f"cogs.{s[:-3] if s.endswith('.py') else s}"
                    )
                    self.bot.print(
                        f"loaded cogs.{s[:-3] if s.endswith('.py') else s}",
                        mode="first"
                    )
                except BaseException:
                    count += 1
                    traceback.print_exc()
        self.bot.print(
            f"all {len(allcogs)} cogs \
            {'successfully ' if not count else ''}loaded\
            {f' and {count} cogs gave an error' if count else ''}.",
            mode="first"
        )

        # saving loop
        self.save.start()
        self.bot.print("started saving loop.", mode="first")

    @tasks.loop(seconds=60)
    async def save(self):
        self.bot.db.commit()
        if self.bot.command_prefix == "g2.":
            self.bot.print("saved data.")


async def setup(bot):
    await bot.add_cog(First(bot))