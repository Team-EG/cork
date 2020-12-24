import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashContext
from modules.client import CorkClient
from modules.guild_ids import guild_ids


class Help(commands.Cog):
    def __init__(self, bot: CorkClient):
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="도움말", description="도움말 명령어 입니다.", guild_ids=guild_ids)
    async def help(self, ctx: SlashContext):
        base_embed = discord.Embed(title="Cork 도움말", color=discord.Color.from_rgb(225, 225, 225))
        await ctx.send(embeds=[base_embed])


def setup(bot):
    bot.add_cog(Help(bot))
