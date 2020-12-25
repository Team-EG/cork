import discord
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
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        if _type == "repeat":
            await self.bot.db.exec_sql("""INSERT INTO repeat VALUES (?,?,?,?,?,?,?,?)""",
                                       (None, None, None, None, user_id, name, channel_id, None))
        else:
            await self.bot.db.exec_sql("""INSERT INTO alarm VALUES (?,?,?,?,?,?,?,?)""",
                                       (None, None, None, None, None, user_id, name, channel_id))
        await ctx.send(content="성공적으로 알림 기본 설정을 이 채널에 추가했어요!\n"
                               "알림을 작동시키기 위해서는 `/set` 명령어를 참고해주세요.")

    @cog_ext.cog_slash(name="set",
                       description="알림 세부 설정 관련 명령어입니다.",
                       guild_ids=guild_ids)
    async def alarm_set(self, ctx: SlashContext):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        repeats = await self.bot.db.res_sql("""SELECT name FROM repeat WHERE user_id=? AND channel_id=?""",
                                            (user_id, channel_id))
        repeats = [x for x in repeats if
                   not x["min"] and not x["hour"] and not x["type"] and not x["duration"] and not x["last_called_at"]]
        alarms = await self.bot.db.res_sql("""SELECT name FROM repeat WHERE user_id=? AND channel_id=?""",
                                           (user_id, channel_id))
        alarms = [x for x in alarms if
                  not x["min"] and not x["hour"] and not x["date"] and not x["month"] and not x["year"]]
        embed = discord.Embed(title="설정해야 하는 알림 리스트",
                              description="`반복` 타입은 `/set 반복 <이름> <분> <시간> <반복 주기> <옵션(특정 주기마다로 설정한 경우):반복할 주기(일)>` "
                                          "명령어로 설정해주시고,\n `알림` 타입은 "
                                          "`/set 알림 <이름> <분> <시간> <일> <월> <년도>` 명령어로 설정해주세요.")
        embed.add_field(name="반복 타입", value="없음" if not repeats else "`" + ("`, `".join(
            [f"{x['name']}" for x in repeats]
        )) + "`")
        embed.add_field(name="알림 타입", value="없음" if not alarms else "`" + ("`, `".join(
            [f"{x['name']}" for x in alarms]
        )) + "`")
        await ctx.send(embeds=[embed])

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
