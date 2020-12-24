from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from modules.client import CorkClient
from modules.guild_ids import guild_ids


class Alarm(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="pin",
                       description="알림 관련 명령어들입니다.",
                       options=[
                           manage_commands.create_option(
                               "알림이름",
                               "알림의 이름입니다.",
                               3,
                               True
                           ),
                           manage_commands.create_option(
                               "타입",
                               "알림 타입입니다.",
                               3,
                               True,
                               choices=[
                                   manage_commands.create_choice(
                                       "repeat",
                                       "반복"
                                   ),
                                   manage_commands.create_choice(
                                       "alarm",
                                       "알림"
                                   )
                               ]
                           )
                       ],
                       guild_ids=guild_ids)
    async def alarm_pin(self, ctx: SlashContext, name, _type):
        await ctx.send(content="아직 준비되지 않은 기능이에요!")
        await ctx.channel.send(
            f"DEBUG: 알림이름: {name} | 타입: {_type}"
        )

    @cog_ext.cog_slash(name="set",
                       guild_ids=guild_ids)
    async def alarm_set(self, ctx: SlashContext):
        await ctx.send(5)

    @cog_ext.cog_subcommand(base="set",
                            name="반복",
                            guild_ids=guild_ids)
    async def alarm_set_repeat(self, ctx: SlashContext):
        await ctx.send(5)

    @cog_ext.cog_subcommand(base="set",
                            name="알림",
                            guild_ids=guild_ids)
    async def alarm_set_alarm(self, ctx: SlashContext):
        await ctx.send(5)


def setup(bot):
    bot.add_cog(Alarm(bot))
