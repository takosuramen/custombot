from discord import ext
from discord.ext import commands
import discord
from os import getenv
import traceback
import random


discord.Intents.members = True
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


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


@bot.command()
async def ping(ctx):  # BOTが稼働してるかどうか確認用
    await ctx.send('HELLO!')


@bot.command()
async def lol(ctx):
    await ctx.send('lololo')


@bot.command()
async def custom(ctx):  # カスタムチーム分けBOT
    user_name = [member.name for member in ctx.author.voice.channel.members]  # コマンドを打ち込んだ人がいるVCに接続しているメンバーの名前を取得
    user_ID = [member.id for member in ctx.author.voice.channel.members]      # 同IDを取得
    await ctx.send("VCに" + str(len(user_ID)) + "人接続しています")
    await ctx.send(*user_ID)
    random.shuffle(user_ID)
    await ctx.send(*[bot.get_user(ID).display_name for ID in user_ID])        # ユーザーネームはサーバーごとに変えれるのでそのサーバーでの名前display_nameを表示


token = getenv('DISCORD_BOT_TOKEN')  # HEROKUの環境設定のほうに書いてあるtokenを取得
bot.run(token)
