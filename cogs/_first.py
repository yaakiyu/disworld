from discord.ext import commands, tasks
import traceback
import os


class First(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.print("the first cog was loaded.", mode="first")
        count = 0
        allcogs = os.listdir("cogs/")

        # load cogs
        for s in allcogs:
            if not s.startswith("_"):
                try:
                    file_name = s[:-3] if s.endswith('.py') else s
                    await self.bot.load_extension(f"cogs.{file_name}")
                    self.bot.print(
                        f"loaded cogs.{file_name}", mode="first"
                    )
                except Exception:
                    count += 1
                    traceback.print_exc()

        # load additional cogs
        await self.bot.load_extension("jishaku")

        self.bot.print(
            f"all {len(allcogs)} cogs "
            f"{'successfully ' if not count else ''}loaded"
            f"{f' and {count} cog(s) gave an error' if count else ''}.",
            mode="first"
        )

        # saving loop
        self.save.start()
        self.bot.print("started saving loop.", mode="first")

    @tasks.loop(seconds=60)
    async def save(self):
        self.bot.db.commit()


async def setup(bot):
    await bot.add_cog(First(bot))