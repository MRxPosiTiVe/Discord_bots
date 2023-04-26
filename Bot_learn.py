import disnake
import re
import pymorphy2
import youtube_dl
import random

from google.oauth2.credentials import Credentials
from googletrans import Translator
from disnake import FFmpegPCMAudio
from disnake.ext import commands
from youtube_dl import YoutubeDL


root_guilds = [1045685662839488533, 1093494405157113871]
joined_guilds = []
joined_guilds.extend(root_guilds)

bot = commands.Bot(command_prefix='>',
                   intents=disnake.Intents.all(),
                   test_guilds=joined_guilds)

ydl_opts = {'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'logtostderr': False,
            'default_search': 'auto',
            'source_address': '0.0.0.0'  # принудительно задает IP-адрес для запросов
            }

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# creds = Credentials.from_authorized_user_info(info={'client_secret': 'AIzaSyCdA3u2beOpafi2KgodJy3shCKrRXCTgxg'})
# translator = Translator(service_urls=['translate.google.com'], credentials=creds)
# 'AIzaSyCdA3u2beOpafi2KgodJy3shCKrRXCTgxg'


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

    # # Проверяем, что сообщение не от бота и написано на словенском языке
    # if message.author.bot or message.author == bot.user or message.channel.type != disnake.ChannelType.text:
    #     return
    # if translator.detect(message.content).lang != 'sl':
    #     return
    #
    # # Переводим сообщение
    # translation = translator.translate(message.content, dest='ru')
    #
    # # Отправляем перевод в чат
    # await message.channel.send(f"{message.author.mention}, перевод: {translation.text}")


last_message_time = {}


@bot.slash_command(name="Jacek".lower(), description="Скажет 1% правды о Яцеке")
async def Jacek(ctx, num: int):
    for i in range(num):
        await ctx.send("Яцек пидорас!", delete_after=10)
        await ctx.send("Шлюха Самохинская, нелюдь!", delete_after=10)


@bot.slash_command(name="Chushka".lower(), description="Пошлет мусор кому угодно")
async def Chushka(ctx, member: disnake.Member, send: str):
    await ctx.send(f'Чел {member.mention} -> {send}!')


@bot.slash_command(name="Nigger".lower(), description="Скажет кому-то, что он нигер")
async def nigger(ctx, member: disnake.Member):
    await ctx.send(f'Чел {member.mention} -> настоящий NIGGER!')


@bot.slash_command(name='fap', description='Призыв + послание + определенное кол-во раз')
async def fap(ctx, member: disnake.Member, text: str, times: int):
    for i in range(times):
        await ctx.send(f'{member.mention}, {text}! Иди сюда, БЛЯТЬ!')


@bot.slash_command(name='monketest', description='Тест на примата')
async def monkeTest(ctx, num: int):
    lst = [random.randint(1, 100) for i in range(1, 50)]
    if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.mention}, вы являетесь администратором или владельцем сервера, '
                       f'вы точно НЕ примат!')
    elif num > 100:
        await ctx.send(f'{ctx.author.mention}, дЭбил, число должно быть меньше 100! Давай по новой!')

    elif num in lst:
        await ctx.send(f'{ctx.author.mention}, ты прошел тест, шанс того, что ты примат = {random.randint(31, 100)}%')
    else:
        await ctx.send(f'{ctx.author.mention}, ты провалил тест, но шанс того, '
                       f'что ты примат все же есть = {random.randint(1, 30)}%')


@bot.slash_command(description='Какая-то инфа о сервере')
async def server(ctx):
    await ctx.send(f'Название сервера: {ctx.guild.name}\nВсего участинков: {ctx.guild.member_count}\n'
                   f'Уровень чего-то: {ctx.guild.verification_level}')


@bot.slash_command(name="calculator",
                   description="Посчитает, что-то за тебя дЭбила! (x+y || x-y || x/y || x*y || y^(1/x))")
async def culc(inter, x: int, operation: str, y: int):
    if operation == "+":
        result = x + y
    elif operation == "-":
        result = x - y
    elif operation == "/":
        result = x / y
    elif operation == "*":
        result = x * y
    elif operation == "sqrt":
        result = y ** (1 / x)
    else:
        result = "Проеб где-то!"

    if result % 1 == 0:
        await inter.send(f"Ответ = {str(result)}")
    else:
        await inter.send(result)


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
async def playing(ctx, game: str):
    await bot.change_presence(activity=disnake.Game(name=game))
    await ctx.send(f"Теперь я играю в {game}!")


bot.load_extension("cogs.ping")
bot.load_extension("cogs.Guild")
bot.load_extension('cogs.titis')
bot.load_extension('cogs.abtititis')

bot.run("Token")

