import asyncio
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
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
        await ctx.send(content=f"퐁! ({round(self.bot.latency * 1000)}ms)")

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

    @cog_ext.cog_slash(name="타이머",
                       description="타이머 기능입니다.",
                       guild_ids=guild_ids,
                       options=[
                           manage_commands.create_option(
                               "분",
                               "분입니다.",
                               4,
                               True
                           ),
                           manage_commands.create_option(
                               "초",
                               "초입니다.",
                               4,
                               True
                           )])
    async def utils_timer(self, ctx: SlashContext, mins, secs):
        secs += mins * 60
        await ctx.send(content=f"타이머가 설정되었어요! {self.parse_second(secs)} 뒤에 알려드릴게요!")
        await asyncio.sleep(secs)
        await ctx.channel.send(f"{ctx.author.mention} 타이머가 울렸어요!")

    @cog_ext.cog_slash(name="크레딧", description="봇 개발자를 보여줍니다.", guild_ids=guild_ids)
    async def utils_credit(self, ctx: SlashContext):
        embed = discord.Embed(title="코르크봇 크레딧", description="Developed at KOREANBOTS Hackathon S1.")
        embed.add_field(name="봇 개발", value="eunwoo1104#9600 (ID: 288302173912170497)")
        embed.add_field(name="봇 기획", value="레이니#5747 (ID: 558323117802389514)")
        await ctx.send(embeds=[embed])


def setup(bot):
    bot.add_cog(Utils(bot))
