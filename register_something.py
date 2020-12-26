import asyncio
from discord_slash.utils import manage_commands
from modules.client import CorkClient

loop = asyncio.get_event_loop()

loop.run_until_complete(
    manage_commands.add_slash_command(
        791679306123968553,
        CorkClient.get_settings("token"),
        None,
        "타이머",
        "타이머 명령어입니다.",
        [
            manage_commands.create_option(
                "분",
                "분입니다.",
                4,
                True
            ),
            manage_commands.create_option(
                "초",
                "초입니다.",
                4,
                True
            )
        ]
    )
)
