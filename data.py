version = "0.1"

storydata = {
    "1":{
        "1":{
            "ja":"目覚めたら、見たこともないところに来た。果たしてここはどこなのか。\n見回してみると、老人がいた。話すといいかもしれない。\n```diff\nミッション\n+ 「g.talk」で老人と話そう。\n```",
            "en":"""I woke up, and found myself in this strange place I never seen before.\nWhere this is, is unclear. However, there's a old man nearby. It might be good to go talk to him.\nEnter g.talk to start a conversation.
"""
        },
        "2":{
            "ja":"老人に棒を買えと言われた。何故かはわからないが、信じてやったほうがいい予感がする。\n買い物をしよう。\n```diff\nミッション\n+ g.shopで買い物をしよう。\n```",
            "en":"""The old man told me to go buy a stick. I'm not sure if he's sane, but I have a feeling this might be important.\nStart shopping with g.shop."""
        },
        "3":{
            "ja":"""(story)
```diff
ミッション
+ (mission)
```""",
            "en":"""
"""
        },
        "4":{
            "ja":"""(story)
```diff
ミッション
+ (mission)
```""",
            "en":"""
"""
        }
    }
}



talkdata = {
    "1":{
        "ja":"""こんにちは。こんな時に初めて見る人なんか珍しいね。\n名前?僕はただのなんてこともない老人だよ。\n君の名前は?{ctx.author.name}さんか。よろしく。\nところでここはどこか分かる?え?わからないって?\n君は実に面白いなー。ここはセーフイ村だよ。\n地上は危ないわけだから、みんなここで暮らしてるわけだよ。\nえっ?出たい?(なんでここを出たい人はみんな僕に言うんだろう...)\n本当に出たいなら一つすることがある。\nあそこの店に行って、を買ってきて。それができれば出してあげるよ。\n```diff\n! ミッションクリア !\n```""",
        "en":"""Hi there! Say, you're new here aren't you? That's very rare in these times.
Who am I? Don't worry, that isn't important. I'm just an old man who lives here.
By the way, who are you? Oh, you're {ctx.author.name}? nice to meet you!
Welcome to Safiy Village, the safest village/bunker/tourist attraction around here! 
Although, you certainly don't seem like the person who would like to stay put...
Okay, tell you what. If you can help me, 
I'll help you get out of here. Agreed? Nice!
Now firstly, I'm going to have to ask you to get a stick. Not going to explain, just go get it. You'll understand why."""
    }
}