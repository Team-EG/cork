import traceback
from discord.ext import commands
from discord_slash import SlashContext
from modules.client import CorkClient


class Events(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, ex):
        if not ctx.sent:
            await ctx.send(5)
        str_ex = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        await ctx.send(content="이런! 명령어를 실행하던 도중 오류가 발생했어요...\n"
                               f"```py\n{str_ex}\n```")


def setup(bot):
    bot.add_cog(Events(bot))
