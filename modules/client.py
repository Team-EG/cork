import json
import logging
import datetime
import koreanbots
from discord.ext import commands
from .sqlite_db import SQLiteDB
from discord_slash import SlashCommand


class CorkClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = self.get_settings("debug")
        self.slash = SlashCommand(self, auto_register=True)
        self.db = SQLiteDB("main")
        self.logger = logging.getLogger("cork")
        self.koreanbots = koreanbots.Client(self, self.get_settings("kor_token"), postCount=not self.debug)

    def run_bot(self):
        self.run(self.get_settings("canary_token" if self.debug else "token"))

    @staticmethod
    def get_settings(key: str):
        with open("bot_settings.json", "r") as f:
            return json.load(f).get(key)

    @staticmethod
    def get_kst() -> datetime.datetime:
        return datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
