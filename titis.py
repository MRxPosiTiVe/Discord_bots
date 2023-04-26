import disnake
import random

from disnake.ext import commands


class Idk(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Призывает пидора!")
    async def titis(self, ctx: disnake.ApplicationCommandInteraction):
        lst = ['гОндон', 'пИдор', 'гей', 'чепух', 'шиншила', 'негр', 'бебра', 'хуй']
        word = random.choice(lst)
        await ctx.send(f'<@352337037459980289>, иди сюда, {word}!')


def setup(bot: commands.Bot):
    bot.add_cog(Idk(bot))
