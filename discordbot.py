from discord.ext import commands
import discord
from os import getenv
import traceback
import random


discord.Intents.members = True
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

BOT_COMMAND_CHANNEL_ID = 892796029362139170
red_team_ID = 948050118031077376
blue_team_ID = 948050118572138536

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

async def on_ready():
    print('We have logged in as {0}'.format(bot.user))


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

async def custom(ctx):
    # bot_text_channnel = client.get_channel(BOT_COMMAND_CHANNEL_ID) ctxで渡されてるかもしれない
    user_name = [member.name for member in ctx.author.voice.channel.members]  # コマンドを打ち込んだ人がいるVCに接続しているメンバーの名前を取得
    user_ID = [member.id for member in ctx.author.voice.channel.members.id]  # Get the ID of the member currently connected to voice chat
    await ctx.send("kanryou")
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
