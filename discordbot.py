from discord.ext import commands
import discord
from os import getenv
import traceback
import random

intents = discord.Intents.default()
intents.members = True  # これをしないとget_memberとかできなくなる
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

BOT_COMMAND_CHANNEL_ID = 951092799623790622  # 892796029362139170
taikibeya_ID = 707947337770860574  # 892796029362139172  # こっちはテストサーバー用
red_team_ID = 270573338752057355  # 948050118031077376
blue_team_ID = 269884896258818049  # 948050118572138536


@bot.event
async def on_command_error(ctx, error):  # エラーはいたときに教えてくれるやつ
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_ready():  # BOT起動時にメッセージを送る
    await bot.change_presence(activity=discord.Game(name='こんにちは'))
    # chan = bot.get_channel(BOT_COMMAND_CHANNEL_ID)
    # 再起動するたびにうるさいので一回消しとく await chan.send("準備完了! $help でコマンドを確認できるよ")


@bot.command()
async def ping(ctx):
    """BOTが稼働してるかどうか確認"""
    await ctx.send('HELLO!')


@bot.command()
async def help(ctx):
    await ctx.send('$ping\n    BOTが稼働してたらHELLOと返事を返すよ\n$custom\n    カスタム待機部屋にいる人を自動的にRED,BLUEにわけるよ\n    コマンドを打つ人がVCにいてVCの人数が10人じゃないといけないよ')


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
async def custom(ctx):  # カスタムチーム分けbot 10人を赤チーム青チーム5人ずつランダムに分ける
    red_team = bot.get_channel(red_team_ID)
    blue_team = bot.get_channel(blue_team_ID)
    taikibeya = bot.get_channel(taikibeya_ID)
    guild = ctx.guild
    #  user_name = [member.name for member in taikibeya.members]  # カスタム待機部屋に接続しているメンバーの名前を取得　IDだけでいいかも
    user_ID = [member.id for member in taikibeya.members]         # 同IDを取得
    await ctx.send("VCに" + str(len(user_ID)) + "人接続しています")
    if len(user_ID) != 10:  # VCの人数が10人か確認
        await ctx.send('VCの人数が10人じゃないとチーム分けできません')
        return

    blueteam = []
    redteam = []
    random.shuffle(user_ID)
    blueteam.append(user_ID[1:6])  # シャッフルしたuser_IDの1~5番目をblueteamに6~10番目をredteamに追加することでランダムに
    redteam.append(user_ID[6:11])

    for i in range(5):
        bluemem = await guild.fetch_member(blueteam[i])
        redmem = await guild.fetch_member(redteam[i])
        await bluemem.move_to(blue_team)
        await redmem.move_to(red_team)

    await ctx.send("-----赤チーム-----" + bot.get_user(*red_team).display_name + "-----青チーム-----" + bot.get_user(*blue_team).display_name)
    # await ctx.send(*[bot.get_user(ID).display_name for ID in user_ID])
    # ユーザーネームはサーバーごとに変えれるのでそのサーバーでの名前display_nameを表示

token = getenv('DISCORD_BOT_TOKEN')  # HEROKUの環境設定のほうに書いてあるtokenを取得
bot.run(token)
