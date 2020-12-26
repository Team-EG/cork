import asyncio
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from modules.client import CorkClient
from modules.guild_ids import guild_ids


class Utils(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="핑핑핑", description="핑 명령어 입니다.", guild_ids=guild_ids)
    async def utils_ping(self, ctx: SlashContext):
        await ctx.send(content=f"퐁! ({round(self.bot.latency*1000)}ms)")

    @staticmethod
    def parse_second(time: int):
        parsed_time = ""
        if time // (60 * 60) != 0:
            hour = time // (60 * 60)
            time -= hour * (60 * 60)
            parsed_time += f"{hour}시간 "
        if time // 60 != 0:
            minute = time // 60
            time -= minute * 60
            parsed_time += f"{minute}분 "
        parsed_time += f"{time}초"
        return parsed_time

    @cog_ext.cog_slash(name="타이머", description="타이머 기능입니다.", guild_ids=guild_ids)
    async def utils_timer(self, ctx: SlashContext, mins, secs):
        secs += mins*60
        await ctx.send(content=f"타이머가 설정되었어요! {self.parse_second(secs)} 뒤에 알려드릴께요!")
        await asyncio.sleep(secs)
        await ctx.channel.send(f"{ctx.author.mention} 타이머가 울렸어요!")


def setup(bot):
    bot.add_cog(Utils(bot))
