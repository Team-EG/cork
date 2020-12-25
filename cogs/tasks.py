import re
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

    def cog_unload(self):
        self.repeat_alarm_loop.cancel()
        self.alarm_alarm_loop.cancel()

    @tasks.loop()
    async def repeat_alarm_loop(self):
        while True: # 그냥 이렇게 해봤어요
            pass

    @tasks.loop()
    async def alarm_alarm_loop(self):
        while True:  # 그냥 이렇게 해봤어요
            pass


def setup(bot):
    bot.add_cog(Tasks(bot))
