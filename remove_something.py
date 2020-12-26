import asyncio
from discord_slash.utils import manage_commands
from modules.client import CorkClient

loop = asyncio.get_event_loop()

resp = loop.run_until_complete(
    manage_commands.get_all_commands(
        791679306123968553,
        CorkClient.get_settings("token"),
        None
    )
)

print(resp)

# 792363040007258193
"""
loop.run_until_complete(
    manage_commands.remove_slash_command(
        791679306123968553,
        CorkClient.get_settings("token"),
        None,
        792241248600981504
    )
)
"""