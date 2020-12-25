import re
import asyncio
import datetime
import discord
from discord.ext import tasks
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from modules.client import CorkClient
from modules.guild_ids import guild_ids


class Tasks(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.repeat_alarm_loop.start()
        self.alarm_alarm_loop.start()
        self.queued = {"repeat": {}, "alarm": {}}

    def cog_unload(self):
        self.repeat_alarm_loop.cancel()
        self.alarm_alarm_loop.cancel()

    @tasks.loop()
    async def repeat_alarm_loop(self):
        await self.bot.wait_until_ready()
        while True: # 그냥 이렇게 해봤어요
            repeats = await self.bot.db.res_sql("""SELECT * FROM repeat""")
            now = datetime.datetime.now()
            for x in repeats:
                user = self.bot.get_user(x["user_id"])
                channel = self.bot.get_channel(x["channel_id"])
                if user.id not in self.queued["repeat"].keys():
                    self.queued["repeat"][user.id] = {}
                if channel.id not in self.queued["repeat"][user.id].keys():
                    self.queued["repeat"][user.id][channel.id] = []
                if x["name"] in self.queued["repeat"][user.id][channel.id]:
                    continue
                if x["type"] == "daily":
                    if x["hour"] == now.hour:
                        if x["min"] < now.minute:
                            continue
                        _min = x["min"] - now.minute
                        secs = _min*60 - now.second
                        secs = secs if secs > 0 else 0
                        self.bot.loop.create_task(self.ring_alarm(secs, user, channel, x["name"], True))
                        self.queued["repeat"][user.id][channel.id].append(x["name"])
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
                if user.id not in self.queued["alarm"].keys():
                    self.queued["alarm"][user.id] = {}
                if channel.id not in self.queued["alarm"][user.id].keys():
                    self.queued["alarm"][user.id][channel.id] = []
                if x["name"] in self.queued["alarm"][user.id][channel.id]:
                    continue
                if x["year"] == now.year:
                    if x["month"] == now.month:
                        if x["date"] == now.day:
                            if x["hour"] == now.hour:
                                if x["min"] >= now.minute:
                                    _min = x["min"] - now.minute
                                    secs = _min * 60 - now.second
                                    secs = secs if secs > 0 else 0
                                    self.bot.loop.create_task(self.ring_alarm(secs, user, channel, x["name"], True))
                                    self.queued["alarm"][user.id][channel.id].append(x["name"])
                                await self.bot.db.exec_sql("""DELETE FROM alarm WHERE name=? AND user_id=? AND channel_id=?""",
                                                           (x["name"], user.id, channel.id))
            await asyncio.sleep(1)

    async def ring_alarm(self, wait, user: discord.User, channel: discord.TextChannel, name, clr_after):
        await asyncio.sleep(wait)
        embed = discord.Embed(title="⏰ 시간이 됐어요!", description=f"설정하신 `{name}` 알림이 울렸어요!")
        await channel.send(user.mention, embed=embed)
        if clr_after:
            _list = self.queued["repeat"][user.id][channel.id]
            self.queued["repeat"][user.id][channel.id] = [x for x in _list if x != name]


def setup(bot):
    bot.add_cog(Tasks(bot))
