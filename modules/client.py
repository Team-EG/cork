import json
import logging
import datetime
import discord
from discord.ext import commands
from .sqlite_db import SQLiteDB
from discord_slash import SlashCommand


class CorkClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slash = SlashCommand(self, auto_register=True)
        self.db = SQLiteDB("main")
        self.logger = logging.getLogger("cork")

    @staticmethod
    def get_settings(key: str):
        with open("bot_settings.json", "r") as f:
            return json.load(f).get(key)

    @staticmethod
    def get_kst() -> datetime.datetime:
        return datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
