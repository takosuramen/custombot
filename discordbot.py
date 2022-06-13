from discord.ext import commands
import discord
from os import getenv
import traceback
import random
import datetime
from riotwatcher import LolWatcher, ApiError

intents = discord.Intents.default()
intents.members = True  # これをしないとget_memberとかできなくなる
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)  # command_prefixはコマンドの前につけるやつ　スラッシュコマンドはdiscordのもともとついている機能と被るため$にした

# BOT関連の発言をするテキストチャンネルおよびチーム振り分け待機VC、赤チーム青チームVCのチャンネルID
"""
BOT_COMMAND_CHANNEL_ID = 892796029362139170  # こっちはテストサーバー用
taikibeya_ID = 892796029362139172
red_team_ID = 948050118031077376
blue_team_ID = 948050118572138536
"""
BOT_COMMAND_CHANNEL_ID = 951092799623790622  # 本サーバー用
taikibeya_ID = 707947337770860574
red_team_ID = 270573338752057355
blue_team_ID = 269884896258818049

key = getenv('riotkey')  # herokuの環境設定においてあるriot apiキー　申請通ったので無期限でリクエスト制限も緩め


@bot.event
async def on_command_error(ctx, error):  # エラーはいたときに教えてくれるやつ
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    await ctx.send("$helpを参考にコマンドを入力してみてね"


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
    await ctx.send('```$ping```BOTが稼働してたらHELLOと返事を返すよ\n'
                   '```$custom or $custom <青チームの人数> <赤チームの人数>```カスタム待機部屋にいる人をランダムに青赤にわけるよ(指定しないと5:5)\n'
                   '```$rank <サモナー名>```その人のランク情報を表示するよ')


@bot.command()
async def blue(ctx):  # 発言者をblueチームに送るコマンド ちゃんとユーザーを移動させることができるかテスト用
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
async def custom(ctx, num1: int = 5, num2: int = 5):  # カスタムチーム分けbot 青チーム赤チーム5人ずつランダムに分ける argが指定されたらその人数ずつにわける
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
    await ctx.send(f'青チーム{num1}人赤チーム{num2}人でチーム分けをします')

    blueteam = []
    redteam = []
    random.shuffle(user_ID)
    blueteam.extend(user_ID[0:num1])  # シャッフルしたuser_IDの1~num1番目をblueteamにnum1~sum番目をredteamに追加することでランダムに
    redteam.extend(user_ID[num1:])

    nameb = ''
    namer = ''

    for i in range(num1):  # ユーザーIDからユーザーを取得して振り分けられたチームのチャンネルに移動させる
        # blueteam.append(user_ID[i])
        bluemem = await guild.fetch_member(blueteam[i])
        await bluemem.move_to(blue_team)
        nameb.append(f"@{bluemem}\n")

    for i in range(num2):
        # redteam.append(user_ID[num1 + i])
        redmem = await guild.fetch_member(redteam[i])
        await redmem.move_to(red_team)
        namer.append(f"@{redmem}\n")
    """
    embed = discord.Embed(title='カスタムチーム分け', color=0xfc7b03)
    embed.add_field(name='青チーム', value=bluemem, inline=True)
    embed.add_field(name='赤チーム', value=redmem, inline=True)
    await ctx.send(embed=embed)
    """
    # message = "-----赤チーム-----" + [bot.get_user(redteam[ID]).display_name for ID in len(redteam)] + "-----青チーム-----" + [bot.get_user(blueteam[ID]).display_name for ID in len(blueteam)]
    # await ctx.send(message)
    # await ctx.send(*[bot.get_user(ID).display_name for ID in user_ID])
    # ユーザーネームはサーバーごとに変えれるのでそのサーバーでの名前display_nameを表示


@bot.command()
async def rank(ctx, *args):
    # RiotのAPIサーバーがおちている時はbadrequestを返す?それを判別して返答する機能も欲しい
    watcher = LolWatcher(key)
    """
    情報を取得するリージョン（地域）とユーザー名を設定
    LOLのユーザー名はスペースを入れることもできるので*argsで複数引数をもらってから全部結合
    """
    region = 'jp1'
    arg = ''.join(args)

    # 429:APIのリクエスト数制限に引っかかってたら出る
    # 404:入力されたsummoner名が存在するかどうかを判定し存在しなかったら出る
    try:
        me = watcher.summoner.by_name(region, arg)
    except ApiError as err:
        if err.response.status_code == 429:
            await ctx.send('try again later')
            return
        elif err.response.status_code == 404:
            await ctx.send(f'{arg}は存在しません')
            return
        else:
            raise
            return

    # 今のゲームのバージョンを受け取る（ゲーム内のプロフィールアイコンなどdatadragonのデータを利用する際に必要になる）
    versions = watcher.data_dragon.versions_for_region(region)
    champions_version = versions['n']['champion']
    # await ctx.send(champions_version)

    rank = watcher.league.by_summoner(region, me['id'])
    # await ctx.send(f'{rank[0]["summonerName"]}   {rank[0]["tier"]} {rank[0]["rank"]} {rank[0]["leaguePoints"]}LP')

    # discordのテキストチャットの埋め込み装飾embedの生成
    embed = discord.Embed(title="Solo Queue", color=0x00ffff)
    embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{me['profileIconId']}.png")
    if rank:
        embed.add_field(name=rank[0]["summonerName"], value=f'{rank[0]["tier"]} {rank[0]["rank"]} {rank[0]["leaguePoints"]}LP', inline=False)
    else:
        embed.add_field(name=me["name"], value='ランクなし', inline=False)
    await ctx.send(embed=embed)

    recentmatchlists = watcher.match.matchlist_by_puuid('asia', me['puuid'], type='ranked')
    # 最近のマッチ履歴を取得、デフォルトは20試合を取得,ソロランクの試合のみを取得
    # await ctx.send(recentmatchlists)
    """
    マッチ履歴からプレイヤーが所属しているチーム側の勝敗を判定し表示
    マッチデータの中にはそのマッチに参加していた10人分のデータが格納されているので
    入力されたsummonerのpuuidと一致するデータの勝敗だけカウントする
    """
    winloss = '最近の勝敗'
    win = 0
    loss = 0
    for num in recentmatchlists:
        match_data = watcher.match.by_id('asia', num)
        for i in match_data['info']['participants']:
            if me['puuid'] in i['puuid']:
                if i['win']:
                    winloss += 'o'
                    win += 1
                else:
                    winloss += 'x'
                    loss += 1
    await ctx.send(f'{winloss}\n直近{win+loss}試合 {win}勝{loss}敗')

token = getenv('DISCORD_BOT_TOKEN')  # HEROKUの環境設定のほうに書いてあるtokenを取得
bot.run(token)
