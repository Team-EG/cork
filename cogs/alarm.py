import re
import datetime
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
                               "알림내용",
                               "알림의 내용입니다.",
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
    async def alarm_pin(self, ctx: SlashContext, name, content, _type):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        if _type == "repeat":
            await self.bot.db.exec_sql("""INSERT INTO repeat VALUES (?,?,?,?,?,?,?,?,?)""",
                                       (None, None, None, None, user_id, name, channel_id, None, content))
        else:
            await self.bot.db.exec_sql("""INSERT INTO alarm VALUES (?,?,?,?,?,?,?,?,?)""",
                                       (None, None, None, None, None, user_id, name, channel_id, content))
        await ctx.send(content="성공적으로 알림 기본 설정을 이 채널에 추가했어요!\n"
                               "알림을 작동시키기 위해서는 `/set 보기` 명령어를 참고해주세요.",
                       complete_hidden=True)

    @cog_ext.cog_subcommand(base="set",
                            name="보기",
                            guild_ids=guild_ids)
    async def alarm_set(self, ctx: SlashContext):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        repeats = await self.bot.db.res_sql("""SELECT * FROM repeat WHERE user_id=? AND channel_id=?""",
                                            (user_id, channel_id))
        repeats = [x for x in repeats if
                   not x["min"] and not x["hour"] and not x["type"] and not x["duration"] and not x["last_called_at"]]
        alarms = await self.bot.db.res_sql("""SELECT * FROM alarm WHERE user_id=? AND channel_id=?""",
                                           (user_id, channel_id))
        alarms = [x for x in alarms if
                  not x["min"] and not x["hour"] and not x["date"] and not x["month"] and not x["year"]]
        embed = discord.Embed(title="설정해야 하는 알림 리스트",
                              description="`반복` 타입은 `/set 반복` 명령어로 설정해주시고,\n"
                                          "`알림` 타입은 `/set 알림` 명령어로 설정해주세요.",
                              timestamp=self.bot.get_kst())
        embed.add_field(name="반복 타입", value="없음 (만약에 잘못된 것 같다면 채널을 확인해주세요.)" if not repeats else "`" + ("`, `".join(
            [f"{x['name']}" for x in repeats]
        )) + "`")
        embed.add_field(name="알림 타입", value="없음 (만약에 잘못된 것 같다면 채널을 확인해주세요.)" if not alarms else "`" + ("`, `".join(
            [f"{x['name']}" for x in alarms]
        )) + "`")
        await ctx.send(embeds=[embed])

    @cog_ext.cog_subcommand(base="set",
                            name="반복",
                            guild_ids=guild_ids)
    async def alarm_set_repeat(self, ctx: SlashContext, name, _min, hour, _type, opt=None, *args):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        is_alarm = await self.bot.db.res_sql("""SELECT * FROM repeat WHERE name=? AND user_id=? AND channel_id=?""",
                                             (name, user_id, channel_id))
        if not is_alarm:
            return await ctx.send(content="해당 알림은 존재하지 않습니다. 채널과 이름을 확인해주세요.", complete_hidden=True)
        if _type == "daily" and opt:
            return await ctx.send(content="잘못된 입력입니다. (`날마다` 타입은 옵션을 입력하면 안됩니다!)", complete_hidden=True)
        if _type != "daily" and opt is None:
            return await ctx.send(content="잘못된 입력입니다. (옵션은 `날마다` 타입을 빼면 무조건 입력해야 합니다!)", complete_hidden=True)
        if _type == "yearly" and not re.findall("^[01][0-9]-[0-3][0-9]$", opt):
            return await ctx.send(content="잘못된 입력입니다. (`월-일`은 `MM-DD` 양식으로 입력해주세요!)", complete_hidden=True)
        if args:
            return await ctx.send(content="잘못된 입력입니다. (옵션은 하나만 입력해야 합니다!)", complete_hidden=True)
        if _type == "daily":
            await self.bot.db.exec_sql(f"""UPDATE repeat SET min=?, hour=?, type=? WHERE name=? AND user_id=? AND channel_id=?""",
                                       (_min, hour, _type, name, user_id, channel_id))
        else:
            await self.bot.db.exec_sql(f"""UPDATE repeat SET min=?, hour=?, type=?, duration=? WHERE name=? AND user_id=? AND channel_id=?""",
                                       (_min, hour, _type, opt, name, user_id, channel_id))
        await ctx.send(content=f"성공적으로 `{name}` 반복 알림을 설정했습니다!", complete_hidden=True)

    @cog_ext.cog_subcommand(base="set",
                            name="알림",
                            guild_ids=guild_ids)
    async def alarm_set_alarm(self, ctx: SlashContext, name, _min, hour, day, month, year):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        is_alarm = await self.bot.db.res_sql("""SELECT * FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                             (name, user_id, channel_id))
        if not is_alarm:
            return await ctx.send(content="해당 알림은 존재하지 않습니다. 채널과 이름을 확인해주세요.", complete_hidden=True)
        today = datetime.datetime.now()
        if day == 0:
            day = today.day
        if month == 0:
            month = today.month
        if year == 0:
            year = today.year
        await self.bot.db.exec_sql("""UPDATE alarm SET min=?, hour=?, date=?, month=?, year=? WHERE name=? AND user_id=? AND channel_id=?""",
                                   (_min, hour, day, month, year, name, user_id, channel_id))
        await ctx.send(content=f"성공적으로 `{name}` 알림을 설정했습니다!", complete_hidden=True)

    @cog_ext.cog_slash(name="remove",
                       description="선택한 알림을 삭제합니다.",
                       guild_ids=guild_ids,
                       options=[
                           manage_commands.create_option(
                               "알림타입",
                               "알림의 타입입니다.",
                               3,
                               True,
                               [manage_commands.create_choice("alarm", "알림"), manage_commands.create_choice("repeat", "반복")]
                           ),
                           manage_commands.create_option(
                               "알림이름",
                               "지울 알림의 이름입니다.",
                               3,
                               True
                           )
                       ])
    async def remove(self, ctx: SlashContext, _type, name):
        channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
        user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
        if _type == "alarm":
            is_alarm = await self.bot.db.res_sql("""SELECT * FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                 (name, user_id, channel_id))
            if not is_alarm:
                return await ctx.send(content="해당 알림은 존재하지 않습니다. 채널과 이름을 확인해주세요.", complete_hidden=True)
            await self.bot.db.exec_sql("DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?",
                                       (name, user_id, channel_id))
        elif _type == "repeat":
            is_alarm = await self.bot.db.res_sql("""SELECT * FROM repeat WHERE name=? AND user_id=? AND channel_id=?""",
                                                 (name, user_id, channel_id))
            if not is_alarm:
                return await ctx.send(content="해당 알림은 존재하지 않습니다. 채널과 이름을 확인해주세요.", complete_hidden=True)
            await self.bot.db.exec_sql("DELETE FROM repeat WHERE name=? AND user_id=? AND channel_id=?",
                                       (name, user_id, channel_id))
        await ctx.send(content="성공적으로 해당 알림을 삭제했어요!", complete_hidden=True)

    @cog_ext.cog_slash(name="list",
                       description="등록된 알림 리스트를 봅니다.",
                       guild_ids=guild_ids,
                       options=[
                           manage_commands.create_option(
                               "범위",
                               "표시할 알림의 범위입니다.",
                               3,
                               True,
                               [manage_commands.create_choice("personal", "자신 전체"),
                                manage_commands.create_choice("channel", "이 채널 전체")]
                           )
                       ])
    async def alarm_list(self, ctx: SlashContext, _type):
        if _type == "personal":
            user_id = ctx.author.id if not isinstance(ctx.author, int) else ctx.author
            alarm_list = await self.bot.db.res_sql("""SELECT * FROM alarm WHERE user_id=?""", (user_id,))
            repeat_list = await self.bot.db.res_sql("""SELECT * FROM repeat WHERE user_id=?""", (user_id,))
        else:
            channel_id = ctx.channel.id if not isinstance(ctx.channel, int) else ctx.channel
            alarm_list = await self.bot.db.res_sql("""SELECT * FROM alarm WHERE channel_id=?""", (channel_id,))
            repeat_list = await self.bot.db.res_sql("""SELECT * FROM repeat WHERE channel_id=?""", (channel_id,))
        embed = discord.Embed(title="등록된 알림 리스트")
        embed.add_field(name="반복 타입", value="없음" if not repeat_list else "`" + ("`, `".join(
            [f"{x['name']}" for x in repeat_list]
        )) + "`")
        embed.add_field(name="알림 타입", value="없음" if not alarm_list else "`" + ("`, `".join(
            [f"{x['name']}" for x in alarm_list]
        )) + "`")
        await ctx.send(embeds=[embed])


def setup(bot):
    bot.add_cog(Alarm(bot))
