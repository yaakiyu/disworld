# disworld - data cache

from typing import TYPE_CHECKING

from copy import deepcopy

from discord.ext import tasks
import aiomysql

if TYPE_CHECKING:
    from .bot import Bot


class Columnlized(list):
    "各データ用クラス。getitemの実装をするためだけ。"
    columns: tuple

    def __getitem__(self, item):
        if isinstance(item, str):
            if item not in self.columns:
                raise KeyError("不明なカラム。")
            return super().__getitem__(self.columns.index(item))
        elif isinstance(item, int):
            return super().__getitem__(item)
        raise KeyError("そんなデータないで。")
    
    def __setitem__(self, item, item2):
        if isinstance(item, str):
            if item not in self.columns:
                raise KeyError("不明なカラム。")
            super().__setitem__(self.columns.index(item), item2)
        elif isinstance(item, int):
            return super().__setitem__(item, item2)
        raise KeyError("そんなデータないで。")


class DataBaseCache:
    "個々のキャッシュ本体。getitemによるアクセスを可能とする。"
    first_data: list[Columnlized]
    data: list[Columnlized]
    bot: "Bot"
    table_name: str
    columns: tuple
    deleted: list[int]

    def __init__(self, table_name: str, bot: "Bot"):
        self.table_name = table_name
        self.deleted = []
        self.bot = bot

    async def async_setup(self) -> None:
        "非同期セットアップ。"
        columns = await self.bot.execute_sql(
            f"SHOW COLUMNS FROM {self.table_name}", _return_type="fetchall"
        )
        if not columns:
            raise ValueError("テーブルが存在しない...?")
        self.columns = tuple(x[0] for x in columns)

        data = await self.bot.execute_sql(
            f"SELECT * FROM {self.table_name}", _return_type="fetchall"
        )
        self.data = []
        for i in data:  # type: ignore
            cldata = Columnlized(i)
            cldata.columns = self.columns
            self.data.append(cldata)

        self.first_data = deepcopy(self.data)

    def insert(self, data: tuple):
        "insertのキャッシュ側の動作をする。データ追加は基本これで。"
        cldata = Columnlized(data)
        cldata.columns = self.columns
        self.data.append(cldata)

    def delete(self, item: int):
        "deleteのキャッシュ側の動作をする。"
        if item < 1000000:
            # deletedにitemのIdを追加して削除。
            self.deleted.append(self.data[item][0])
            del self.data[item]
        if item not in (ids := [i[0] for i in self.data]):
            raise KeyError("そんなデータない。")
        self.deleted.append(item)
        del self.data[ids.index(item)]

    def __getitem__(self, item: int):
        # itemがIDっぽかったらID検索をする。
        if item < 1000000:
            return self.data[item]
        if item not in (ids := [i[0] for i in self.data]):
            raise KeyError("そんなデータない。")
        return self.data[ids.index(item)]

    def __contains__(self, item: int):
        return item in [i[0] for i in self.data]

    def get_by_id(self, item: int):
        return self[item]


class DataController:
    "Botの全データをキャッシュとしてコントロールするクラス。"

    user: DataBaseCache
    item: DataBaseCache
    equipment: DataBaseCache

    def __init__(self, bot: "Bot"):
        "キャッシュの初期化。"
        self.bot = bot
        self.user = DataBaseCache("User", bot)
        self.item = DataBaseCache("Item", bot)
        self.equipment = DataBaseCache("Equipment", bot)

    async def async_setup(self):
        "非同期セットアップ。 mysql接続済みの前提で動作します。"
        await self.user.async_setup()
        await self.item.async_setup()
        await self.equipment.async_setup()

        self.saveloop.start()

    @tasks.loop(minutes=1)
    async def saveloop(self):
        "データのセーブをします。"
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for db in (self.user, self.item, self.equipment):
                    await self.deleted_data_check(db, cursor)
                    for row in db.data:
                        await self.data_check(db, row, cursor)

    async def deleted_data_check(
        self, db: DataBaseCache, cursor: aiomysql.Cursor
    ) -> None:
        "削除済みのデータに関して一気に処理します。"
        await cursor.executemany(
            f"DELETE FROM {db.table_name} WHERE Id = %s", db.deleted
        )
        db.deleted = []

    async def data_check(
        self, db: DataBaseCache, row: Columnlized,
        cursor: aiomysql.Cursor
    ):
        "データの変更を調べてあればinsert・updateします。"
        if row in db.first_data:
            return
        if row[0] not in (ids := [r[0] for r in db.first_data]):
            # insertする。
            await cursor.execute(
                f"INSERT INTO {db.table_name} VALUES ("
                + ", ".join("%s" for _ in range(len(row.columns))) + ");",
                row
            )
        if db[ids.index(row[0])] != row:
            # updateする。
            await cursor.execute(
                f"UPDATE {db.table_name} SET "
                + ", ".join(f"{i} = %s" for i in row.columns)
                + "WHERE Id = %s,",
                row + [row[0],]
            )
        db.first_data = deepcopy(db.data)
