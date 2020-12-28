import discord
from discord.ext import commands


class Etc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hellothisisverification")
    async def htiv(self, ctx):
        await ctx.send("eunwoo1104#9600 (ID: 288302173912170497)")


def setup(bot):
    bot.add_cog(Etc(bot))
