from discord.ext import commands
import discord
from os import getenv
import traceback
import random
import datetime
from riotwatcher import LolWatcher

intents = discord.Intents.default()
intents.members = True  # これをしないとget_memberとかできなくなる
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)  # command_prefixはコマンドの前につけるやつ　スラッシュコマンドはdiscordのもともとついている機能と被るため$にした

# BOT関連の発言をするテキストチャンネルおよびチーム振り分け待機VC、赤チーム青チームVCのチャンネルID
BOT_COMMAND_CHANNEL_ID = 892796029362139170  # こっちはテストサーバー用
taikibeya_ID = 892796029362139172
red_team_ID = 948050118031077376
blue_team_ID = 948050118572138536
"""
BOT_COMMAND_CHANNEL_ID = 951092799623790622 # 本サーバー用
taikibeya_ID = 707947337770860574
red_team_ID = 270573338752057355
blue_team_ID = 269884896258818049
"""
key = getenv('riotkey')


@bot.event
async def on_command_error(ctx, error):  # エラーはいたときに教えてくれるやつ
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_ready():  # BOT起動時に日本時間でいつ起動したかをステータスに設定する
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    jst = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    await bot.change_presence(activity=discord.Game(name=f'起動日時{jst}'))
    # chan = bot.get_channel(BOT_COMMAND_CHANNEL_ID)
    # 再起動すると指定チャンネルに再起動したことを通知するがうるさいので一回消しとく await chan.send("準備完了! $help でコマンドを確認できるよ")


@bot.command()
async def ping(ctx):  # BOTがちゃんと稼働してるかどうか確認するためのこまんど
    await ctx.send('HELLO!')


@bot.command()
async def help(ctx):  # helpコマンド
    await ctx.send('$ping\n    BOTが稼働してたらHELLOと返事を返すよ\n$custom\n    カスタム待機部屋にいる人を自動的にRED,BLUEにわけるよ\n    コマンドを打つ人がVCにいてVCの人数が10人じゃないといけないよ')


@bot.command()
async def test(ctx, num1: int = 5, num2: int = 5):
    await ctx.send(f'{num1}と{num2}')


@bot.command()
async def blue(ctx):  # 発言者をblueチームに送るコマンド
    blue_team = bot.get_channel(blue_team_ID)
    voice = ctx.author.voice
    if voice is None:
        await ctx.send("VCに接続していませんね")
        return
    guild = ctx.guild
    blue = []
    blue.append(ctx.author.id)
    blmem = await guild.fetch_member(blue[0])
    await blmem.move_to(blue_team)


@bot.command()
async def custom(ctx, num1: int = 5, num2: int = 5):  # カスタムチーム分けbot 青チーム赤チーム5人ずつランダムに分ける
    # チーム振り分け待機部屋、赤青チームのチャンネル、コマンドが実行されたguild(=サーバー)を取得
    red_team = bot.get_channel(red_team_ID)
    blue_team = bot.get_channel(blue_team_ID)
    taikibeya = bot.get_channel(taikibeya_ID)
    guild = ctx.guild

    #  user_name = [member.name for member in taikibeya.members]  # 待機部屋に接続しているメンバーの名前を取得　IDだけでいいかも
    user_ID = [member.id for member in taikibeya.members]         # 同IDを取得
    await ctx.send("VCに" + str(len(user_ID)) + "人接続しています")
    sum = num1 + num2
    if len(user_ID) != sum:  # VCの人数が(num1 + num2)人か確認
        await ctx.send(f'VCの人数が{sum}人じゃないとチーム分けできません')
        return

    blueteam = []
    redteam = []
    random.shuffle(user_ID)
    blueteam.append(user_ID[0:num1])  # シャッフルしたuser_IDの1~num1番目をblueteamにnum1~sum番目をredteamに追加することでランダムに
    redteam.append(user_ID[num1:])

    for i in range(num1):  # ユーザーIDからユーザーを取得して振り分けられたチームのチャンネルに移動させる
        blueteam.append(user_ID[i])
        bluemem = await guild.fetch_member(blueteam[i])
        await bluemem.move_to(blue_team)

    for i in range(num2):
        redteam.append(user_ID[num1 + i])
        redmem = await guild.fetch_member(redteam[i])
        await redmem.move_to(red_team)

    message = "-----赤チーム-----" + bot.get_user(*redteam).display_name + "-----青チーム-----" + bot.get_user(*blueteam).display_name
    await ctx.send(message)
    # await ctx.send(*[bot.get_user(ID).display_name for ID in user_ID])
    # ユーザーネームはサーバーごとに変えれるのでそのサーバーでの名前display_nameを表示


@bot.command()
async def lolinfo(ctx, arg):
    # RiotのAPIサーバーがよく落ちていてその時はbadrequestを返す。それを判別して返答する機能も欲しい
    watcher = LolWatcher(key)
    # 情報を取得するリージョン（地域）とユーザー名を設定
    region = 'jp1'
    summonername = arg
    me = watcher.summoner.by_name(region, summonername)
    my_ranked_stats = watcher.league.by_summoner(region, me['id'])  # その人のランクを取得
    recentmatchlists = watcher.match.matchlist_by_puuid(region, me['accountId'])  # 最近のマッチ履歴を取得
    await ctx.send(recentmatchlists)
    await ctx.send(my_ranked_stats)


token = getenv('DISCORD_BOT_TOKEN')  # HEROKUの環境設定のほうに書いてあるtokenを取得
bot.run(token)
