import discord
from discord.ext import commands
# from discord_slash import SlashCommand


class CorkClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.slash = SlashCommand(self)
