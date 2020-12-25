import asyncio
from discord_slash.utils import manage_commands
from modules.guild_ids import guild_ids
from modules.client import CorkClient

loop = asyncio.get_event_loop()

for x in guild_ids:
    loop.run_until_complete(manage_commands.add_slash_command(
        791679306123968553,
        CorkClient.get_settings("token"),
        x,
        "set",
        "알림 세부 설정 관련 명령어입니다.",
        [
            {
                "name": "보기",
                "description": "설정이 필요한 알림들을 보여줍니다.",
                "type": 1,
                "required": False
            },
            {
                "name": "반복",
                "description": "반복 타임 알림 설정 명령어입니다.",
                "type": 1,
                "required": False
            },
            {
                "name": "알림",
                "description": "알림 타입 알림 설정 명령어입니다.",
                "type": 1,
                "required": False
            }
        ]
    ))
