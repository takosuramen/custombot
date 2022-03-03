from discord.ext import commands
import discord
from os import getenv
import traceback
import random


discord.Intents.members = True
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


BOT_COMMAND_CHANNEL_ID = 892796029362139170
red_team_ID = 948050118031077376
blue_team_ID = 948050118572138536


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_ready():  # BOT起動時にメッセージを送る
    await bot.change_presence(activity=discord.Game(name="on ready"))
    chan = bot.get_channel(BOT_COMMAND_CHANNEL_ID)
    await chan.send("準備完了! $bothelp でコマンドを確認できるよ")


@bot.command()
async def ping(ctx):
    """BOTが稼働してるかどうか確認"""
    await ctx.send('HELLO!')


@bot.command()
async def bothelp(ctx):
    await ctx.send('$ping\n    BOTが稼働してたらHELLOと返事を返すよ\n$custom\n    カスタム待機部屋にいる人を自動的にRED,BLUEにわけるよ\n    コマンドを打つ人がVCにいてVCの人数が10人じゃないといけないよ')


@bot.command()
async def custom(ctx):
    """カスタムチーム分けBOT"""
    
    if ctx.author.voice.channel is None:  # コマンドを打った人がVCにいるか確認
        await ctx.send("あなたVCにいませんね")
        return
    
    #  user_name = [member.name for member in ctx.author.voice.channel.members]  # コマンドを打ち込んだ人がいるVCに接続しているメンバーの名前を取得
    user_ID = [member.id for member in ctx.author.voice.channel.members]      # 同IDを取得
    if len(user_ID) != 10:  # VCの人数が10人か確認
        await ctx.send('VCの人数が10人じゃないとチーム分けできません')
        return
    
    await ctx.send("VCに" + str(len(user_ID)) + "人接続しています")
    
    
    for i in range(5):
        blueteam.append(member.id[2*i])
        redteam.append(member.id[2*i+1])
    
    for i in range(5)
        bluemem = bot.get_user(blueteam[i])
        redmem = bot.get_user(redteam[i])
        bluemem.move_to(blue_team_ID)
        redmem.move_to(red_team_ID)
    
    random.shuffle(user_ID)
    await ctx.send(*[bot.get_user(ID).display_name for ID in user_ID])        # ユーザーネームはサーバーごとに変えれるのでそのサーバーでの名前display_nameを表示
    


token = getenv('DISCORD_BOT_TOKEN')  # HEROKUの環境設定のほうに書いてあるtokenを取得
bot.run(token)
