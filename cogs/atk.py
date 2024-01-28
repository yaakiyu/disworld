import discord
from discord.ext import commands


class Attack(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.hybrid_command(aliases=["atk"])
    async def attack(self, ctx):
        await ctx.reply("開発中...")


async def setup(bot):
    await bot.add_cog(Attack(bot))