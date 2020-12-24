import json
import discord
from discord.ext import commands
# from discord_slash import SlashCommand


class CorkClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.slash = SlashCommand(self)

    @staticmethod
    def get_settings(key: str):
        with open("bot_settings.json", "r") as f:
            return json.load(f).get(key)
