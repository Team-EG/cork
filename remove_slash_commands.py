import asyncio
from discord_slash.utils import manage_commands
from modules.guild_ids import guild_ids
from modules.client import CorkClient

loop = asyncio.get_event_loop()

for x in guild_ids:
    cmds = loop.run_until_complete(
        manage_commands.get_all_commands(
            791679306123968553,
            CorkClient.get_settings("token"),
            x
        ))
    for y in cmds:
        loop.run_until_complete(
            manage_commands.remove_slash_command(
                791679306123968553,
                CorkClient.get_settings("token"),
                x,
                y["id"])
        )
