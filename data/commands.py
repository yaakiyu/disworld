# Disworld - Command Data

def story_desc(storyid):
    if storyid == 0:
        return "最初は必ずこのコマンドを使ってください。"
    else:
        return "ストーリーを見ることができます。"


commandsdata = {
    "help": {
        "type": "default",
        "short": "このコマンド",
        "description": "このbotで使えるコマンドについて表示します。\n`help [コマンド名]`と実行することでコマンドの詳細を表示できます。"
    },
    "info":{
        "type": "default",
        "short": "botの情報を表示",
        "description": "ゲームをプレイしてくれてる人などの情報を表示できます。\nゲーム本編とは関係ありません。"
    },
    "story": {
        "type": "story_special",
        "short": story_desc,
        "description": lambda id:"このコマンドではbotのストーリーを見ることができます。このコマンドを使って、ミッションをクリアしていくことで、様々なコマンドが解放されていきます。"
    },
    "talk": {
        "type": "story",
        "require": 1,
        "short": "いろんな人と会話します。",
        "description": "コマンドを実行したあとメニューが出てくるので、メニューで指定した人と会話することができます。"
    },
    "shop":{
        "type": "story",
        "require": 3,
        "short": "お買い物します。",
        "description": "ショップでお買い物できます。\nストーリーを進めると買えるものが増えるかも。"
    }
}