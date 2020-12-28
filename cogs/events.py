import traceback
import discord
from discord.ext import commands
from discord_slash import SlashContext
from discord_slash.error import RequestFailure
from modules.client import CorkClient


class Events(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, ex):
        if not ctx.sent:
            try:
                await ctx.send(5)
            except RequestFailure:
                pass
        str_ex = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        await ctx.channel.send(content="이런! 명령어를 실행하던 도중 오류가 발생했어요...\n"
                               f"```py\n{str_ex}\n```")

    @commands.Cog.listener()
    async def on_ready(self):
        print("on_ready Dispatched.")
        await self.bot.change_presence(activity=discord.Game(name="슬래시 커맨드를 확인해보세요!"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            str_ex = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            await ctx.send(content="이런! 명령어를 실행하던 도중 오류가 발생했어요...\n"
                                   f"```py\n{str_ex}\n```")


def setup(bot):
    bot.add_cog(Events(bot))
