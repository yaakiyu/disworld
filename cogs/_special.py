from discord.ext import commands

from core import Bot


class Special(commands.Cog):
    def __init__(self, bot: Bot):
        bot.print("loading special cog...")
        self.bot = bot

    async def cog_load(self):
        self.bot.print("called on_ready")


async def setup(bot: Bot):
    await bot.add_cog(Special(bot))
