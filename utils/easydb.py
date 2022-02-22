import sqlite3
from typing import List, Optional

class EasyDB():
    """簡単にデータベース(sqlite3)を扱えるクラス。"""
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("select name from SQLITE_MASTER where type='table' ORDER BY name")
        for f in self.cur.fetchall():
            setattr(self, f[0], Table(f[0], self.conn, self.cur))

    def create_table(self, table_name: str, **values) -> None:
        """「EasyDB.(テーブル名)」(Tableオブジェクト)が作成される。
        table_name:テーブル名
        **values:(キーワード引数)中身 {value:type}"""
        m = [f"{k} {v}" for k, v in values.items()]
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({', '.join(m)})")
        if not getattr(self, table_name, False):
            setattr(self, table_name, Table(table_name, self.conn, self.cur))

    def delete_table(self, table_name: str) -> None:
        """テーブルの削除を行う。"""
        if not hasattr(self, table_name):
            raise TableNotFound("テーブルが見つかりませんでした。")
        self.cur.execute(f"DROP TABLE {table_name}")
        delattr(self, table_name)

    def get_table(self, name: str):
        """テーブルを検索し、Tableオブジェクトを返す。"""
        if not hasattr(self, name):
            raise TableNotFound("テーブルが見つかりませんでした。")
        return getattr(self, name)

    def get_all_tables(self) -> list:
        """EasyDB.(テーブル名)は作成されず、List[Table]が返る。"""
        self.cur.execute("select name from SQLITE_MASTER where type='table' ORDER BY name")
        return [Table(f[0], self.conn, self.cur) for f in self.cur.fetchall()]

    def get_all_tables_name(self) -> List[str]:
        """テーブル名だけのリストが返る。"""
        self.cur.execute("select name from SQLITE_MASTER where type='table' ORDER BY name")
        return [f[0] for f in self.cur.fetchall()]

    def do(self, *commands, commit: Optional[bool]=True) -> Optional[List[str]]:
        """sql構文をそのまま実行する。"""
        returns = ""
        for c in commands:
            self.cur.execute(c)
            if c.startswith("SELECT"):
                returns += f"\n{self.cur.fetchall()}"
        return returns

    def commit(self) -> None:
        """データを実際に保存する。
        Table.add_itemなどでcommit=Trueを指定するのと同じ動き。"""
        self.conn.commit()


class TableNotFound(Exception):
    pass


class UnknownType(Exception):
    pass


