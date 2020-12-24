import logging
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from modules.client import CorkClient
from modules.guild_ids import guild_ids


class Utils(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.bot.slash.get_cog_commands(self)
        self.logger = logging.getLogger("cork")
        print("loaded")

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="ping", guild_ids=guild_ids)
    async def utils_ping(self, ctx: SlashContext):
        await ctx.send(content=f"퐁! ({round(self.bot.latency*1000)}ms)")


def setup(bot):
    bot.add_cog(Utils(bot))
