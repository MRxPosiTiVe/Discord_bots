import disnake

from disnake.ext import commands


class Guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.joined_guilds = []

    async def on_guild_join(self, guild: disnake.Guild):
        self.joined_guilds.append(guild.id)


def setup(bot: commands.Bot):
    bot.add_cog(Guild(bot))
