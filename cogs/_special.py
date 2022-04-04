from discord.ext import commands
import utils

class Special(commands.Cog):
    def __init__(self, bot):
        print("loading special...")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.print("called on_ready")
        self.bot.db = utils.EasyDB("disworld.db")
        self.bot.db.create_table("temp",id="int", data="str")
        all = self.bot.db.item.get_all()
        for l in all:
            self.bot.db.temp.add_item(l[0], l[1])
        self.bot.db.delete_table("item")
        self.bot.db.do("ALTER TABLE temp RENAME TO item")
        self.bot.db.commit()
        self.bot.print("done")

async def setup(bot):
    bot.add_cog(Special(bot))