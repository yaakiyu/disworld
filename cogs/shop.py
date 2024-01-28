# disworld - shop

from discord.ext import commands
import discord
import orjson

from core import Bot
import utils


class Shop(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="shop")
    async def c_shop(self, ctx: commands.Context):
        await self.bot.lock_checker(ctx, 3, 0.2)

        udata = self.bot.db.user[ctx.author.id]["Story"]
        if udata == 3:
            # チュートリアル
            return await self.tutorial(ctx)

        udata = self.bot.db.user[ctx.author.id]
        uitem = orjson.loads(self.bot.db.item[ctx.author.id]["Data"])
        places = [p for p in self.bot.fielddata if p["visit"] < udata[2]]
        shops = [x for s in places for x in s["shops"]]
        shop_names = [i["name"] for i in shops]
        view = utils.EasyView(utils.EasyMenu(
            "お店を選択", 
            "行きたいお店を選択してください。",
            **{shops[i]["name"]: shops[i]["description"] for i in range(len(shop_names))}
        ))
        msg = await ctx.send(
            embed=discord.Embed(
                title="ショップ",
                description="行きたいお店に行くことができます。"
            ),
            view=view
        )
        def inter_check(inter: discord.Interaction):
            return (inter.user == ctx.author
                and inter.type == discord.InteractionType.component
                and inter.channel_id == ctx.channel.id
                and inter.message is not None and inter.message.id == msg.id
            )
        inter: discord.Interaction = await self.bot.wait_for(
            "interaction", check=inter_check
        )
        select: discord.ui.Select = view.children[0]  # type: ignore
        selected_shop = shops[shop_names.index(select.values[0])]
        selling_items = [self.bot.itemdata[l] for l in selected_shop["items"]]
        embed = discord.Embed(title=selected_shop["name"], description="買いたいアイテムを選択してください。")
        for ite in selling_items:
            if ite["type"] == "weapon":
                embed.add_field(
                    name=ite["name"],
                    value=f"種類：武器 攻撃力：{ite['attack']} 価格：{ite['shop']}")
            elif ite["type"] == "armour":
                embed.add_field(
                    name=ite["name"],
                    value=f"種類：防具 防御力：{ite['block']} 価格：{ite['shop']}")
            elif ite["type"] == "useful":
                embed.add_field(
                    name=ite["name"],
                    value=f"種類：便利アイテム 効果：{ite['effect']} 価格：{ite['shop']}")
        menu = {m["name"]:f"価格: {m['shop']}" for m in selling_items}
        view = utils.EasyView(utils.EasyMenu("アイテムを選択", "自分が十分なお金を持っている場合のみ買えます。", **menu))
        await inter.response.edit_message(embed=embed, view=view)

        inter = await self.bot.wait_for("interaction", check=inter_check)

        select: discord.ui.Select = view.children[0]  # type: ignore
        itemid = selected_shop["items"][list(menu.keys()).index(select.values[0])]
        selected_item = self.bot.itemdata[itemid]
        if udata[6] < selected_item["shop"]:
            return await inter.response.edit_message(
                embed=utils.ErrorEmbed(
                    "エラー", f"お金が足りません。\n必要金額: `{selected_item['shop']}`\n現在所持: `{udata[6]}`"
                ),
                view=None
            )
        if not str(itemid) in uitem:
            uitem[str(itemid)] = 1
        else:
            uitem[str(itemid)] += 1
        # itemテーブルへ書き込み
        self.bot.db.item[ctx.author.id]["Data"] = orjson.dumps(uitem)
        udata[6] -= selected_item["shop"]
        # moneyを減らしてusersテーブルへ書き込み
        self.bot.db.user[ctx.author.id]["Money"] = udata[6]
        await inter.response.edit_message(
            embed=discord.Embed(
                title="成功",
                description=f"{selected_item['name']}を購入しました。"
            ),
            view=None
        )

    async def tutorial(self, ctx: commands.Context):
        e = discord.Embed(
            title="ショップ - チュートリアル",
            description="お店へようこそ！案内人のマスダです！\nこの街には1個のお店が存在するようですね...\nセーフィ生活店というところに行ってみましょう！"
        )

        async def callback_1(inter: discord.Interaction):
            if inter.user != ctx.author:
                return await inter.response.send_message(
                    "あなたはこの操作をすることができません！", ephemeral=True
                )
            e = discord.Embed(
                title="セーフイ生活店 - チュートリアル",
                description="この店に来るのが初めてなので、まずはただの棒を買ってみましょう！今回だけ特別にタダで渡します！"
            )

            async def callback_2(inter: discord.Interaction):
                if inter.user != ctx.author:
                    return await inter.response.send_message(
                        "あなたはこの操作をすることができません！", ephemeral=True
                    )
                if ctx.author.id not in self.bot.db.item:
                    data = orjson.dumps({"0":1}).decode()
                    self.bot.db.item.insert((ctx.author.id, data))
                e = discord.Embed(
                    title="セーフイ生活店 - チュートリアル",
                    description="しっかり商品を購入できましたね！おめでとう！\n```diff\n! ミッションクリア !\n+ 「g.equip」で購入した武器を装備しよう。\n```"
                )
                await inter.response.edit_message(embed=e, view=None)
                self.bot.db.user[ctx.author.id]["Story"] = 4

            menu = utils.EasyMenu("アイテムを選択", "アイテムを選択してください", callback=callback_2, **{"ただの棒":"2"})
            await inter.response.edit_message(view=None)
            await ctx.send(embed=e, view=utils.EasyView(menu))

        menu = utils.EasyMenu("お店を選択", "お店を選択してください", callback=callback_1, **{"セーフイ生活店":"1"})
        await ctx.send(embed=e, view=utils.EasyView(menu))


async def setup(bot: Bot):
    await bot.add_cog(Shop(bot))