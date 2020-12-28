import asyncio
from discord_slash.utils import manage_commands
from modules.client import CorkClient

loop = asyncio.get_event_loop()

loop.run_until_complete(
    manage_commands.add_slash_command(
        791679306123968553,
        CorkClient.get_settings("token_real"),
        None,
        "크레딧",
        "봇 개발자를 보여줍니다."
    )
)
