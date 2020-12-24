import discord
from modules.client import CorkClient

bot = CorkClient(command_prefix="c!", intents=discord.Intents.all(), help_command=None)

bot.run(bot.get_settings("token"))
