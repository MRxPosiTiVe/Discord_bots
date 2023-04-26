import disnake

from disnake.ext import commands


class Shit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='ping', description='Узнать задержку бота')
    async def ping(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.send(f'Пинг нахой {round(self.bot.latency * 1000)} мс')


def setup(bot: commands.Bot):
    bot.add_cog(Shit(bot))
