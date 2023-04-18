import disnake
import re
import pymorphy2
import youtube_dl

from disnake import FFmpegPCMAudio
from disnake.ext import commands
from youtube_dl import YoutubeDL


bot = commands.Bot(command_prefix='>', intents=disnake.Intents.all(), test_guilds=[1045685662839488533])


ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'default_search': 'auto',
    'outtmpl': './%(title)s.%(ext)s'
}


@bot.event
async def on_ready():
    print(f'Бот ({bot.user}) готов к работе!')


@bot.event
async def on_member_join(member: disnake.Member):
    role = member.guild.get_role(1045688823885074492)
    role2 = member.guild.get_role(1045691062439657493)
    role3 = member.guild.get_role(1045698807624642691)
    role4 = member.guild.get_role(1045698531127738418)
    channel = member.guild.system_channel

    embed = disnake.Embed(
        title="Новый охотник!",
        description=f"{member.mention}\n"
                    f"получает роль: {role.name}\n"
                    f"получает роль: {role2.name}\n"
                    f"получает роль: {role3.name}\n"
                    f"получает роль: {role4.name}\n",
        color=0xFF0000
    )

    await member.add_roles(role)
    await member.add_roles(role2)
    await member.add_roles(role3)
    await member.add_roles(role4)
    await channel.send(embed=embed)


morph = pymorphy2.MorphAnalyzer(lang='ru')

CENSORED_WORDS = ["jacek", "banana", "africa", "monke", "monkey", "dick", "yacek"]
CENSORED_RU_WORDS = ["хуй", "пизда", "залупа", "яцек", "обезьяна", "примат", "африка"]
CENSORED_WORDS.extend(CENSORED_RU_WORDS)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    print(message.content)
    if (message.content and message.content.isascii()) or re.match(r'[А-Яа-я]+', message.content):
        words = re.findall(r"\w+", message.content.lower())
        lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
        censored = set(lemmatized_words) & set(CENSORED_WORDS)

        if censored:
            await message.channel.send(f"{message.author.mention}, такого писать здесь незя, ПИДОРАС!", delete_after=10)
            await message.delete()

last_message_time = {}


@bot.slash_command(name="Jacek".lower(), description="Скажет 1% правды о Яцеке")
async def Jacek(ctx, num: int):
    for i in range(num):
        await ctx.send("Яцек пидорас!", delete_after=10)


@bot.slash_command(name="Chushka".lower(), description="Пошлет мусор кому угодно")
async def Chushka(ctx, member: disnake.Member, send: str):
    await ctx.send(f'Чел {member.mention} -> {send}!')
    await ctx.message.delete


@bot.slash_command(name="Nigger".lower(), description="Скажет кому-то, что он нигер")
async def Chushka(ctx, member: disnake.Member):
    await ctx.send(f'Чел {member.mention} -> настоящий NIGGER!')
    await ctx.message.delete


@bot.slash_command(name='fap', description='Призыв + послание + определенное кол-во раз')
async def fap(ctx, member: disnake.Member, text: str, times: int):
    for i in range(times):
        await ctx.send(f'{member.mention}, {text}! Иди сюда, БЛЯТЬ!')


@bot.slash_command(name="calculator",
                   description="Посчитает, что-то за тебя дЭбила! (x+y || x-y || x/y || x*y || y^(1/x))")
async def culc(inter, x: int, oper: str, y: int):
    if oper == "+":
        result = x + y
    elif oper == "-":
        result = x - y
    elif oper == "/":
        result = x / y
    elif oper == "*":
        result = x * y
    elif oper == "sqrt":
        result = y ** (1 / x)
    else:
        result = "Проеб где-то!"

    if result % 1 == 0:
        await inter.send(f"Ответ = {str(result)}")
    else:
        await inter.send(result)


@bot.command()
async def play(ctx, *, query: str):
    vc = ctx.author.voice.channel
    if not vc:
        return await ctx.send("Вы должны быть в голосовом канале, чтобы использовать эту команду")

    try:
        await vc.connect()
    except disnake.ClientException:
        pass

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        except youtube_dl.utils.DownloadError:
            return await ctx.send("Не удалось найти видео на YouTube")

        url = info['url']
        title = info['title']
        length = info['duration']
        uploader = info['uploader']

    embed = disnake.Embed(
        title=title,
        description=f'Uploader: {uploader}\nDuration: {length}',
        url=url,
        color=0xff0000
    )

    player = await vc.connect()
    player.play(disnake.FFmpegPCMAudio(url, options="-vn"))
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостатосно прав для выполнения этой команды!")


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил"):
    await ctx.send(f'Админ {ctx.author.mention} выгнал пользователя {member.mention}', delete_after=5)
    await member.kick(reason=reason)
    await ctx.message.delete


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил"):
    await ctx.send(f'Админ {ctx.author.mention} забанил пользователя {member.mention}', delete_after=5)
    await member.ban(reason=reason)
    await ctx.message.delete


@bot.command()
async def offline(ctx):
    await bot.change_presence(status=disnake.Status.invisible)


@bot.command()
async def online(ctx):
    await bot.change_presence(status=disnake.Status.online)


@bot.command()
async def playing(ctx, game):
    await bot.change_presence(status=disnake.Status.invisible, activity=disnake.Game(name=game))


bot.run("Token")
