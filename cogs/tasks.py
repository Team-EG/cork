import json
import asyncio
import datetime
import discord
from discord.ext import tasks
from discord.ext import commands
from modules.client import CorkClient


class Tasks(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.repeat_alarm_loop.start()
        self.alarm_alarm_loop.start()
        self.bot.loop.create_task(self.check_if_forgotten())
        self.queued = {"repeat": {}, "alarm": {}}

    def cog_unload(self):
        self.repeat_alarm_loop.cancel()
        self.alarm_alarm_loop.cancel()

    async def check_if_forgotten(self):
        await self.bot.wait_until_ready()
        forgotten = await self.bot.db.res_sql("SELECT * FROM forgotten")
        for x in forgotten:
            raw = json.loads(x["raw_data"])
            channel = self.bot.get_channel(raw["channel_id"])
            user = self.bot.get_user(raw["user_id"])
            if not channel:
                if user:
                    try:
                        await user.send(f"이런! `{raw['name']}` 알림을 설정한 채널이 사라져서 발송에 실패했어요."
                                        "알림은 삭제해드릴께요.")
                    except (discord.Forbidden, discord.HTTPException):
                        pass
                self.bot.dispatch("alarm_channel_none", raw["name"], raw["user_id"], raw["channel_id"])
                await self.bot.db.exec_sql("""DELETE FROM forgotten WHERE invoke_at=? AND raw_data=?""",
                                           (x["invoke_at"], x["raw_data"]))
                if "type" in raw.keys():
                    await self.bot.db.exec_sql("""DELETE FROM repeat WHERE name=? AND user_id=? AND channel_id=?""",
                                               (raw["name"], raw["user_id"], raw["channel_id"]))
                else:
                    await self.bot.db.exec_sql("""DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                               (raw["name"], raw["user_id"], raw["channel_id"]))
                continue
            await self.trigger_forgotten(user, channel, raw["name"], x["invoke_at"]+" (예상)")
            await self.bot.db.exec_sql("""DELETE FROM forgotten WHERE invoke_at=? AND raw_data=?""",
                                       (x["invoke_at"], x["raw_data"]))

    @tasks.loop()
    async def repeat_alarm_loop(self):
        await self.bot.wait_until_ready()
        while True: # 그냥 이렇게 해봤어요
            repeats = await self.bot.db.res_sql("""SELECT * FROM repeat""")
            now = datetime.datetime.now()
            for x in repeats:
                if now.strftime("%Y-%m-%d") == x["last_called_at"]:
                    continue
                user = self.bot.get_user(x["user_id"])
                channel = self.bot.get_channel(x["channel_id"])
                if x["type"] == "weekly":
                    week_dict = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
                    if week_dict[x["duration"]] != now.weekday():
                        continue
                elif x["type"] == "monthly":
                    if int(x["duration"]) != now.day:
                        continue
                elif x["type"] == "yearly":
                    mm, dd = x["duration"].split("-")
                    if mm != now.month or dd != now.day:
                        continue
                elif x["type"] == "duration":
                    if x["last_called_at"]:
                        called_at = datetime.datetime.strptime(x["last_called_at"], "%Y-%m-%d")
                        to_call = called_at + datetime.timedelta(days=int(x["duration"]))
                    else:
                        to_call = now
                    # 일단 빠른 개발을 위해 걍 str로 바꿔서 비교합니다.
                    if now.strftime("%Y-%m-%d") != to_call.strftime("%Y-%m-%d"):
                        continue
                if x["hour"] == now.hour:
                    if x["min"] >= now.minute:
                        if not channel:
                            if user:
                                try:
                                    await user.send(f"이런! `{x['name']}` 알림을 설정한 채널이 사라져서 발송에 실패했어요."
                                                    "알림은 삭제해드릴께요.")
                                except (discord.Forbidden, discord.HTTPException):
                                    pass
                            self.bot.dispatch("alarm_channel_none", x["name"], x["user_id"], x["channel_id"])
                            await self.bot.db.exec_sql("""DELETE FROM repeat WHERE name=? AND user_id=? AND channel_id=?""",
                                                       (x["name"], x["user_id"], x["channel_id"]))
                            continue
                        args = (now.strftime("%Y-%m-%d %H:%M:%S"), json.dumps(x))
                        await self.bot.db.exec_sql("""INSERT INTO forgotten VALUES (?,?)""", args)
                        self.prepare_alarm(x["min"], now, user, channel, x["name"], "repeat", x["content"], args)
                        last_called_at = now.strftime("%Y-%m-%d")
                        await self.bot.db.exec_sql(
                            """UPDATE repeat SET last_called_at=? WHERE name=? AND user_id=? AND channel_id=?""",
                            (last_called_at, x["name"], user.id, channel.id)
                        )
            await asyncio.sleep(1)

    @tasks.loop()
    async def alarm_alarm_loop(self):
        await self.bot.wait_until_ready()
        while True:  # 그냥 이렇게 해봤어요
            alarms = await self.bot.db.res_sql("""SELECT * FROM alarm""")
            now = datetime.datetime.now()
            for x in alarms:
                user = self.bot.get_user(x["user_id"])
                channel = self.bot.get_channel(x["channel_id"])
                if x["min"] is None and x["hour"] is None:
                    continue
                if x["year"] == now.year and x["month"] == now.month and x["date"] == now.day and x["hour"] == now.hour:
                    if x["min"] >= now.minute:
                        if not channel:
                            if user:
                                try:
                                    await user.send(f"이런! `{x['name']}` 알림을 설정한 채널이 사라져서 발송에 실패했어요."
                                                    "알림은 삭제해드릴께요.")
                                except (discord.Forbidden, discord.HTTPException):
                                    pass
                            self.bot.dispatch("alarm_channel_none", x["name"], x["user_id"], x["channel_id"])
                            await self.bot.db.exec_sql("""DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                       (x["name"], x["user_id"], x["channel_id"]))
                            continue
                        arg = (now.strftime("%Y-%m-%d %H:%M:%S"), json.dumps(x))
                        self.prepare_alarm(x["min"], now, user, channel, x["name"], "alarm", x["content"], arg)
                        await self.bot.db.exec_sql("""INSERT INTO forgotten VALUES (?,?)""", arg)
                        # 일단 중복 알림이 울리는 것을 방지하기 위해 지웁니다. 어차피 파이썬 루프 안에서는 살아있어서 언제든 복구 가능해요.
                        await self.bot.db.exec_sql("""DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                   (x["name"], user.id, channel.id))
                if x["min"] < now.minute and x["hour"] <= now.hour and x["date"] <= now.day and x["month"] <= now.month and x["year"] <= now.year:
                    # 이경우 확실히 뭔가 엿된게 분명하므로 바로 전송하러 갑니다.
                    orig_time = f"{x['year']}년 {x['month']}월 {x['date']}일 {x['hour']}시 {x['min']}분"
                    self.bot.loop.create_task(self.trigger_forgotten(user, channel, x["name"], orig_time))
                    if await self.bot.db.res_sql("""SELECT * FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                 (x["name"], user.id, channel.id)):
                        await self.bot.db.exec_sql("""DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                   (x["name"], user.id, channel.id))
            await asyncio.sleep(1)

    def prepare_alarm(self, _min, now, user: discord.User, channel: discord.TextChannel, name, _type, cont, raw):
        _min = _min - now.minute
        secs = _min * 60 - now.second
        secs = secs if secs > 0 else 0
        self.bot.loop.create_task(self.ring_alarm(secs, user, channel, name, cont, True, _type, raw))
        self.bot.dispatch("alarm_prepare", _type, name, user, channel)

    async def ring_alarm(self, wait, user: discord.User, channel: discord.TextChannel, name, cont, clr_after, _type, raw=None):
        await asyncio.sleep(wait)
        self.bot.dispatch("alarm_trigger", _type, name, user, channel)
        embed = discord.Embed(title="⏰ 시간이 됐어요!", description=f"설정하신 `{name}` 알림이 울렸어요!", timestamp=self.bot.get_kst())
        embed.add_field(name="알림 내용", value=cont)
        embed.set_footer(text="알림을 확인하셨다면 이모지 반응을 클릭해주세요!")
        try:
            msg = await channel.send(user.mention, embed=embed)
        except (discord.Forbidden, discord.NotFound, discord.HTTPException):
            return
        if clr_after:
            await self.bot.db.exec_sql("""DELETE FROM forgotten WHERE invoke_at=? AND raw_data=?""", raw)
        self.bot.loop.create_task(msg.add_reaction("⏰"))
        try:
            await self.bot.wait_for("reaction_add",
                                    timeout=30,
                                    check=lambda r, u: str(r) == "⏰" and u.id == user.id and r.message.id == msg.id)
            self.bot.loop.create_task(msg.add_reaction("✅"))
        except asyncio.TimeoutError:
            self.bot.dispatch("snooze_trigger", _type, name, user, channel)
            msg = await channel.send("이런! 알림을 확인하지 않으셔서 스누즈 기능이 활성화되었어요. 5분 뒤에 다시 알림을 울릴께요.\n"
                                     "아니면 5분 안에 :alarm_clock: 이모지 반응을 눌러주세요.")
            self.bot.loop.create_task(msg.add_reaction("⏰"))
            try:
                await self.bot.wait_for("reaction_add",
                                        timeout=60*5,
                                        check=lambda r, u: str(r) == "⏰" and u.id == user.id and r.message.id == msg.id)
                await channel.send("스누즈가 취소되었어요.")
                self.bot.dispatch("snooze_cancel", _type, name, user, channel)
            except asyncio.TimeoutError:
                self.bot.loop.create_task(self.ring_alarm(0, user, channel, name, cont, False, _type))

    async def trigger_forgotten(self, user: discord.User, channel: discord.TextChannel, name, orig_time):
        await channel.send(user.mention, embed=discord.Embed(
            title="이런! 울렸어야 하는 알림이 하나 있었네요...",
            description="봇의 오류 때문에 이 알림이 잊혀진 것 같아요.\n"
                        f"알림 이름은 `{name}` 이고, `{orig_time}`때 울렸어야 되는 알림이었어요.",
            timestamp=self.bot.get_kst()
        ))


def setup(bot):
    bot.add_cog(Tasks(bot))
