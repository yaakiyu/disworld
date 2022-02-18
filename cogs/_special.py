from nextcord.ext import commands
import utils

class Special(commands.Cog):
    def __init__(self, bot):
        print("loading special...")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("called on_ready")
        self.bot.db = utils.EasyDB("disworld.db")
        self.bot.db.create_table("user", id="int", name="str", story="int", level="int", exp="int", place="int", money="int")
        for old in self.bot.db.users.get_all():
            self.bot.db.user.add_item(old[0], old[1], old[2], old[3], old[4], old[5], 0)
        self.bot.db.delete_table("users")
        self.bot.db.create_table("users", id="int", name="str", story="int", level="int", exp="int", place="int", money="int")
        for old in self.bot.db.user.get_all():
            self.bot.db.users.add_item(old[0], old[1], old[2], old[3], old[4], old[5], 0)
        self.bot.db.delete_table("user")
        self.bot.db.commit()
        print("all success")

def setup(bot):
    bot.add_cog(Special(bot))