from discord.ext import commands, tasks
import discord
import traceback

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = []

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        await ctx.send("error!\n```py\n" + traceback.format_exception(type(e), e, e.__traceback__)+ "\n```")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.command_log.start()
    
    @tasks.loop(seconds=60)
    async def command_log(self):
        if len(self.log) == 0:return



def setup(bot):
    bot.add_cog(Error(bot))