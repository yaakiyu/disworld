from discord.ext import commands
import discord
from dislash import slash_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(description="攻撃！")
    async def attack(self, inter):
        await inter.reply("attacked!?!?", ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))