# disworld - first

from discord.ext import commands
import traceback
import os

from core import Bot


class First(commands.Cog):
    def __init__(self, bot: Bot):
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
                except:
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

        # create tables
        await self.bot.execute_sql(
            """CREATE TABLE IF NOT EXISTS Equipment (
                Id BIGINT PRIMARY KEY NOT NULL,
                Weapon INT UNSIGNED, Weapon2 INT UNSIGNED,
                Armor INT UNSIGNED, Accessory INT UNSIGNED
            );"""
        )
        await self.bot.execute_sql(
            """CREATE TABLE IF NOT EXISTS User (
                Id BIGINT UNSIGNED, Name TEXT, Story SMALLINT UNSIGNED,
                Level INT UNSIGNED, Exp BIGINT UNSIGNED,
                Place SMALLINT UNSIGNED, Money INT UNSIGNED
            );"""
        )
        await self.bot.execute_sql(
            "CREATE TABLE IF NOT EXISTS Item(Id BIGINT UNSIGNED, Data JSON);"
        )

        await self.bot.db.async_setup()

        await self.bot.tree.sync()



async def setup(bot: Bot):
    await bot.add_cog(First(bot))
