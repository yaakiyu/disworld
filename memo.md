# memo  
ちょっとメモ。  
  
## story進行ナンバーについて  
0 - ストーリー開始前  
1 - Ep1を見た後  
2 - talk後  
3 - Ep2を見た後  
4 - shopに行った後  
5 - Ep3を見た後  
6 - equipコマンドで装備した後  
7 - 敵と一回戦った後  
8 - 敵と5回戦った後  
  
## talkの内部処理番号について  
1 - 老人  
  
## commands_dataについて  
help用データ。コマンドにはそれぞれtypeが存在する。　  
さらに、short(短い説明)とdescription(詳細helpで出す長い説明)キーは必ず必要。  
(以下、typeに関する説明)
- default デフォルトで表示するコマンド。
- story ストーリー進行に合わせて表示されるコマンド。require(値はストーリーナンバー)キーが必要。
- story_special ストーリー進行によって表示内容が変わるコマンド。shortやdescriptionにストーリー進行度を引数にとる関数を渡す。

## DBの仕様について
User: Id=BIGINT UNSIGNED, Name=TEXT(~65535桁), Story=SMALLINT UNSIGNED(0~255)  
    : Level=INT UNSIGNED(0~4294967295), Exp=BIGINT UNSIGNED,  
    : Place=SMALLINT UNSIGNED, Money=INT UNSIGNED  
Item: Id=BIGINT UNSIGNED, Data=JSON  
Equipment: Id=BIGINT UNSIGNED, Weapon=INT UNSIGNED, Weapon2=INT UNSIGNED,  
         : Armor=INT UNSIGNED, Accessory=INT UNSIGNED