import os
import logging
import discord
from modules.client import CorkClient

logger = logging.getLogger('cork')
logging.basicConfig(level=logging.INFO)  # DEBUG/INFO/WARNING/ERROR/CRITICAL
handler = logging.FileHandler(filename=f'cork.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = CorkClient(command_prefix="c!", intents=discord.Intents.all(), help_command=None)

[bot.load_extension("cogs."+x.replace(".py", "")) for x in os.listdir("cogs") if x.endswith(".py")]

bot.run(bot.get_settings("token"))
