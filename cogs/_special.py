from discord.ext import commands


class Special(commands.Cog):
    def __init__(self, bot):
        bot.print("loading special cog...")
        self.bot = bot

    async def cog_load(self):
        self.bot.print("called on_ready")


async def setup(bot):
    bot.add_cog(Special(bot))