class Table():
    def __init__(self, name:str, conn, cur):
        self.conn = conn
        self.cur = cur
        self.name = name
        if not name in EasyDB.get_all_tables_name(self):
            raise TableNotFound("テーブルが見つかりませんでした。")
        self.cur.execute("select sql from SQLITE_MASTER where type='table' and name=?", (self.name,))
        sql = self.cur.fetchall()[0][0]
        sql = sql.split(f"{self.name}(")[1].replace(")", "")
        self.values = {a.split()[0]:a.split()[1] for a in sql.split(", ")}

    def __getitem__(self, item):
        if "id" not in list(self.values.keys()):
            raise ValueError("テーブルにidカラムが存在しません。")
        return self.search(id=item)

    def _execute_data_create(*values) -> str:
        """(管理用)渡された引数がstr型だったら「'」をつけて返す。"""
        return_data = []
        for m in values:
            if isinstance(m, str):
                return_data.append(f"'{m}'")
            elif isinstance(m, int):
                return_data.append(str(m))
        return ", ".join(return_data)

    def add_item(self, *values, commit=False) -> None:
        """アイテムの追加。
        values:create時に指定した順番に従って値を入力。
        commit:(キーワード専用)コミットするかどうか。"""
        if len(values) != len(self.values.keys()):
            raise KeyError(f"引数の数がテーブルの中身と一致していません。\nテーブルの中身：{self.values}")
        execute_data = self._execute_data_create(*values)
        # print(execute_data)
        self.cur.execute(f"INSERT INTO {self.name} values({execute_data})")
        if commit:
            self.conn.commit()

    def remove_item(self, *where, mode="and", commit=False) -> None:
        """アイテムの削除。
        where:strで一つ一つの式を書く。('id>10 and id<100'のようにするとmodeがorでもandできる。)
        mode:(キーワード専用・defaultはand)orかandを使ってそれぞれの式をどう繋げるかを書く。
        commit:(キーワード専用)コミットするかどうか。
        """
        if not mode in ["and", "or"]:
            raise TypeError("modeはandかorのみです。")
        if len(where) == 0:
            value = ""
        else:
            value = " WHERE " + f" {mode} ".join(where)
        self.cur.execute(f"DELETE FROM {self.name}{value}")
        if commit:
            self.conn.commit()
    
    def search(self, get=None, sort=None, mode="and", **where) -> tuple:
        """情報の検索。
        get: どの値をゲットするか。
        sort: どの値の順番に並べるか。
        mode: 条件式が2つ以上のとき、andかorか。
        **where: (キーワード引数)サーチする条件。
        """
        values = self.values.keys()
        if not mode in ["and", "or"]:
            raise TypeError("modeはandかorのみです。")
        if not all((f in values) for f in where.keys()):
            raise KeyError("引数の中におかしいものが含まれています")
        if len(where.keys()) == 0:
            whered = ""
        else:
            whered = " WHERE " + f" {mode} ".join([f"{k}={self._execute_data_create(v)}" for k,v in where.items()])
        if get is None:
            get = "*"
        elif get not in values:
            raise KeyError("引数の中におかしいものが含まれています")
        if sort is None:
            sort = ""
        elif not sort in values:
            raise KeyError("sortに指定されたカラムが存在しません。")
        else:
            sort = f" ORDER BY {sort}"
        self.cur.execute(f"SELECT {get} FROM {self.name}{whered}{sort}")
        return self.cur.fetchall()

    def get_all(self) -> tuple:
        """全データをゲットする。引数を指定しないsearchのエイリアス。"""
        return self.search()

    def is_in(self, **kwargs) -> int:
        """データがテーブル内に存在するかどうかを調べる。
        存在する個数を返す。
        **kwargs: データに関する情報。"""
        if not all(m in self.values.keys() for m in kwargs.keys()):
            raise ValueError("存在しないキーがあります。")
        return len(self.search(**kwargs))

    def update_item(self, *where, mode="and", commit=False, **after) -> None:
        """データの変更を行う。
        *where:どこかについての情報(strで条件文を書くこと)
        mode:whereの検索で幾つか条件があった場合andを使うかorを使うか。
        commit:conn.commit()するかどうか。
        **after:キーワード引数でどこをどう変更するかを書く。"""
        values = self.values.keys()
        if not mode in ["and", "or"]:
            raise TypeError("modeはandかorのみです。")
        if not all((f in values) for f in after.keys()):
            raise KeyError("引数の中におかしいものが含まれています")
        if len(after) == 0:
            raise TypeError("変更するものを選択してください")
        if len(where) == 0:
            value = ""
        else:
            value = " WHERE " + f" {mode} ".join(where)
        after = ", ".join(
            [f"{k}={self._execute_data_create(v)}" for k,v in after.items()]
        )
        self.cur.execute(f"UPDATE {self.name} SET {after}{value}")
        if commit:
            self.conn.commit()

    def add_column(
        self, name:str, typ:str, default=None, *, 
        first: bool=False, after:Optional[str]=None, commit:bool=False
    ):
        """テーブルにカラムを追加します。
        name: 新カラムの名前
        typ: 新カラムのタイプ指定
        default=None: デフォルト値。これを指定しないと適当なものが選出される。
        *
        first(キーワード引数): カラムを先頭に持ってくるかどうか。afterとは併用不可。
        after(キーワード引数): どのカラムの直後に持ってくるか(str)。firstとは併用不可。
        """
        assert (first == False) or (after is None), "firstとafterの両方があってはいけません。"
        after = "" if after is None else " AFTER "+after
        first = " FIRST" if first else ""
        self.cur.execute(f"ALTER TABLE {self.name} ADD {name} {typ}{first}{after}")
        if default is not None:
            return self.update_item(commit=commit, **{name:default})
        if typ in ["str", "string", "text"]:
            return self.update_item(commit=commit, **{name:""})
        elif typ in ["int", "integer"]:
            return self.update_item(commit=commit, **{name:0})
        else:
            if commit:
                self.conn.commit()
            raise UnknownType("コラム追加には成功したがデフォルトの自動選出に失敗しました。")

    def rename_column(self, before, after, *, commit=False):
        """(未完成)カラムの名前を変更します。tempというテーブルがないことが条件です。"""
        pass